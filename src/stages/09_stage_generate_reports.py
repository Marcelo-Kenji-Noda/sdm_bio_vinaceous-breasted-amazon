import json
import os
import tomllib
from datetime import datetime

import matplotlib.pyplot as plt
from PIL import Image

if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["force_use_date"]:
        current_date = config["general"]["date"]
    else:
        current_date = datetime.now().strftime("%d-%m-%Y")

    # Directory containing model folders
    models_directory = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/MODELS"
    output_directory = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/REPORT/METRICS"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Function to add text to the plot
    def add_text(ax, text, position, fontsize=12):
        ax.text(
            position[0],
            position[1],
            text,
            transform=ax.transAxes,
            fontsize=fontsize,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
        )

    # Traverse through each subfolder in the MODELS directory
    for model_folder in os.listdir(models_directory):
        model_path = os.path.join(models_directory, model_folder)
        if os.path.isdir(model_path):
            json_file_path = os.path.join(model_path, "model.json")
            roc_file_path = os.path.join(model_path, "roc.png")

            if os.path.exists(json_file_path) and os.path.exists(roc_file_path):
                try:
                    with open(json_file_path, "r") as json_file:
                        data = json.load(json_file)

                    # Extract the required information
                    name = data["input"]["name"]
                    bic = data["output"]["BIC"]
                    aic = data["output"]["AIC"]
                    auc_roc = data["output"]["AUC_ROC"]
                    cross_validation_mean = data["output"]["cross_validation_mean"]

                    # Create the figure
                    fig, ax = plt.subplots(1, 2, figsize=(15, 10))

                    # Add the ROC plot
                    roc_img = Image.open(roc_file_path)
                    ax[0].imshow(roc_img)
                    ax[0].axis("off")

                    # Add the text information
                    text_str = (
                        f"Model: {name}\n"
                        f"BIC: {bic}\n"
                        f"AIC: {aic}\n"
                        f"AUC_ROC: {auc_roc}\n"
                        f"Cross-validation mean: {cross_validation_mean:.2f}%"
                    )
                    add_text(ax[1], text_str, position=(0.05, 0.95))

                    # Hide the second axis
                    ax[1].axis("off")

                    # Save the figure
                    output_path = os.path.join(output_directory, f"{name}.png")
                    plt.savefig(output_path, bbox_inches="tight", pad_inches=0.1)
                    plt.close(fig)

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {json_file_path}: {e}")
                except KeyError as e:
                    print(f"Missing key in {json_file_path}: {e}")

    print("Processing complete. Files saved at:", output_directory)

    # Directory containing PNG files
    output_pdf_path = f"{output_directory}/combined_report.pdf"

    # Get a list of all PNG files in the directory
    png_files = [
        os.path.join(output_directory, file)
        for file in os.listdir(output_directory)
        if file.endswith(".png")
    ]

    # Check if any PNG files were found
    if not png_files:
        print("No PNG files found in the directory:", output_directory)
    else:
        # Open each PNG file and append to a list
        images = [Image.open(png_file) for png_file in png_files]

        # Save as a single PDF file
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])

        print("PDF report saved at:", output_pdf_path)
