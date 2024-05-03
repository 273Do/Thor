# 誤差，評価実行ファイル

import sys
from src.module.evaluation_and_verification import all_evaluation_and_verification, calculate_error, data_reset

[function, mode] = sys.argv

if (mode == "error"):

    # 全体の結果を用いた精度の確認をする
    all_evaluation_and_verification()

    # 全体の結果を用いた起床時刻と就寝時刻の誤差の計算
    calculate_error()

elif (mode == "reset"):

    # データのリセット
    data_reset()
