import pandas as pd

# 時間帯ごとに睡眠している確率を変数で指定．
# median_time_probability(%)，goal_probability(%)を指定すると，
# それに対応した時間bed_time_examine：[start, goal](h)，wake_time_examine：[start, goal](h)を返す．
# [[start, goal], [start, goal]](h)このような配列を平日と土日で返す．
def setReferenceTime(median_time_probability, edge_time_probability):
    weekday = [[], []]
    holiday = [[], []]
    
    # CSVファイルを読み込む
    df = pd.read_csv("src/module/nhk_investigation_data/sleep_data_weekday.csv", low_memory=False)
    
    print(df)
  