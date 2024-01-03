import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

# CSVファイルのパス
# csv_file_path = "app/extraction_data/extraction_sleepdata.csv"

csv_file_path = "app/data/SleepAnalysis.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

# 日付とwatchデバイス名
yyyymmdd = "2023-11-14"
device_name = df["sourceName"][0]
# device_name = "name"


print(device_name)

# 2023-11-14以降のデータをフィルタリング
df = df[(df["creationDate"] >= yyyymmdd) & (df["sourceName"] == device_name) & (df["value"] == "HKCategoryValueSleepAnalysisInBed")]

# 'startDate' と 'endDate' の列を datetime 型に変換
df['startDate'] = pd.to_datetime(df['startDate'])
df['endDate'] = pd.to_datetime(df['endDate'])

# データを日付ごとにまとめる
grouped_df = df.groupby(df['startDate'].dt.date).agg({'startDate': 'min', 'endDate': 'max'})

# ヒートマップ用のデータを初期化
heatmap_data = np.zeros((len(grouped_df), 288))  # 288は24時間 x 60分 / 5分刻み

# 各行に対して、startDate から endDate の範囲を1に設定
for i, (_, row) in enumerate(grouped_df.iterrows()):
    start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
    end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
    heatmap_data[i, start_index:end_index + 1] = 1

# ヒートマップの描画
plt.imshow(heatmap_data, cmap=ListedColormap(['white', 'blue']), aspect='auto', interpolation='none')

# タイトル，軸の設定
plt.xlabel('Time (5-minute intervals)')
plt.ylabel('Date')
plt.yticks(fontsize=8)
plt.title('Sleep Time Heatmap')

# x軸の目盛りを設定
time_labels = np.arange(0, 288, 6*12)  # 12時間ごとに目盛りを表示
plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])

# 日付を表示
date_labels = np.arange(len(grouped_df))
plt.yticks(date_labels, grouped_df['startDate'].dt.date)

# カラーバーを表示
cbar = plt.colorbar(ticks=[0, 1])
cbar.set_ticklabels(['No Sleep', 'Sleep'])
cbar.set_label('Sleep Status')

# グラフを保存
plt.savefig("app/extraction_data/sleep_heatmap_3.png")

# ヒートマップを作成
# heatmap = plt.imshow(data, cmap='viridis', interpolation='nearest')

# # カラーバーを追加
# plt.colorbar(heatmap)

# # 軸ラベルの設定
# plt.xlabel("time")
# plt.ylabel("day")


# 画像を保存
# plt.savefig("./app/extraction_data/heatmap.png")

# グラフを表示
# plt.show()
