import pandas as pd

# 日付とwatchデバイス名
yyyymmdd = "2023-11-14"
device_name = "irwAW"

# CSVファイルのパス
csv_file_path = "app/data/SleepAnalysis.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

# "creationDate"列を日付型に変換
df["creationDate"] = pd.to_datetime(df["creationDate"])

# 2023-11-14以降のデータをフィルタリング
filtered_df = df[(df["creationDate"] >= yyyymmdd) & (df["sourceName"] == device_name) & (df["value"] == "HKCategoryValueSleepAnalysisInBed")]


# 出力ファイルのパス
output_csv_path = "./app/extraction_data/extraction_sleeptime.csv"

# フィルタリングされたデータを別のCSVファイルに出力
filtered_df.to_csv(output_csv_path, index=False)

# 結果を表示
# print(filtered_df)