import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from src.module.draw_heatmap import confusionMatrixHeatmap
import pandas as pd
from datetime import datetime
from src.module.time_function import shift_time, time_to_minutes
import sys

# 誤差の計算


def evaluation_and_verification(actual_data_pass, pred_data_pass, method, subject_data, correction):

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
            file = open(
                "extraction_data/z_all_output/all_extracted_actual_data.txt", "a")
            for d in (extracted_actual_data):
                file.write(f"{d} ")
            file.close()

            print("extracted_pred_data書き込み", len(extracted_pred_data))
            file = open(
                "extraction_data/z_all_output/all_extracted_around_pred_data.txt", "a")
            for d in (extracted_pred_data):
                file.write(f"{d} ")
            file.close()
        else:
            # print("extracted_pred_data書き込み", len(extracted_pred_data))
            # file = open(
            #     "extraction_data/z_all_output/all_extracted_actual_data.txt", "a")
            # for d in (extracted_actual_data):
            #     file.write(f"{d} ")
            # file.close()
            file = open(
                "extraction_data/z_all_output/all_extracted_median_pred_data.txt", "a")
            for d in (extracted_pred_data):
                file.write(f"{d} ")
            file.close()

        # 混同行列を出力
        cm = confusion_matrix(extracted_actual_data, extracted_pred_data, labels=[
                              0, 1], normalize='true')
        print("confusion_matrix")
        print(np.array(cm))

        # 行の合計を計算
        # row_sums = cm.sum(axis=1, keepdims=True)

        # 各セルを行の合計で正規化
        # normalized_cm = cm / row_sums

        data_info = f"valid date count:{len(actual_dates)}, \ndata count:{len(extracted_actual_data)}"
        confusionMatrixHeatmap(np.array(cm), method,
                               data_info, subject_data, correction)

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


def allEvaluationAndVerification(survey_id):

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

    if (survey_id == ""):
        print("Around=====================================")
        evaluate_predictions(actual_array, around_pred_array, "Around")
        print("Median=====================================")
        evaluate_predictions(actual_array, median_pred_array, "Median")
    else:
        print("Around=====================================")
        evaluate_predictions(
            actual_array, around_pred_array, f"Around_{survey_id}")
        print("Median=====================================")
        evaluate_predictions(
            actual_array, median_pred_array,  f"Median_{survey_id}")
        # 評価を行う関数


def evaluate_predictions(actual, pred, method):

    print("cm")
    cm = confusion_matrix(actual, pred,
                          labels=[0, 1], normalize='true')
    print(cm)

    # 正解率を出力
    accuracy = accuracy_score(actual, pred)
    # print("accuracy")
    print(format(accuracy, ".2f"))

    # 適合率を出力
    precision = precision_score(actual, pred)
    # print("precision")
    print(format(precision, ".2f"))

    # 再現率を出力
    recall = recall_score(actual, pred)
    # print("recall")
    print(format(recall, ".2f"))

    # F値を出力
    f1_measure = f1_score(actual, pred)
    # print("f1_measure")
    print(format(f1_measure, ".2f"))

    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成

    plt.imshow(np.array(cm), cmap='Blues', interpolation='nearest')

    data_info = f"data count:{len(actual)}"
    # plt.title(f'Estimation Sleep ({method})')
    plt.text(1.65, -0.55, data_info, fontsize=7)
    plt.colorbar(label='')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.xticks(ticks=[0, 1], labels=[0, 1])
    plt.yticks(ticks=[0, 1], labels=[0, 1])

    for i in range(2):
        for j in range(2):
            text_color = 'white' if np.array(cm)[i, j] >= 0.5 else 'black'
            plt.text(j, i, format(
                np.array(cm)[i, j], ".2f"), ha='center', va='center', color=text_color)

    plt.savefig(
        f'extraction_data/z_all_output/confusion_matrix_all_{method}_pred.png')


