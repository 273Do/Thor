import json
import numpy as np
import pandas as pd

# 推定アルゴリズムに必要なデータフレームなどの設定
def dataFrameSettings(mode):
  
    # 時間の設定を読み込む
    json_open = open('./src/settings.json', 'r')
    time = json.load(json_open)
    
    # CSVファイルを読み込む
    df = pd.read_csv(mode["metadata"]["csv_file_path"], dtype={"sourceVersion": str, "device": str}, low_memory=False)
    
    # 指定の日付範囲でフィルタリング
    df = df[(df["startDate"] >= time["time"]["start_date"]) & (df["endDate"] <= time["time"]["end_date"])]
    
    # "startDate" と "endDate" の列を datetime 型に変換
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    
    # 抽出対象を指定してフィルタリング
    df = df[df["device"].str.contains("name:iPhone")]
    
    # ヒートマップ用のデータを初期化
    unique_dates = df['startDate'].dt.date.unique().tolist()
    heatmap_data = np.zeros((len(unique_dates), 288))  # 288は24時間 x 60分 / 5分刻み
    return df, unique_dates, heatmap_data