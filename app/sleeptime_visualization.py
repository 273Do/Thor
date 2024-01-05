import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

# CSVファイルのパス
csv_file_path = "app/data/SleepAnalysis.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

# 日付とwatchデバイス名
start_yyyymmdd = "2023-12-01"
end_yyyymmdd = "2024-01-01"
# device_name = df["sourceName"][0]

# 2023-11-14以降のデータをフィルタリング
df = df[(df["creationDate"] >= start_yyyymmdd) & (df["creationDate"] <= end_yyyymmdd) & (df["sourceName"] == device_name) & (df["value"] == "HKCategoryValueSleepAnalysisInBed")]

# 'startDate' と 'endDate' の列を datetime 型に変換
df['startDate'] = pd.to_datetime(df['startDate'])
df['endDate'] = pd.to_datetime(df['endDate'])

# ヒートマップ用のデータを初期化
unique_dates = df['startDate'].dt.date.unique()
heatmap_data = np.zeros((len(unique_dates), 288))  # 288は24時間 x 60分 / 5分刻み

# 各行に対して、startDate から endDate の範囲を1に設定
for i, date in enumerate(unique_dates):
    date_data = df[df['startDate'].dt.date == date]
    for _, row in date_data.iterrows():
        start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
        end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
        heatmap_data[i, start_index:end_index + 1] = 1

# ヒートマップの描画
plt.imshow(heatmap_data, cmap=ListedColormap(['white', 'blue']), aspect='auto', interpolation='none')

# タイトル，軸の設定
plt.xlabel('Time (5-minute intervals)')
plt.ylabel('Date')
plt.title('Sleep Time Heatmap')
plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)

# x軸の目盛りを設定
time_labels = np.arange(0, 288, 6*12)  # 6時間ごとに目盛りを表示
plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])

# カラーバーを表示
cbar = plt.colorbar(ticks=[0, 1])
cbar.set_ticklabels(['No Sleep', 'Sleep'])
cbar.set_label('Sleep Status')


# グラフを保存
plt.savefig("app/extraction_data/sleep_heatmap_31.png")
