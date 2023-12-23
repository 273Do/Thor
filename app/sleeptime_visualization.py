import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ダミーデータを生成
data = np.random.rand(10, 10)  # 10x10のランダムなデータ

# # 日付とwatchデバイス名
# yyyymmdd = "2023-11-14"
# device_name = "irwAW"

# CSVファイルのパス
csv_file_path = "app/extraction_data/extraction_sleepdata.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

selected_columns = df[['startDate', 'endDate']]
print(selected_columns)




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
