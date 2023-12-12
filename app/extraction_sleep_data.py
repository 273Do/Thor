import pandas as pd

# CSVファイルのパス
csv_file_path = "app/data/SleepAnalysis.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

# "creationDate"列を日付型に変換
df["creationDate"] = pd.to_datetime(df["creationDate"])

# 2023-11-14以降のデータをフィルタリング
filtered_df = df[(df["creationDate"] >= "2023-11-14") & (df["sourceName"] == "irwAW") & (df["value"] == "HKCategoryValueSleepAnalysisInBed")]


# 出力ファイルのパス
output_csv_path = "./app/extraction_data/extraction_sleeptime.csv"

# フィルタリングされたデータを別のCSVファイルに出力
filtered_df.to_csv(output_csv_path, index=False)

# 結果を表示
# print(filtered_df)