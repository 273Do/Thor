import urllib.request
import csv
import os
import json
import itertools
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from set_reference_time import setReferenceTime

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


def clustering():

    # dataフォルダの中のディレクトリ名を全て取得
    file_names = os.listdir('./data/')

    # モードの設定ファイルを読み込む
    json_open = open('./src/settings.json', 'r')
    mode = json.load(json_open)

    # 精査する日付の範囲のリスト
    unique_dates = pd.date_range(start=mode["time"]["start_date"], end=datetime.strptime(
        mode["time"]["end_date"], "%Y-%m-%d") - timedelta(days=1)).date
    # print(unique_dates)

    # 統計データによる精査範囲の時間を取得
    weekday_time, holiday_time = setReferenceTime([94, 4], [94, 4])
    # print(weekday_time, holiday_time)
    print(f"weekday_time:{weekday_time}")
    print(f"holiday_time:{holiday_time}")
    # =>['3:00', '4:15', '12:00', '21:00'] ['3:00', '4:45', '12:45', '20:45']

    # その中のstepデータを範囲指定して取得
    for file_name in file_names:
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

            # 日毎にデータの数と歩数の合計を計算してデータに格納
            # print(file_name[:3])
            with open("all_data/2d_clustering_step_data.csv", mode='a+', newline='') as file:
                writer = csv.writer(file)
                # writer.writerow(["id", "date", "sumValue", "valueCount"])
                for i, date in enumerate(unique_dates):
                    if (date.weekday() == 5 or (date.weekday() == 6)):
                        # 土日
                        start_time = holiday_time[0]
                        end_time = holiday_time[1]
                    else:
                        # 平日
                        start_time = weekday_time[0]
                        end_time = weekday_time[1]

                    # 文字列を時間に変換
                    start_time = pd.to_datetime(start_time)
                    end_time = pd.to_datetime(end_time)

                    # 指定した時間範囲のデータを抽出
                    df = df[(df["startDate"].dt.time >= start_time.time())
                            & (df["startDate"].dt.time <= end_time.time())]

                    # 歩数の合計
                    sum_step = df[df['startDate'].dt.date ==
                                  date]['value'].sum()

                    # データの数
                    data_count = df[df['startDate'].dt.date == date].shape[0]

                    # 3~4時からまでの中にデータがなければ夜更かし疑惑がある．
                    # 21時(5%%の時刻)まで睡眠時間を推定する

                    staying_up_late = False
                    if (data_count > 0):
                        staying_up_late = True
                    # print("就寝時刻を推定する時のみ")

                    # これらをcsvに書き込む

                    writer.writerow(
                        [
                            file_name[:3].replace("_", ""),
                            date,
                            staying_up_late,
                            sum_step,
                            data_count
                        ]
                    )

    # データを読み込んでkmeansを実行
    df_step = pd.read_csv(
        "all_data/2d_clustering_step_data.csv", low_memory=False)

    # 2d_kmeansの実行
    model_2d_kmeans = KMeans(n_clusters=3).fit(df_step.iloc[:, -2:])
    # 1d_kmeansの実行(1dを強引に2dに)
    sumValue_1d_kmeans = KMeans(n_clusters=3).fit(
        df_step.iloc[:, 3].values.reshape(-1, 1))
    valueCount_1d_kmeans = KMeans(n_clusters=3).fit(
        df_step.iloc[:, 4].values.reshape(-1, 1))

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

    for pass_name in clustering_label_pass:
        file = open(f"all_data/{pass_name}.txt", "w")
        for d in (model_2d_kmeans.labels_):
            file.write(f"{d} ")
        file.close()

    plt.figure(figsize=(6, 6))
    plt.scatter(df_step.iloc[:, 3], df_step.iloc[:, 4],
                c=model_2d_kmeans.labels_, s=50)
    plt.xlabel(df_step.columns[3])
    plt.ylabel(df_step.columns[4])
    plt.savefig(f"all_data/{clustering_label_pass[0]}.png")

    plt.figure(figsize=(6, 4))
    plt.scatter(df_step.iloc[:, 3].values.reshape(-1, 1),
                np.zeros_like(df_step.iloc[:, 3].values.reshape(-1, 1)),
                c=sumValue_1d_kmeans.labels_, s=50)
    plt.xlabel(df_step.columns[3])
    plt.savefig(f"all_data/{clustering_label_pass[1]}.png")

    plt.figure(figsize=(6, 4))
    plt.scatter(df_step.iloc[:, 4].values.reshape(-1, 1),
                np.zeros_like(df_step.iloc[:, 4].values.reshape(-1, 1)),
                c=valueCount_1d_kmeans.labels_, s=50)
    plt.xlabel(df_step.columns[4])
    plt.savefig(f"all_data/{clustering_label_pass[2]}.png")


# csvファイルを初期化


def resetData():
    with open("all_data/2d_clustering_step_data.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "date", "stayingUpLate",
                        "sumValue", "valueCount"])

    for pass_name in clustering_label_pass:
        file = open(f"all_data/{pass_name}.txt", "w")
        file.close()


# 実行

resetData()
clustering()
