import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from src.module.draw_heatmap import confusionMatrixHeatmap
import sys

# 誤差の計算


def calculate_error(actual_data_pass, pred_data_pass, method, subject_data):

    # ファイルからデータを読み込む
    actual_file = open(actual_data_pass, 'r')
    actual_array = actual_file.read().splitlines()
    pred_file = open(pred_data_pass, 'r')
    pred_array = pred_file.read().splitlines()

    # print(len(actual_array))
    if (len(actual_array) > 1):
        actual_data = actual_array[0].split()
        actual_dates = actual_array[1].split()

        pred_data = pred_array[0].split()
        pred_dates = pred_array[1].split()

        # np配列に変換，288個ずつに分割
        actual_data = np.array(actual_data, dtype=float).reshape(-1, 288)
        pred_data = np.array(pred_data, dtype=float).reshape(-1, 288)

        # 日付をkeyとして，それぞれのデータのオブジェクト(辞書)を作成する
        actual_dictionary = {}
        pred_dictionary = {}

        for i in range(len(actual_data)):
            key = pred_dates[i]
            actual_dictionary[key] = actual_data[i]
            pred_dictionary[key] = pred_data[i]

        # keyと実際に観測された正解データとkeyを比較してデータを抽出する
        extracted_actual_data = []
        extracted_pred_data = []
        for key in actual_dictionary.keys():
            if key in actual_dates:
                extracted_actual_data.append(actual_dictionary[key])
                extracted_pred_data.append(pred_dictionary[key])
        extracted_actual_data = list(
            itertools.chain.from_iterable(extracted_actual_data))
        extracted_pred_data = list(
            itertools.chain.from_iterable(extracted_pred_data))

    # mse = np.mean((actual_array - pred_array) ** 2)
    # mae = np.mean(np.abs(actual_array - pred_array))
    # print(f"MSE: {mse}") # 平均二乗誤差
    # print(f"MAE: {mae}") # 平均絶対誤差

        # ここで01の統合データ(extracted_actual_dataとextracted_pred_data)に書き込みをする
        if (method == "Around"):
            print("extracted_actual_data書き込み", len(extracted_actual_data))
            # "extraction_data/z_all_output/all_exo"
            file = open(
                "extraction_data/z_all_output/all_extracted_actual_data.txt", "w")
            for d in (extracted_actual_data):
                file.write(f"{d} ")
            file.close()

            print("extracted_pred_data書き込み", len(extracted_pred_data))
            file = open(
                "extraction_data/z_all_output/all_extracted_around_pred_data.txt", "w")
            for d in (extracted_pred_data):
                file.write(f"{d} ")
            file.close()
        else:
            print("extracted_pred_data書き込み", len(extracted_pred_data))
            file = open(
                "extraction_data/z_all_output/all_extracted_median_pred_data.txt", "w")
            for d in (extracted_pred_data):
                file.write(f"{d} ")
            file.close()

        # 混同行列を出力
        cm = confusion_matrix(extracted_actual_data, extracted_pred_data, labels=[
                              1, 0], normalize='true')
        print("confusion_matrix")
        print(np.array(cm))

        # 行の合計を計算
        # row_sums = cm.sum(axis=1, keepdims=True)

        # 各セルを行の合計で正規化
        # normalized_cm = cm / row_sums

        data_info = f"valid date count:{len(actual_dates)}, \ndata count:{len(extracted_actual_data)}"
        confusionMatrixHeatmap(np.array(cm), method, data_info, subject_data)

        # 正解率を出力
        accuracy = accuracy_score(extracted_actual_data, extracted_pred_data)
        print("accuracy")
        print(format(accuracy, ".2f"))

        # 適合率を出力
        precision = precision_score(extracted_actual_data, extracted_pred_data)
        print("precision")
        print(format(precision, ".2f"))

        # 再現率を出力
        recall = recall_score(extracted_actual_data, extracted_pred_data)
        print("recall")
        print(format(recall, ".2f"))

        # F値を出力-F1-measure
        f1_measure = f1_score(extracted_actual_data, extracted_pred_data)
        print("f1_measure")
        print(format(f1_measure, ".2f"))

        # sys.exit()
        return [format(accuracy, ".2f"), format(precision, ".2f"), format(recall, ".2f"), format(f1_measure, ".2f"), [actual_data, pred_data, pred_dates]]

    else:
        print("正解データが観測されていません．")
        return ["NoData", "NoData", "NoData", "NoData"]

# 統合データの混同行列を出力


def all_calculate_error():

    # ファイルからデータを読み込む
    actual_array = np.loadtxt(
        "extraction_data/z_all_output/all_extracted_actual_data.txt")
    around_pred_array = np.loadtxt(
        "extraction_data/z_all_output/all_extracted_around_pred_data.txt")
    median_pred_array = np.loadtxt(
        "extraction_data/z_all_output/all_extracted_median_pred_data.txt")

    # around_pred_cm = confusion_matrix(actual_array, around_pred_array,
    #                                   labels=[1, 0], normalize='true')
    # median_pred_cm = confusion_matrix(actual_array, median_pred_array,
    #                                   labels=[1, 0], normalize='true')

    print("around=====================================")
    evaluate_predictions(actual_array, around_pred_array, "Around")
    print("median=====================================")
    evaluate_predictions(actual_array, median_pred_array, "Median")


# 評価を行う関数
def evaluate_predictions(actual, pred, method):

    print("cm")
    cm = confusion_matrix(actual, pred,
                          labels=[1, 0], normalize='true')
    print(cm)

    # 正解率を出力
    accuracy = accuracy_score(actual, pred)
    print("accuracy")
    print(format(accuracy, ".2f"))

    # 適合率を出力
    precision = precision_score(actual, pred)
    print("precision")
    print(format(precision, ".2f"))

    # 再現率を出力
    recall = recall_score(actual, pred)
    print("recall")
    print(format(recall, ".2f"))

    # F値を出力
    f1_measure = f1_score(actual, pred)
    print("f1_measure")
    print(format(f1_measure, ".2f"))

    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成

    plt.imshow(np.array(cm), cmap='Blues', interpolation='nearest')

    data_info = f"data count:{len(actual)}"
    # plt.title(f'Estimation Sleep ({method})')
    plt.text(1.65, -0.55, data_info, fontsize=7)
    plt.colorbar(label='Count')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.xticks(ticks=[0, 1], labels=['Positive', 'Negative'])
    plt.yticks(ticks=[0, 1], labels=['Positive', 'Negative'])

    for i in range(2):
        for j in range(2):
            plt.text(j, i, format(
                np.array(cm)[i, j], ".2f"), ha='center', va='center', color='black')

    plt.savefig(
        f'extraction_data/z_all_output/confusion_matrix_all_{method}_pred.png')


# all_output_data.csvから，二乗平均誤差と絶対平均誤差を計算する
