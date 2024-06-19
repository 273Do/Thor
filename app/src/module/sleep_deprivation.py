import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from time_function import timedelta_to_hhmmss, shift_time
from matplotlib.colors import ListedColormap
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
# from src.module.draw_heatmap import confusionMatrixHeatmap

final_result = "extraction_data/z_all_output/final_result.csv"

actual_flg = []
estimate_flg = []


def sleep_deprivation():
    print("sleep_deprivation")

    # データの読み込み
    df = pd.read_csv(final_result, low_memory=False)

    # 時間型に変換
    df['actual_bed_datetime'] = pd.to_datetime(
        df['actual_bed_datetime'])
    df['actual_wake_datetime'] = pd.to_datetime(
        df['actual_wake_datetime'])
    df['q4_bed_estimate_datetime'] = pd.to_datetime(
        df['q4_bed_estimate_datetime'])
    df['q5_wake_estimate_datetime'] = pd.to_datetime(
        df['q5_wake_estimate_datetime'])

    # idのリストを作成
    id_list = df["id"].unique()
    # print(id_list)
    for id in id_list:

        id_df = df[df["id"] == id][["actual_bed_datetime", "actual_wake_datetime", "q4_bed_estimate_datetime",
                                   "q5_wake_estimate_datetime"]]

        # print(id_df)

        # 就寝時刻の平均を求める
        # 実際
        mean_a_bed = meanTime(id_df["actual_bed_datetime"])
        # 推定
        mean_q4_bed = meanTime(id_df["q4_bed_estimate_datetime"])

        # 睡眠時間を求める
        # 実際
        sleep_a = sleepTime(id_df["actual_bed_datetime"],
                            id_df["actual_wake_datetime"])
        # 推定
        sleep_e = sleepTime(id_df["q4_bed_estimate_datetime"],
                            id_df["q5_wake_estimate_datetime"])
        # 睡眠時間の平均を求める
        # 実際
        mean_sleep_a = meanTime(sleep_a)
        # # 推定
        mean_sleep_e = meanTime(sleep_e)

        # print(sleep_a)
        # 実際の値で異常検知
        sleepAnomalyDetection(
            "actual", mean_a_bed, id_df["actual_bed_datetime"], mean_sleep_a, sleep_a)
        sleepAnomalyDetection(
            "estimate", mean_q4_bed, id_df["q4_bed_estimate_datetime"], mean_sleep_e, sleep_e)
    print("actual_flg")
    print(actual_flg)
    print("estimate_flg")
    print(estimate_flg)

    # 正解率を出力
    accuracy = accuracy_score(actual_flg, estimate_flg)
    print("accuracy")
    print(format(accuracy, ".2f"))

    # 適合率を出力
    precision = precision_score(actual_flg, estimate_flg)
    print("precision")
    print(format(precision, ".2f"))

    # 再現率を出力
    recall = recall_score(actual_flg, estimate_flg)
    print("recall")
    print(format(recall, ".2f"))

    # F値を出力-F1-measure
    f1_measure = f1_score(actual_flg, estimate_flg)
    print("f1_measure")
    print(format(f1_measure, ".2f"))

    cm = confusion_matrix(actual_flg, estimate_flg,
                          labels=[0, 1], normalize='true')
    print("confusion_matrix")
    print(np.array(cm))

    plt.figure()  # 新しいFigureを作成

    plt.imshow(np.array(cm), cmap='Blues', interpolation='nearest')

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
        f'extraction_data/sleep_deprivation_confusion_matrix.png')

    # 結果の表示


