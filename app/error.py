# 誤差，評価実行ファイル

import sys
from src.module.evaluation_and_verification import allEvaluationAndVerification, calculateError, dataReset
from src.module.all_output import dataCategorization
from src.module.time_function import shift_time
[function, mode, survey_id] = sys.argv

# 質問リスト
survey_list = ["survey_0", "survey_1", "survey_2",
               "survey_3", "survey_4", "survey_5", "survey_6", "composite", "individual"]

if (mode == "error"):

    # 全体の結果を用いた精度の確認をする
    if (survey_id in survey_list):
        allEvaluationAndVerification(survey_id)
        # 全体の結果を用いた起床時刻と就寝時刻の誤差の計算
        calculateError(survey_id)
    else:
        allEvaluationAndVerification("")
        calculateError("")

    # 回答によるカテゴリー分け
    # dataCategorization()


elif (mode == "reset"):

    # データのリセット
    dataReset()
