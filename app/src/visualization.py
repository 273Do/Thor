import json
import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap
from datetime import datetime, timedelta
from src.module.time_function import subtract_time
import src.module.all_output as allOutput

# データ可視化用の関数


def dataVisualization(mode, subject_data):

    # 時間の設定を読み込む
    json_open = open('./src/settings.json', 'r')
    time = json.load(json_open)

    # CSVファイルを読み込む
    df = pd.read_csv(mode["metadata"]["csv_file_path"].replace(
        "{ID_HERE}", f"{subject_data[0]}_{subject_data[1]}_{subject_data[2]}"), low_memory=False)

    # 指定の日付範囲でフィルタリング
    df = df[(df["startDate"] >= time["time"]["start_date"])
            & (df["endDate"] <= time["time"]["end_date"])]

    # "startDate" と "endDate" の列を datetime 型に変換
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])

    # 抽出対象を指定してフィルタリング
    if (mode["mode_name"] == "sleep"):
        # デバイス名を取得
        # df = df[(df["sourceName"].str.contains("Watch")) & (df["value"] == "HKCategoryValueSleepAnalysisInBed")]
        df = df[(df["sourceVersion"].str.contains("10.")) & (
            df["value"] == "HKCategoryValueSleepAnalysisInBed")]
    elif (mode["mode_name"] == "step"):
        df = df[df["device"].str.contains("name:iPhone")]

    unique_dates = pd.date_range(start=time["time"]["start_date"], end=datetime.strptime(
        time["time"]["end_date"], "%Y-%m-%d") - timedelta(days=1)).date
    observed_dates = df['startDate'].dt.date.unique()
    heatmap_data = np.zeros((len(unique_dates), 288))  # 288：24時間 x 60分 / 5分刻み
    print(mode["mode_name"])

    previous_day_bed = None  # 前日の就寝時間を格納する変数(日を跨がない場合)

    # 各行に対して、startDate から endDate の範囲を1に設定
    for i, date in enumerate(unique_dates):
        raw_time_data = [[], []]
        actual_time_data = []
        if (len(observed_dates) > 0):
            if date in observed_dates:
                date_data = df[df['startDate'].dt.date == date]
                for _, row in date_data.iterrows():
                    # MEMO:
                    # startDateとendDateの日付がズレてるものはヒートマップに記載されない
                    start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (
                        row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
                    end_index = int(
                        (row['endDate'].hour * 60 + row['endDate'].minute) / 5)
                    heatmap_data[i, start_index:end_index + 1] = 1
                    # if(row['endDate'].)
                    # print(row['startDate'].strftime("%Y-%m-%d"),row['endDate'].strftime("%Y-%m-%d"))
                    # MEMO:
                    # startDateとendDateの日付がズレてるものは統合データに記載されない
                    if (row['startDate'].strftime("%Y-%m-%d") == row['endDate'].strftime("%Y-%m-%d")):
                        raw_time_data[0].append(
                            (row['startDate']).strftime("%H:%M"))
                        raw_time_data[1].append(
                            (row['endDate']).strftime("%H:%M"))

            else:
                heatmap_data[i, 0:288] = 0
        else:
            heatmap_data[i, 0:288] = 0

        if ((mode["mode_name"] == "sleep") and (len(raw_time_data[0]) > 0) and (len(raw_time_data[1]) > 0)):
            # print(f"rawdata{raw_time_data[1]}")
            # print(date)
            tmp = "00:00"  # 一つ前の時間の差分用

            if (previous_day_bed == None):
                # if(len(raw_time_data[0]) > 0):
                actual_time_data.append(raw_time_data[0][0])
            else:
                actual_time_data.append(previous_day_bed)
                previous_day_bed = None
            print("生データ", raw_time_data)
            for j, time in enumerate(raw_time_data[1]):
                result = subtract_time(f"{time}:00", f"{tmp}:00")
                tmp = time
                if (datetime.strptime(result, '%H:%M:%S') > datetime.strptime("09:30:00", '%H:%M:%S')):
                    # print(result)
                    # print(j,time,result) #j-1番目をactual_wakeとする
                    actual_time_data.append(raw_time_data[1][j-1])
                    previous_day_bed = raw_time_data[0][j]
                    # 次の日に[j]をstartとする
            print(date, "正解データ", actual_time_data)
            if ((len(actual_time_data) == 1)):
                print("len1", date)
                print(raw_time_data)
                actual_time_data.append(
                    raw_time_data[1][len(raw_time_data[1])-1])
            #     print(len(raw_time_data[1])-1)
            # print(f"result{actual_time_data}")
        # print(f"{date}：{mode["mode_name"]}")
        # print(f"{raw_time_data[0]}") #min:bed
        # print(f"{raw_time_data[1]}") #max:wake

            allOutput.actual_sleep_data[date] = actual_time_data
            # print(date,allOutput.actual_sleep_data[date])
    print(allOutput.actual_sleep_data)

    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成
    plt.imshow(heatmap_data, cmap=ListedColormap(
        ['#ffffff', '#08306b']), aspect='auto', interpolation='none')

    # タイトル，軸の設定
    plt.title(mode["heatmap"]["title"])
    plt.xlabel(mode["heatmap"]["x_label"])
    plt.ylabel(mode["heatmap"]["y_label"])
    plt.yticks(range(len(unique_dates)), [date.strftime(
        '%Y-%m-%d') for date in unique_dates], fontsize=8)

    # x軸の目盛りを設定
    time_labels = np.arange(0, 289, 6*12)  # 6時間ごとに目盛りを表示
    plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])

    # カラーバーを表示
    cbar = plt.colorbar(ticks=[0, 1])
    cbar.set_ticklabels(mode["color_bar"]["tick_labels"])
    cbar.set_label(mode["color_bar"]["label"])

    # グラフを保存
    plt.savefig(mode["metadata"]["image_name"] +
                "_" + subject_data[0] + ".png")

    # ヒートマップデータと日付をテキストファイルに出力(正解データ)
    file = open(f"./extraction_data/actual_{mode["mode_name"]}_data.txt", "w")
    # ヒートマップのデータを配列として格納
    for d in list(itertools.chain.from_iterable(heatmap_data)):
        file.write(f"{d} ")
    file.write("\n")
    # 日付データを文字列に変換してリストに格納
    date_strings = [date.strftime("%Y-%m-%d") for date in observed_dates]
    for date_str in date_strings:
        file.write(f"{date_str} ")
    file.write("\n")
    # 日付データ(フォーマット前)を文字列に変換してリストに格納
    file.close()
