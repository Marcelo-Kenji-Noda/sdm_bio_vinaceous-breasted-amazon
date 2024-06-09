import os
import tomllib
from datetime import datetime


def create_dir(*args):
    if not os.path.exists(os.path.join(*args)):
        os.mkdir(os.path.join(*args))
    return os.path.join(*args)


if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["force_use_date"]:
        current_date = config["general"]["date"]
    else:
        current_date = datetime.now().strftime("%d-%m-%Y")

    main_dir = os.path.join(config["general"]["output_path"], current_date)

    create_dir(config["general"]["output_path"], current_date)
    create_dir(main_dir, "PREP")
    create_dir(main_dir, "MODELS")
    create_dir(main_dir, "INPUT")
    create_dir(main_dir, "OUTPUT")
    create_dir(main_dir, "INFO")
    create_dir(main_dir, "REPORT")
    create_dir(main_dir, "IMAGES")

    for model in config["models"]["selected_models"]:
        create_dir(main_dir, "MODELS", model)
    for model in config["models_pipeline"]["selected_models"]:
        create_dir(main_dir, "MODELS", model)
