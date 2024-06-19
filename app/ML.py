import pandas as pd
import sys
from src.module.clustering import clustering, resetData
from src.module.ML.svm_cross_validation_dump import svm_cross_validation, svm_dump
from src.module.ML.random_forest_cross_validation import random_forest_cross_validation, balanced_random_forest_cross_validation

# 機械学習などの実行

# データのリセット
resetData()

# 手動で指定する場合([3, 4, 21]3~4時の歩数/睡眠時間の推定, 21時まで精査)
clustering([3, 12, 21])
# clustering("statistics")  # 統計を使う場合(94% -> 4%)

sys.exit()

# クロスバリデーションの実行

# csvファイルを読み込む
sleep_label_df = pd.read_csv(
    "all_data/actual_sleep_label.csv", low_memory=False)
clustering_df = pd.read_csv(
    "all_data/2d_clustering_step_data.csv", low_memory=False)

sleep_label_df = sleep_label_df.sort_values(
    by=['id', 'date'], key=lambda col: col.str.lower())
clustering_df = clustering_df.sort_values(
    by=['id', 'date'], key=lambda col: col.str.lower())

print(sleep_label_df)

# MEMO: sleep_labelが0の行を抜き出す
# sleep_label_df = sleep_label_df[sleep_label_df["sleep_label"] == 0]

# sleep_label_dfのidと日付をセットにしたリストを作成
id_date_set = set(zip(sleep_label_df['id'], sleep_label_df['date']))

# df_2をフィルタリング
filtered_df = clustering_df[clustering_df.apply(lambda row: (
    row['id'], row['date']) in id_date_set, axis=1)]


# # df_2のidの順番に従ってdf_1を並び替える
# ordered_ids = sleep_label_df['id'].unique()
# filtered_df['id'] = pd.Categorical(
#     filtered_df['id'], categories=ordered_ids, ordered=True)
# filtered_sorted_df = filtered_df.sort_values('id')

# # 結果を表示
# print(sleep_label_df)
# print(filtered_df)

# sleep_label_df.to_csv("all_data/test_sleep_label_df.csv", index=False)
# filtered_df.to_csv("all_data/test_filtered_df.csv", index=False)

# 特徴量とラベルを分ける
filtered_columns = [col for col in filtered_df.columns if col.startswith(
    'sumValue_') or col.startswith('valueCount_')]

# 'sumValue_' と 'valueCount_' が含まれる列を動的に抜き出す
X = filtered_df[filtered_columns + ['habit']]

# sleep_labelが0のdateとidを取得
# sleep_zero_ids = sleep_label_df[sleep_label_df['sleep_label'] == 0][[
#     'id', 'date']]
# print(sleep_zero_ids)

# # sleep_zero_idを満たす行だけを抜き出す
# X = filtered_df[filtered_df['habit'] == 0][filtered_columns + ['habit']]
# X = filtered_df.merge(sleep_zero_ids, on=['date', 'id'])[
#     filtered_columns + ['habit']]

# sleep_labelが0の行を抜き出す
# y = sleep_label_df[sleep_label_df['sleep_label'] == 0]['sleep_label']
# print(len(y))
# print(len(X))

# X = filtered_df[['sumValue', 'valueCount']]  # (歩数の合計とデータの数)
y = sleep_label_df['sleep_label']  # 正解データにおいて就寝時刻が3時以降のときとそうでない時の1,0で分けたやつ

groups = sleep_label_df['id']
print(filtered_df)
print(sleep_label_df)

# print(X.dtypes)
# print(y)


# svm_cross_validation(X, y, groups)

# svm_dump(X, y)

# random_forest_cross_validation(X, y, groups)
# balanced_random_forest_cross_validation(X, y, groups)
