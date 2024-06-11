# ML
import json
import os
import tomllib
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sdm_bio.models import output_model, plot_roc_curve
from sklearn import metrics, model_selection
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.model_selection import LeaveOneOut
from xgboost import XGBClassifier

MODELS = {
    "random_forest_class": RandomForestClassifier(),
    "extra_tree_class": ExtraTreesClassifier(),
    "ada_class": AdaBoostClassifier(),
    "bagging_class": BaggingClassifier(),
    "gbooster": GradientBoostingClassifier(),
    "xgb_class": XGBClassifier(),
    "lightgbm": LGBMClassifier(),
    "maxent": LogisticRegression(),
}


def evaluate_clf(
    clf,
    X,
    y,
    name,
    filepath,
    k=5,
    test_size=0.2,
    scoring="f1_weighted",
    feature_names=None,
):
    """
    Evaluate a classifier and display evaluation metrics.

    Args:
        clf: The classifier to evaluate.
        X (pd.DataFrame): Features data.
        y (pd.Series): Target data.
        name (str): Name of the classifier.
        k (int, optional): Number of folds for cross-validation.
        test_size (float): Proportion of the dataset to include in the test split.
        scoring (str): Scoring metric for cross-validation.
        feature_names (list[str], optional): List of feature names.

    Returns:
        clf: Fitted classifier.
        m_values: Dictionary of evaluation metrics.
    """

    print(name)
    X_train, X_test, y_train, y_true = model_selection.train_test_split(
        X,
        y,
        test_size=test_size,  # Test data size
        shuffle=True,  # Shuffle the data before split
        stratify=y,  # Keeping the appearance/non-appearance ratio of Y
    )

    scores = []
    if k:  # Cross-validation
        kf = model_selection.KFold(n_splits=k)  # k-fold
        scores = model_selection.cross_val_score(
            clf, X_train, y_train, cv=kf, scoring=scoring
        )

    clf.fit(X_train, y_train)  # Training of classifiers
    y_pred = clf.predict(X_test)  # Classifier predictions

    # ROC
    probs = clf.predict_proba(X_test)
    prob = probs[:, 1]
    fper, tper, thresholds = metrics.roc_curve(y_true, prob)
    plot_roc_curve(fper, tper, filepath)

    # AIC and BIC (when possible)
    aic = None
    bic = None
    if hasattr(clf, "predict_proba"):
        ll = -log_loss(y_true, probs, normalize=False)
        n_params = len(clf.coef_.flatten()) if hasattr(clf, "coef_") else len(X.columns)
        aic = 2 * n_params - 2 * ll
        bic = n_params * np.log(len(y_true)) - 2 * ll

    # LOOCV
    # loo = LeaveOneOut()
    # loo_scores = model_selection.cross_val_score(clf, X, y, cv=loo, scoring=scoring)
    # loo_mean_score = loo_scores.mean()

    m_values = {
        "input": {
            "name": name,
            "k_folds": k,
        },
        "output": {
            "cross_validation_mean": float(scores.mean() * 100),
            "cross_validation_err": f"+/- {scores.std() * 200}",
            "accuracy_score": float(metrics.accuracy_score(y_true, y_pred)),
            "AUC_ROC": float(metrics.roc_auc_score(y_true, y_pred)),
            "class_report": str(metrics.classification_report(y_true, y_pred)),
            "confusion_matrix": str(metrics.confusion_matrix(y_true, y_pred)),
            "probs": [list(i) for i in probs],
            "fper": list(fper),
            "tper": list(tper),
            "AIC": float(aic),
            "BIC": float(bic),
        },
    }
    print(
        f'AUC:{m_values["output"]["accuracy_score"]}',
        f'confusion_matrix:\n{m_values["output"]["confusion_matrix"]}',
        f'AIC: {m_values["output"]["AIC"]}',
        f'BIC: {m_values["output"]["AIC"]}',
        sep="\n",
    )
    # if hasattr(clf, "feature_importances_"):
    #    print("Feature importances")
    #    for f, imp in zip(feature_names, clf.feature_importances_):
    #        print("%20s: %s" % (f, round(imp * 100, 1)))
    #    print()

    return clf, m_values


if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["force_use_date"]:
        current_date = config["general"]["date"]
    else:
        current_date = datetime.now().strftime("%d-%m-%Y")

    df = pd.read_parquet(
        os.path.join(
            config["general"]["output_path"], current_date, "OUTPUT/data.parquet"
        )
    ).dropna()

    for model in config["models"]["selected_models"]:
        if model not in MODELS:
            raise ValueError(
                f"{model} is not a possible model. These are the options {MODELS.keys()}"
            )

    for model_name in config["models"]["selected_models"]:
        filepath = os.path.join(
            config["general"]["output_path"],
            current_date,
            f"MODELS/{model_name}/roc.png",
        )
        df_cp = df.copy()
        y = df_cp.pop("target")
        X = df_cp.copy()

        _, m = evaluate_clf(
            MODELS[model_name],
            X,
            y,
            name=model_name,
            filepath=filepath,
            k=config["models"]["k"],
            test_size=config["models"]["test_size"],
            scoring=config["models"]["scoring"],
            feature_names=X.columns,
        )
        image_output_path = os.path.join(
            config["general"]["output_path"],
            current_date,
            f"MODELS/{model_name}/IMAGES/",
        )
        with open(
            os.path.join(
                config["general"]["output_path"],
                current_date,
                config["feature_selection"]["file_feature_selection_info"],
            )
        ) as f:
            tiff_files = json.load(f)["tiff_files"]

        tiff_files = [
            Path(os.path.join(config["general"]["output_path"], "features/MANT", i))
            for i in tiff_files
        ]

        ########
        output_model(
            MODELS[model_name],
            tiff_output_files=tiff_files,
            output_dir=image_output_path,
        )
        try:
            with open(
                os.path.join(
                    config["general"]["output_path"],
                    current_date,
                    f"MODELS/{model_name}/",
                    "model.json",
                ),
                "w",
            ) as f:
                json.dump(m, f)
        except:
            print(m)
    print(f"[SUCESS] RAN MODELS: {config['models']['selected_models']}")
