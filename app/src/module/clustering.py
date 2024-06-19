import urllib.request
import csv
import os
import json
import sys
import itertools
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from src.module.set_reference_time import setReferenceTime
from src.module.time_function import shift_time, subtract_time

# kmeansのチュートリアル
# url = "https://raw.githubusercontent.com/maskot1977/ipython_notebook/master/toydata/iris.txt"

# filename = url.split("/")[-1]
# urllib.request.urlretrieve(url, filename)
# df = pd.read_csv(filename, delimiter="\t", index_col=0)
# # df
# print(df.iloc[:, :2])
# filename = url.split("/")[-1]
# urllib.request.urlretrieve(url, filename)

# kmeans_model = KMeans(n_clusters=3).fit(df.iloc[:, :2])

# print(kmeans_model.labels_)
# print(kmeans_model.cluster_centers_)


# 精査範囲を指定して，全員分のsleepを格納する．

# クラスタリング関係のデータのファイル名
clustering_label_pass = ["2d_clustering_label_data",
                         "sumValue_1d_clustering_label_data",
                         "valueCount_1d_clustering_label_data"]

# kmeansの実装


def clustering(time_list):

    start, end = time_list[0], time_list[1]

    # sys.exit()

    # dataフォルダの中のディレクトリ名を全て取得
    file_names = os.listdir('./data/')

    # モードの設定ファイルを読み込む
    json_open = open('./src/settings.json', 'r')
    mode = json.load(json_open)

    # 精査する日付の範囲のリスト
    unique_dates = pd.date_range(start=mode["time"]["start_date"], end=datetime.strptime(
        mode["time"]["end_date"], "%Y-%m-%d") - timedelta(days=1)).date

    # 外出検知のラベルを格納するファイル
    all_go_out_label = pd.read_csv("all_data/1d_clustering_step_data.csv")
    all_go_out_label['startDate'] = pd.to_datetime(
        all_go_out_label['startDate'])
    all_go_out_label['endDate'] = pd.to_datetime(all_go_out_label['endDate'])
    # print(unique_dates)

    # 統計データによる精査範囲の時間を取得
    weekday_time, holiday_time = setReferenceTime([94, 4], [94, 4])
    # print(weekday_time, holiday_time)
    print(f"weekday_time:{weekday_time}")
    print(f"holiday_time:{holiday_time}")
    # =>['3:00', '4:15', '12:00', '21:00'] ['3:00', '4:45', '12:45', '20:45']

    # その中のstepデータを範囲指定して取得
    allStep_data = []
    allStep_startDate = []
    allStep_endDate = []
    allStep_name = []

    if (time_list != "statistics"):
        header_titles = {}
        for hour in range(start, end):
            header_titles[f"sumValue_{hour}_{hour+1}"] = ''
            header_titles[f"valueCount_{hour}_{hour+1}"] = ''
        header = [
            'id',
            'date',
            'stayingUpLateBed',
            'stayingUpLateWake'
        ] + list(header_titles.keys())
    else:
        header = [
            'id',
            'date',
            'stayingUpLateBed',
            'stayingUpLateWake',
            'valueCount',
            'sumValue'
        ]
    with open("all_data/2d_clustering_step_data.csv", mode='a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    for i, file_name in enumerate(file_names):
        if (file_name[0] != "."):
            # print(file_name)

            # CSVファイルを読み込む
            df = pd.read_csv(mode["step"]["metadata"]["csv_file_path"].replace(
                "{ID_HERE}", f"{file_name}"), dtype={"sourceVersion": str, "device": str}, low_memory=False)

            # 指定の日付範囲でフィルタリング
            df = df[(df["startDate"] >= mode["time"]["start_date"])
                    & (df["endDate"] <= mode["time"]["end_date"])]

            # "startDate" と "endDate" の列を datetime 型に変換
            df['startDate'] = pd.to_datetime(df['startDate'])
            df['endDate'] = pd.to_datetime(df['endDate'])

            # iPhoneのデータのみを抽出
            df = df[df["device"].str.contains("name:iPhone")]

            # 被験者個人の3ヶ月の歩数単体を格納
            allStep_data.append(df["value"])
            allStep_startDate.append(df["startDate"])
            allStep_endDate.append(df["endDate"])

            allStep_name.append(file_name[:3].replace("_", ""))

            # sys.exit()

            # 日毎にデータの数と歩数の合計を計算してデータに格納
            print(file_name[:3])

            # idごとのデータを抽出
            go_out_label = all_go_out_label[all_go_out_label["id"] == file_name[:3].replace(
                "_", "")]

            with open("all_data/2d_clustering_step_data.csv", mode='a+', newline='') as file:
                writer = csv.writer(file)

                # writer.writerow(["id", "date", "sumValue", "valueCount"])
                for i, date in enumerate(unique_dates):
                    if (time_list == "statistics"):
                        if (date.weekday() == 5 or (date.weekday() == 6)):
                            # 土日
                            start_time = holiday_time[0]
                            end_time = holiday_time[1]
                            staying_up_late_end_time = holiday_time[3]
                        else:
                            # 平日
                            start_time = weekday_time[0]
                            end_time = weekday_time[1]
                            staying_up_late_end_time = weekday_time[3]
                    else:
                        start_time = f"{time_list[0]}:00"
                        end_time = f"{time_list[1]}:00"
                        staying_up_late_end_time = f"{time_list[2]}:00"

                    # 文字列を時間に変換
                    start_time = pd.to_datetime(start_time)
                    end_time = pd.to_datetime(end_time)
                    staying_up_late_end_time = pd.to_datetime(
                        staying_up_late_end_time)
                    # start_time = pd.to_datetime("02:00:00")
                    # end_time = pd.to_datetime("05:00:00")

                    # ここの時間を(2,3時　3,4時　4.5時)と2,5時
                    # 指定した時間範囲の1時間ごとの歩数合計と歩数観測回数を抽出
                    if (time_list != "statistics"):
                        step_sum_count = {}
                        for hour in range(start, end):

                            start_time_v = pd.to_datetime(f"{hour}:00")
                            end_time_v = pd.to_datetime(f"{hour+1}:00")
                            # print(start_time_v, end_time_v)

                            # 時間範囲を指定
                            range_df = df[(
                                df["startDate"].dt.time >= start_time_v.time()) & (df["startDate"].dt.time <= end_time_v.time())]
                            step_sum_count[f"sumValue_{hour}_{hour+1}"] = range_df[range_df['startDate'].dt.date == date]['value'].sum(
                            )
                            step_sum_count[f"valueCount_{hour}_{hour+1}"] = range_df[
                                range_df['startDate'].dt.date == date].shape[0]
                    else:
                        range_df = df[(
                            df["startDate"].dt.time >= start_time.time()) & (df["startDate"].dt.time <= end_time.time())]
                        step_sum_count = {
                            "sumValue": range_df[range_df['startDate'].dt.date == date]['value'].sum(),
                            "valueCount": range_df[range_df['startDate'].dt.date == date].shape[0]
                        }

                    # print(step_sum_count)
                    # print("---")
                    # sys.exit()

                    # 最初に指定した時間から1時間のみのデータを抽出(保存用ではない)
                    df_clustering = df[(df["startDate"].dt.time >= start_time.time())
                                       & (df["startDate"].dt.time <= staying_up_late_end_time.time())]

                    # 歩数の合計
                    # sum_step = df_clustering[df_clustering['startDate'].dt.date ==
                    #                          date]['value'].sum()

                    # データの数
                    data_count = df_clustering[df_clustering['startDate'].dt.date == date].shape[0]

                    # 3~4時からまでの中にデータがなければ夜更かし疑惑がある．
                    # 21時(5%の時刻)まで睡眠時間を推定する

                    # 夜更かしを検知した(3~4時にステップあり)の場合の推定睡眠時刻を格納する変数TODO:これ関係なしに全て見る必要があるかも

                    # データがない場合はFalseを格納
                    staying_up_late_bed = False
                    staying_up_late_wake = False

                    time_interval = 0
                    staying_up_late = []

                    if (data_count > 0):

                        staying_up_late_bed = True
                        staying_up_late_wake = True

                        # print("就寝時刻を推定する時のみ")
                        # 右側を辿ってステップの間隔が最も大きいものを睡眠時間とする
                        df_stayingUpLate = df[(df["startDate"].dt.time >= start_time.time()) & (
                            df["endDate"].dt.time <= staying_up_late_end_time.time())]

                        date_data = df_stayingUpLate[df_stayingUpLate['startDate'].dt.date == date]
                        print(f"データあり{file_name[:3].replace("_", "")}_{date}")

                        # 前のendDateを格納数する変数
                        prev_end_time = pd.to_datetime(start_time)
                        # 一行目を取得
                        # prev_end_time = pd.to_datetime(
                        #     date_data["startDate"].iloc[0]).time()
                        tmp_estimate_sleep_time = pd.to_datetime(
                            "00:00:00").time()
                        tmp_bed_wake_time = []
                        # last_update = []
                        # sys.exit()
                        for i, row in date_data.iterrows():
                            # print(row["startDate"], row["endDate"])
                            time_interval = subtract_time(f"{row["startDate"].hour}:{row["startDate"].minute}:00", f"{prev_end_time.hour}:{prev_end_time.minute}:00")

                            estimate_sleep_time = pd.to_datetime(
                                time_interval).time()

                            print(estimate_sleep_time,  f"{prev_end_time.hour}:{prev_end_time.minute}", f"{row["startDate"].hour}:{row["startDate"].minute}")

                            # print(
                            #     go_out_label[go_out_label['endDate'] == pd.to_datetime(prev_end_time)]['1dClusteringLabel'])
                            if (((go_out_label[go_out_label['endDate'] == pd.to_datetime(prev_end_time)]['1dClusteringLabel']).values == 1) and (i > 0)):
                                print("外出検知")
                                # print(
                                #     go_out_label[go_out_label['endDate'] == pd.to_datetime(prev_end_time)])
                                break

                            if (tmp_estimate_sleep_time < estimate_sleep_time):
                                print("更新")
                                # print(tmp_estimate_sleep_time,
                                #       estimate_sleep_time)
                                # last_update.append(estimate_sleep_time)
                                tmp_estimate_sleep_time = estimate_sleep_time
                                # rowの時刻が1dClusteringLabel=1(外出検知)の場合，以下は適応せずにbreakする．(直前のtmp_bed_wake_timeが推定就寝時刻となる)
                                # go_out_labelから取得した

                                tmp_bed_wake_time = [f"{prev_end_time.hour}:{prev_end_time.minute}", f"{row["startDate"].hour}:{row["startDate"].minute}"]

                            prev_end_time = row["endDate"]

                        # print(
                        #     f"結果{tmp_estimate_sleep_time},{tmp_bed_wake_time}")
                        # print(f"二番目：{last_update}")
                        staying_up_late = [
                            tmp_estimate_sleep_time] + tmp_bed_wake_time
                    print(staying_up_late)
                    # sys.exit()

                    if (len(staying_up_late) > 1):
                        staying_up_late_bed = staying_up_late[1]
                        staying_up_late_wake = staying_up_late[2]
                        # staying_up_late_bed_2 = "二番目に大きい間隔の就寝時刻"
                        # staying_up_late_wake_2 = "二番目に大きい間隔の就寝時刻"
                    else:
                        staying_up_late_bed = False
                        staying_up_late_wake = False
                        # staying_up_late_bed_2 = False
                        # staying_up_late_wake_2 = False

                    # これらをcsvに書き込む

                    # step_sum_countの数だけ繰り返して格納したい
                        # 設定された変数を表示
                    # for name, value in step_sum_count.items():
                    #     print(f"{name}: {value}")

                    row = [
                        file_name[:3].replace("_", ""),
                        date,
                        staying_up_late_bed,
                        staying_up_late_wake,
                        # staying_up_late_bed_2,
                        # staying_up_late_wake_2,
                    ] + list(step_sum_count.values())
                    writer.writerow(row)

    # print(allStep_data)
    # print(allStep_name)
    allStep_combined = pd.concat(allStep_data, ignore_index=True)
    allStart_combined = pd.concat(allStep_startDate, ignore_index=True)
    allEnd_combined = pd.concat(allStep_endDate, ignore_index=True)

    # print(allStep_combined)
    y_data = []
    id_data = []
    for i, df in enumerate(allStep_data):
        y_data.extend([i] * len(df))
        id_data.extend([allStep_name[i]] * len(df))
    combined_df = pd.DataFrame(
        {'id': id_data, 'startDate': allStart_combined, 'endDate': allEnd_combined,
         'value': allStep_combined, 'label': y_data})
    print("---combined_df---")
    print(combined_df)

    # allStep_combined = pd.concat(allStep_data, ignore_index=True)
    # print(allStep_combined)
    # print("結果ｘ")
    # print(len(x_data))
    # print("結果y-")
    # print(y_data)

    # 被験者個人の3ヶ月の歩数単体(観測されたステップをそのまま使う)で3値クラスタリングをする．
    allStep_1d_kmeans = KMeans(n_clusters=3, random_state=2).fit(
        combined_df.iloc[:, -2:])
    print("---allStep_1d_kmeans---")
    print(allStep_1d_kmeans.labels_)
    print(allStep_1d_kmeans.cluster_centers_)

    plt.figure(figsize=(6, 6))
    plt.scatter(combined_df.iloc[:, 3], combined_df.iloc[:, 0],
                c=allStep_1d_kmeans.labels_, s=50)
    plt.xlabel("value")
    plt.yticks(ticks=range(len(allStep_name)), labels=allStep_name)
    plt.savefig("all_data/allStep_clustering.png")

    # 外出検知でallStep_1d_kmeansを使うため，このタイミングでリセット
    with open("all_data/1d_clustering_step_data.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'startDate', 'endDate',
                        'value', 'label', '1dClusteringLabel'])

    # ラベルをcsvファイルに追加
    combined_df["1dClusteringLabel"] = allStep_1d_kmeans.labels_
    combined_df.to_csv("all_data/1d_clustering_step_data.csv", index=False)

    # データを読み込んでkmeansを実行
    df_step = pd.read_csv(
        "all_data/2d_clustering_step_data.csv", low_memory=False)

    # 2d_kmeansの実行
    model_2d_kmeans = KMeans(n_clusters=4, random_state=2).fit(
        df_step.iloc[:, 4:], df_step.iloc[:, 5:])
    # 1d_kmeansの実行(1dを強引に2dに)
    sumValue_1d_kmeans = KMeans(n_clusters=4, random_state=2).fit(
        df_step.iloc[:, 4].values.reshape(-1, 1))
    valueCount_1d_kmeans = KMeans(n_clusters=4, random_state=2).fit(
        df_step.iloc[:, 5].values.reshape(-1, 1))
    # df_stepを読み込んで，sumV

    print("---2d_kmeans---")
    print(model_2d_kmeans.labels_)  # 0 or 1でラベルずけ
    print(model_2d_kmeans.cluster_centers_)  # クラスターの中心
    print("---sumValue_1d_kmeans---")
    print(sumValue_1d_kmeans.labels_)  # 0 or 1でラベルずけ
    print(sumValue_1d_kmeans.cluster_centers_)  # クラスターの中心
    print("---valueCount_1d_kmeans---")
    print(valueCount_1d_kmeans.labels_)  # 0 or 1でラベルずけ
    print(valueCount_1d_kmeans.cluster_centers_)  # クラスターの中心

    # クラスタリングのラベルをファイルに格納

    # for pass_name in clustering_label_pass:
    #     file = open(f"all_data/{pass_name}.txt", "w")
    #     for d in (model_2d_kmeans.labels_):
    #         file.write(f"{d} ")
    #     file.close()

    # 各ラベルを画像に出力

    plt.figure(figsize=(6, 6))
    plt.scatter(df_step.iloc[:, 4], df_step.iloc[:, 5],
                c=model_2d_kmeans.labels_, s=50)
    plt.xlabel(df_step.columns[4])
    plt.ylabel(df_step.columns[5])
    plt.savefig(f"all_data/{clustering_label_pass[0]}.png")

    plt.figure(figsize=(6, 4))
    plt.scatter(df_step.iloc[:, 4].values.reshape(-1, 1),
                np.zeros_like(df_step.iloc[:, 4].values.reshape(-1, 1)),
                c=sumValue_1d_kmeans.labels_, s=50)
    plt.xlabel(df_step.columns[4])
    plt.savefig(f"all_data/{clustering_label_pass[1]}.png")

    plt.figure(figsize=(6, 4))
    plt.scatter(df_step.iloc[:, 5].values.reshape(-1, 1),
                np.zeros_like(df_step.iloc[:, 5].values.reshape(-1, 1)),
                c=valueCount_1d_kmeans.labels_, s=50)
    plt.xlabel(df_step.columns[5])
    plt.savefig(f"all_data/{clustering_label_pass[2]}.png")

    # 各ラベルをcsvに追加

    df_step["2dClusteringLabel"] = model_2d_kmeans.labels_
    df_step["sumValueClusteringLabel"] = sumValue_1d_kmeans.labels_
    df_step["valueCountClusteringLabel"] = valueCount_1d_kmeans.labels_

    df_step.to_csv("all_data/2d_clustering_step_data.csv", index=False)


# csvファイルを初期化


def resetData():
    with open("all_data/2d_clustering_step_data.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(["id", "date", "stayingUpLateBed", "stayingUpLateWake",
        #                 # "sumValue", "valueCount"
        #                  ])
        # writer.writerow([])

    for pass_name in clustering_label_pass:
        file = open(f"all_data/{pass_name}.txt", "w")
        file.close()

    # with open("all_data/1d_clustering_step_data.csv", mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['id', 'startDate', 'endDate',
    #                     'value', 'label', '1dClusteringLabel'])
