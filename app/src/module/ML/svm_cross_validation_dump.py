import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
# from src.module.draw_heatmap import confusionMatrixHeatmap
from copy import deepcopy

# クロスバリデーションの実行


def svm_cross_validation(X, y, groups):

    # パイプラインの作成

    # clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    base_clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))

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
        # clf.fit(X_train, y_train)
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


# モデルの保存
def svm_dump(X, y):

    # 特徴量とラベルを分ける
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))

    # モデルの訓練
    clf.fit(X, y)

    joblib_file = "all_data/svm_model.pkl"
    joblib.dump(clf, joblib_file)
