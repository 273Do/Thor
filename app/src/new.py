import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

# CSVファイルのパス
csv_file_path = "data/StepCount.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path, dtype={"sourceVersion": str, "device": str}, low_memory=False)

# 日付とwatchデバイス名
start_yyyymmdd = "2023-12-01"
end_yyyymmdd = "2024-01-01"
device_name = "TSIPXIIIM"

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
bed_time_threshold = ConvertToHeatmapCompatible(1.5) # 30分 6
wake_time_threshold = ConvertToHeatmapCompatible(0.25) # 30分 6




# 各行に対して、startDate から endDate の範囲を1に設定
for i, date in enumerate(unique_dates):
    date_data = df[df['startDate'].dt.date == date]
    # print(date_data)
    set_bed_time = False
    set_wake_time = False
    for _, row in date_data.iterrows():
        start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
        end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
        print(start_index,end_index)
        if((abs(end_index - bed_time_average) < bed_time_threshold)):
            heatmap_data[i, start_index:end_index + 1] = 1
            set_bed_time = True
        elif(set_bed_time == False): heatmap_data[i, bed_time_average:bed_time_average + 1] = 1
        if((abs(start_index - wake_time_average) < wake_time_threshold)):
            heatmap_data[i, start_index:end_index + 1] = 1
            set_wake_time = True
        elif(set_wake_time == False): heatmap_data[i, wake_time_average:wake_time_average + 1] = 1
    # if(set_bed_time and set_wake_time):
            # heatmap_data[i, bed_time_average:wake_time_average + 1] = 1
        
    print("----day:",row['startDate'].day,"----")

# 繋げる場合
# grouped_df = df.groupby(df['startDate'].dt.date).agg({'startDate': 'min', 'endDate': 'max'})
# for i, (_, row) in enumerate(grouped_df.iterrows()):
#     start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
#     end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
#     heatmap_data[i, start_index:end_index + 1] = 1
#     print(start_index,end_index)
#     print("----day:",row['startDate'].day,"----")
#     # if(abs(start_index - bed_time_average) > bed_time_threshold):
#     #     start_index = bed_time_average
#     # elif(abs(start_index - wake_time_average) > wake_time_threshold):
#     #     end_index = wake_time_average
#     # if(abs(end_index - wake_time_average) > wake_time_threshold):
#     #     end_index = wake_time_average
#     heatmap_data[i, start_index:end_index + 1] = 1
#     # heatmap_data[i, sleep_time_average:wake_time_average] = 1

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
cbar.set_ticklabels(['No Step', 'Step'])
cbar.set_label('Measured Step')

# グラフを保存
plt.savefig("extraction_data/estimation_sleep_heatmap.png")