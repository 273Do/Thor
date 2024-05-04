# 誤差，評価実行ファイル

import sys
from src.module.evaluation_and_verification import allEvaluationAndVerification, calculateError, dataReset
from src.module.all_output import dataCategorization
from src.module.time_function import shift_time
[function, mode] = sys.argv

if (mode == "error"):

    # 全体の結果を用いた精度の確認をする
    # allEvaluationAndVerification()

    # # 全体の結果を用いた起床時刻と就寝時刻の誤差の計算
    # calculateError()

    # 回答によるかテーゴリー分け
    dataCategorization()
    # shift_time("23:06", "21:48")


elif (mode == "reset"):

    # データのリセット
    dataReset()
