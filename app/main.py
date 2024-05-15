# 実行ファイル

# ライブラリインポート
import json
import sys
import pandas as pd
from src.visualization import dataVisualization
from src.estimate_sleep_from_step import estimateSleepFromStep_Around, estimateSleepFromStep_Median
from src.module.time_function import ConvertToH, add_time

# コマンドライン引数を受け取って処理を行う
# [function, id, bed, wake, survey_id] = sys.argv
# print(f"id:{id}, bed:{bed}, wake:{wake}")

# 数字四桁である場合は，0200->2，1030->10.5，2400->0に変換する
# エラーハンドリング
# test


# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 質問リスト
survey_list = ["survey_0", "survey_1", "survey_2",
               "survey_3", "survey_4", "survey_5", "survey_6"]
# 質問回答データ
survey_df = pd.read_csv(
    "extraction_data/z_all_output/all_preliminary_data.csv")
# 回答ごとの間時間の平均をまとめたオブジェクト
json_open = open('extraction_data/z_all_output/data_categorization.json', 'r')
survey_average_time = json.load(json_open)

# 各モード共通
# 睡眠と歩数の可視化(初期のみ実行)
dataVisualization(mode["sleep"], [id, bed, wake])

dataVisualization(mode["step"], [id, bed, wake])
sys.exit()

# 通常モード
if (survey_id == "normal"):

    # 回答してもらった時刻をもとに精査する方法
    estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [
        [ConvertToH(bed), ConvertToH(wake)], [2, 3]], survey_id, [id, bed, wake])

    # nhkの調査をもとに精査する方法
    estimateSleepFromStep_Median([mode["estimate_sleep_from_step"], "percent"], [
        [94, 4], [94, 4]], survey_id, [id, bed, wake])

elif (survey_id in survey_list):

    print(f"survey_id:{survey_id}")

    # idをもとに，survey_idに対応する時刻を取得
    # subjects_answers = survey_df.at[id, survey_id]
    # 被験者の質問に対する回答を取得
    subjects_answers = survey_df[survey_df["id"] == id][survey_id].values[0]

    # 回答ごとの間時間の平均を質問と回答をもとに取得する

    print(subjects_answers)

    corr = survey_average_time[survey_id][subjects_answers]
    print(corr)

    # 質問と補正する時刻をまとめる
    if ((survey_id == "survey_1") or (survey_id == "survey_2") or (survey_id == "survey_3")):
        correction = [survey_id, corr, None]
    elif ((survey_id == "survey_4") or (survey_id == "survey_5") or (survey_id == "survey_6")):
        correction = [survey_id, None, corr]
    else:
        correction = [survey_id] + corr
    print(correction)

    # 回答してもらった時刻をもとに精査する方法
    # corr_bed，corr_wakeには補正する時間を入力
    estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [
        [ConvertToH(bed), ConvertToH(wake)], [2, 3]], correction, [id, bed, wake])

    # nhkの調査をもとに精査する方法
    # estimateSleepFromStep_Median([mode["estimate_sleep_from_step"], "percent"], [
    #     [94, 4], [94, 4]], mode_designation, [id, bed, wake])

elif (survey_id == "composite"):
    # アンケートの結果が最も良かったものを就寝時刻と起床時刻を選択
    # print("composite")

    correction = [survey_id]
    most_survey_id = ["survey_0", "survey_6"]

    for i, survey_id in enumerate(most_survey_id):
        subjects_answers = survey_df[survey_df["id"]
                                     == id][survey_id].values[0]
        if i == 0:
            correction.append(
                survey_average_time[survey_id][subjects_answers][1])
        else:
            correction.append(
                survey_average_time[survey_id][subjects_answers])

    # print(correction)
    # sys.exit()
    estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [
        [ConvertToH(bed), ConvertToH(wake)], [2, 3]], correction, [id, bed, wake])

else:
    print("適切なsurvey_idを入力してください")
    sys.exit()
