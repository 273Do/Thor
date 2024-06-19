import numpy as np
import pandas as pd
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold
from copy import deepcopy


def random_forest_cross_validation(X, y, groups):
    # パイプラインの作成
    base_clf = make_pipeline(StandardScaler(), RandomForestClassifier())

    # クロスバリデーションの設定
    logo = LeaveOneGroupOut()

    # クロスバリデーションの実行
    scores = cross_val_score(base_clf, X, y, groups=groups, cv=logo)

    print("Cross-validation scores: ", scores)
    print("Average score: ", np.mean(scores))

    # 評価指標の格納リスト
    confusion_matrices = []
    f1_scores = []
    precision_scores = []
    recall_scores = []
    trained_models = []

    for train_index, test_index in logo.split(X, y, groups):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # モデルの訓練
        clf = deepcopy(base_clf)  # 各分割で新しいモデルを作成
        clf.fit(X_train, y_train)

        # フィッティングしたモデルを保存
        trained_models.append(clf)

        # 予測
        y_pred = clf.predict(X_test)

        # 混同行列の計算
        cm = confusion_matrix(y_test, y_pred)
        confusion_matrices.append(cm)

        # F値の計算
        f1 = f1_score(y_test, y_pred, average='weighted')
        f1_scores.append(f1)

        # 適合率の計算
        precision = precision_score(y_test, y_pred, average='weighted')
        precision_scores.append(precision)

        # 再現率の計算
        recall = recall_score(y_test, y_pred, average='weighted')
        recall_scores.append(recall)

    print("Confusion Matrices:")

    for i, cm in enumerate(confusion_matrices):
        print("---------------------------------")
        print(f"Fold {i+1}:\n{cm}\n")

    print("F1 Scores:", f1_scores)
    print("Average F1 Score:", np.mean(f1_scores))

    print("Precision Scores:", precision_scores)
    print("Average Precision Score:", np.mean(precision_scores))

    print("Recall Scores:", recall_scores)
    print("Average Recall Score:", np.mean(recall_scores))


def balanced_random_forest_cross_validation(X, y, groups):
    # base_clf = make_pipeline(StandardScaler(), BalancedRandomForestClassifier(
    # sampling_strategy="all", replacement=True, max_depth=50, random_state=0, bootstrap=False))

    base_clf = BalancedRandomForestClassifier(
        sampling_strategy="all", replacement=True, max_depth=50, random_state=0, bootstrap=False)

    logo = LeaveOneGroupOut()
    scores = cross_val_score(base_clf, X, y, groups=groups, cv=logo)
    # stratifiedkfold = StratifiedKFold(n_splits=10)
    # scores = cross_val_score(base_clf, X, y, cv=stratifiedkfold)

    print("Cross-validation scores: ", scores)
    print("Average score: ", np.mean(scores))

    confusion_matrices = []
    f1_scores = []
    precision_scores = []
    recall_scores = []
    trained_models = []
    feature_importances = []

    for train_index, test_index in logo.split(X, y, groups):
        # for train_index, test_index in logo.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        clf = deepcopy(base_clf)
        clf.fit(X_train, y_train)
        trained_models.append(clf)

        model = clf.named_steps['balancedrandomforestclassifier']
        feature_importances.append(model.feature_importances_)

        y_pred = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        confusion_matrices.append(cm)

        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=1)
        f1_scores.append(f1)

        precision = precision_score(
            y_test, y_pred, average='weighted', zero_division=1)
        precision_scores.append(precision)

        recall = recall_score(
            y_test, y_pred, average='weighted', zero_division=1)
        recall_scores.append(recall)

    avg_feature_importances = np.mean(feature_importances, axis=0)

    print("Confusion Matrices:")
    for i, cm in enumerate(confusion_matrices):
        print("---------------------------------")
        print(f"Fold {i+1}:\n{cm}\n")

    print("F1 Scores:", f1_scores)
    print("Average F1 Score:", np.mean(f1_scores))
    print("Precision Scores:", precision_scores)
    print("Average Precision Score:", np.mean(precision_scores))
    print("Recall Scores:", recall_scores)
    print("Average Recall Score:", np.mean(recall_scores))
    print("Feature Importances:", avg_feature_importances)