# 異常検知を行う関数
def sleepAnomalyDetection(mode, bed_mean, bed_df, sleep_mean, sleep_df):

    print("平均就寝時刻", bed_mean)
    print("平均睡眠時間", sleep_mean)

    flg = []

    for bed, sleep in zip(bed_df, sleep_df):
        bed_shift = shift_time(bed.time().strftime('%H:%M'),
                               bed_mean.strftime('%H:%M'))
        print(f"{mode}--------------")
        print(bed_shift)

        # print(bed, sleep)
        # if (((bed > bed_mean) and (bed - bed_mean >= 2)) or ((sleep > sleep_mean) and (sleep - sleep_mean >= 2))):
        #     Flg.append(1)
        # else:
        #     Flg.append(0)

        bed_time = bed.time() if isinstance(bed, pd.Timestamp) else bed
        sleep_time = sleep.time() if isinstance(sleep, pd.Timestamp) else sleep
        bed_mean_time = bed_mean.time() if isinstance(
            bed_mean, pd.Timestamp) else bed_mean
        sleep_mean_time = sleep_mean.time() if isinstance(
            sleep_mean, pd.Timestamp) else sleep_mean

        print(bed_time, sleep_time)
        if (((bed_shift[0] == -1) and ((bed_time.hour - bed_mean_time.hour) * 60 + (bed_time.minute - bed_mean_time.minute) >= 120)) or
                ((sleep_mean_time > sleep_time) and ((sleep_mean_time.hour - sleep_time.hour) * 60 + (sleep_mean_time.minute - sleep_time.minute) >= 120))):
            if (mode == "actual"):
                actual_flg.append(1)

            else:
                estimate_flg.append(1)
            flg.append(1)
            print(1)
        else:
            if (mode == "actual"):
                actual_flg.append(0)
            else:
                estimate_flg.append(0)
            flg.append(0)
            print(0)
        # if(bed_time > bed_mean_time):
        # if (((bed_time > bed_mean_time) and ((bed_time.hour - bed_mean_time.hour) * 60 + (bed_time.minute - bed_mean_time.minute) >= 120)) or
        #         ((sleep_mean_time > sleep_mean) and ((sleep_mean_time.hour - sleep_time.hour) * 60 + (sleep_mean_time.minute - sleep_time.minute) >= 120))):
        #     if (mode == "actual"):
        #         actual_flg.append(1)
        #     else:
        #         estimate_flg.append(1)
        #     flg.append(1)
        # else:
        #     if (mode == "actual"):
        #         actual_flg.append(0)
        #     else:
        #         estimate_flg.append(0)
        #     flg.append(0)

    # print(flg)

    # print(actual_flg)
    # print(estimate_flg)
    # その日の就寝時刻が就寝時刻の平均時間より2時間以上遅い場合は異常(1)とする

    # その日の睡眠時間が睡眠時間の平均より2時間以上短い場合は異常(1)とする

    # 平均時間を計算する関数


def meanTime(df):
    df['time'] = pd.to_datetime(df, format='%H:%M:%S').dt.time

    # adjusted_time 列を追加して時間を調整
    df['adjusted_time'] = df['time'].apply(lambda x: pd.Timestamp.combine(pd.Timestamp.today(
    ), x) + pd.Timedelta(days=1) if x.hour < 12 else pd.Timestamp.combine(pd.Timestamp.today(), x))

    # 平均時間を計算
    mean_time = df['adjusted_time'].mean()

    # 平均時間を24時間フォーマットに戻す
    mean_time_of_day = (mean_time - pd.Timestamp("1970-01-01")
                        ) // pd.Timedelta('1s') % (24 * 3600)
    mean_time_of_day = pd.to_datetime(mean_time_of_day, unit='s').time()

    return mean_time_of_day

# 睡眠時間を求める関数


def sleepTime(bed_df, wake_df):
    bed_df['bed_time'] = pd.to_datetime(
        bed_df, format='%H:%M:%S').dt.time
    wake_df['wake_time'] = pd.to_datetime(
        wake_df, format='%H:%M:%S').dt.time

    bed_df['adjusted_bed_time'] = bed_df['bed_time'].apply(lambda x: pd.Timestamp.combine(pd.Timestamp.today(
    ), x) + pd.Timedelta(days=1) if x.hour < 12 else pd.Timestamp.combine(pd.Timestamp.today(), x))
    wake_df['adjusted_wake_time'] = wake_df['wake_time'].apply(lambda x: pd.Timestamp.combine(pd.Timestamp.today(
    ), x) + pd.Timedelta(days=1) if x.hour < 12 else pd.Timestamp.combine(pd.Timestamp.today(), x))

    # 就寝時間を計算
    bed_df['sleep_duration'] = wake_df['adjusted_wake_time'] - \
        bed_df['adjusted_bed_time']

    # マイナスの時間を修正（日を跨ぐ場合）
    bed_df['sleep_duration'] = bed_df['sleep_duration'].apply(
        lambda x: x + pd.Timedelta(days=1) if x.total_seconds() < 0 else x)

    # 就寝時間を分に変換
    sleep_time = bed_df['sleep_duration'].apply(
        timedelta_to_hhmmss)

    return sleep_time


sleep_deprivation()
