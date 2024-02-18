import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

# CSVファイルのパス
csv_file_path = "data/StepCount.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path, dtype={"sourceVersion": str, "device": str}, low_memory=False)

# デバイス名が記述されたテキストファイルを読み込む
f = open('src/device_name.txt', 'r', encoding='UTF-8')
data = f.read()
print(data)


# 日付とwatchデバイス名
start_yyyymmdd = "2023-12-01"
end_yyyymmdd = "2024-01-01"
device_name = data

# 2023-11-14以降のデータをフィルタリング
df = df[(df["creationDate"] >= start_yyyymmdd) & (df["creationDate"] <= end_yyyymmdd) & (df["sourceName"] == device_name) ]

# 'startDate' と 'endDate' の列を datetime 型に変換
df['startDate'] = pd.to_datetime(df['startDate'])
df['endDate'] = pd.to_datetime(df['endDate'])

# ヒートマップ用のデータを初期化
unique_dates = df['startDate'].dt.date.unique()
heatmap_data = np.zeros((len(unique_dates), 288))  # 288は24時間 x 60分 / 5分刻み

def ConvertToHeatmapCompatible(time):
    return int(288 * time / 24)
    
    

bed_time_average = ConvertToHeatmapCompatible(2) # 02:00 24
wake_time_average = ConvertToHeatmapCompatible(10.5) # 10:30 126 
bed_time_threshold = ConvertToHeatmapCompatible(2) # 30分 6
wake_time_threshold = ConvertToHeatmapCompatible(3) # 30分 6




# 各行に対して、startDate から endDate の範囲を1に設定
for i, date in enumerate(unique_dates):
    date_data = df[df['startDate'].dt.date == date]
    print(date_data)
    set_bed_time = False
    set_wake_time = False
    estimate_index_array = [[],[]]
    for _, row in date_data.iterrows():
        start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
        end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
        # print(start_index,end_index)
        
        if((abs(end_index - bed_time_average) < bed_time_threshold)):
            estimate_index_array[0].append(end_index)
            set_bed_time = True
        elif(set_bed_time == False):
            estimate_index_array[0].append(bed_time_average)
        if((abs(start_index - wake_time_average) < wake_time_threshold)):
            estimate_index_array[1].append(start_index)
            set_wake_time = True
        elif(set_wake_time == False):
            estimate_index_array[1].append(wake_time_average)
    print(estimate_index_array)
    heatmap_data[i, max(estimate_index_array[0]):min(estimate_index_array[1]) + 1] = 1
        
    print("----day:",row['startDate'].day,"----")

# ヒートマップの描画
plt.imshow(heatmap_data, cmap=ListedColormap(['white', 'blue']), aspect='auto', interpolation='none')

# タイトル，軸の設定
plt.title('Estimate Sleep Heatmap')
plt.xlabel('Time (5-minute intervals)')
plt.ylabel('Date')
plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)

# x軸の目盛りを設定
time_labels = np.arange(0, 288, 6*12)  # 6時間ごとに目盛りを表示
plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])

# カラーバーを表示
cbar = plt.colorbar(ticks=[0, 1])
cbar.set_ticklabels(['No Sleep', 'Sleep'])
cbar.set_label('Estimate Sleep')

# グラフを保存
plt.savefig("extraction_data/estimation_sleep_heatmap.png")