# all_output_data.csvから，二乗平均誤差と絶対平均誤差を計算する
def calculateError(survey_id):
    if (survey_id == ""):
        mode_list = ["Around", "Median"]
    else:
        mode_list = ["Around", "Median"]

    df = pd.read_csv("extraction_data/z_all_output/all_output_data.csv",
                     dtype={"sourceVersion": str, "device": str}, low_memory=False)

    for mode in mode_list:
        mode_df = df[df["mode"] == mode]

        print(f"{mode}=====================================")

        # 時間差を計算
        # mode_df['bed_diff_minutes'] = mode_df.apply(lambda row: datetime.strptime(
        #     shift_time(row['actual_bed'], row['estimate_bed'])[1], "%H:%M").time().strftime("%H:%M"), axis=1)
        # mode_df['wake_diff_minutes'] = mode_df.apply(lambda row: datetime.strptime(
        #     shift_time(row['actual_wake'], row['estimate_wake'])[1], "%H:%M").time().strftime("%H:%M"), axis=1)

        # mode_dfの各行に対して時間差を分に変換して格納
        mode_df['bed_diff_minutes'] = mode_df.apply(lambda row: time_to_minutes(
            datetime.strptime(shift_time(row['actual_bed'], row['estimate_bed'])[1], "%H:%M").strftime("%H:%M")), axis=1)
        mode_df['wake_diff_minutes'] = mode_df.apply(lambda row: time_to_minutes(
            datetime.strptime(shift_time(row['actual_wake'], row['estimate_wake'])[1], "%H:%M").strftime("%H:%M")), axis=1)

        # 中心からのズレを抽出
        mode_df['median_shift_diff'] = mode_df['shift']
        mode_df['median_shift_diff_minutes'] = mode_df.apply(lambda row: time_to_minutes(
            datetime.strptime(row['shift_value'], "%H:%M")), axis=1)

        # mode_df.loc[:, 'bed_diff_minutes'] = mode_df.apply(
        #     lambda row: time_difference(row['actual_bed'], row['estimate_bed']), axis=1)
        # mode_df.loc[:, 'wake_diff_minutes'] = mode_df.apply(
        #     lambda row: time_difference(row['actual_wake'], row['estimate_wake']), axis=1)

        # print(mode_df['bed_diff_minutes'])
        # print(mode_df['wake_diff_minutes'])
        # print(mode_df['median_shift_diff'])
        # print(mode_df['median_shift_diff_minutes'])

        # Mean Squared Error(MSE) を計算
        mse_bed = np.mean(mode_df['bed_diff_minutes']**2)
        mse_wake = np.mean(mode_df['wake_diff_minutes']**2)
        mse_median_shift = np.mean(mode_df['median_shift_diff']**2)
        mse_median_shift_value = np.mean(
            mode_df['median_shift_diff_minutes']**2)

        # Root Mean Squared Error(RMSE) を計算
        rmse_bed = np.sqrt(np.mean(mode_df['bed_diff_minutes']**2))
        rmse_wake = np.sqrt(np.mean(mode_df['wake_diff_minutes']**2))
        rmse_median_shift = np.sqrt(
            np.mean(mode_df['median_shift_diff']**2))
        rmse_median_shift_value = np.sqrt(np.mean(
            mode_df['median_shift_diff_minutes']**2))

        # Mean Absolute Error (MAE) を計算
        mae_bed = np.mean(np.abs(mode_df['bed_diff_minutes']))
        mae_wake = np.mean(np.abs(mode_df['wake_diff_minutes']))
        mae__median_shift = np.mean(mode_df['median_shift_diff'])
        mae_median_shift_value = np.mean(mode_df['median_shift_diff_minutes'])

        # 結果を出力
        # print("Bed Time MSE:", format(mse_bed, ".2f"))
        # print("Bed Time RMSE:", format(rmse_bed, ".2f"))
        # print("Bed Time MAE:", format(mae_bed, ".2f"))
        # print("Wake Time MSE:", format(mse_wake, ".2f"))
        # print("Wake Time RMSE:", format(rmse_wake, ".2f"))
        # print("Wake Time MAE:", format(mae_wake, ".2f"))
        # print("Shift MSE:", format(mse_median_shift, ".2f"))
        # print("Shift RMSE:", format(rmse_median_shift, ".2f"))
        # print("Shift MAE:", format(mae__median_shift, ".2f"))
        # print("Shift Time MSE:", format(mse_median_shift_value, ".2f"))
        # print("Shift Time RMSE:", format(rmse_median_shift_value, ".2f"))
        # print("Shift Time MAE:", format(mae_median_shift_value, ".2f"))
        # 値だけを出力するように print 文を修正
        print(format(mse_bed, ".2f"))
        print(format(rmse_bed, ".2f"))
        print(format(mae_bed, ".2f"))
        print(format(mse_wake, ".2f"))
        print(format(rmse_wake, ".2f"))
        print(format(mae_wake, ".2f"))
        print(format(mse_median_shift, ".2f"))
        print(format(rmse_median_shift, ".2f"))
        print(format(mae__median_shift, ".2f"))
        print(format(mse_median_shift_value, ".2f"))
        print(format(rmse_median_shift_value, ".2f"))
        print(format(mae_median_shift_value, ".2f"))


# データのリセット


def dataReset():

    # データの中身をリセット
    file = open(
        "extraction_data/z_all_output/all_extracted_actual_data.txt", "w")
    file.close()
    file = open(
        "extraction_data/z_all_output/all_extracted_around_pred_data.txt", "w")
    file.close()
    file = open(
        "extraction_data/z_all_output/all_extracted_median_pred_data.txt", "w")
    file.close()

    # CSVファイルを読み込む
    df = pd.read_csv("extraction_data/z_all_output/all_output_data.csv")
    # 最初の行だけを取得
    first_row = df.iloc[:0]
    # 最初の行のみを含むDataFrameをCSVファイルに上書き保存
    first_row.to_csv(
        "extraction_data/z_all_output/all_output_data.csv", index=False)

    sleep_label_df = pd.read_csv(
        "all_data/actual_sleep_label.csv")
    # 最初の行だけを取得
    first_row = sleep_label_df.iloc[:0]
    # 最初の行のみを含むDataFrameをCSVファイルに上書き保存
    first_row.to_csv(
        "all_data/actual_sleep_label.csv", index=False)
