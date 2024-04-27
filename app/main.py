# 実行ファイル

# ライブラリインポート
import json
import sys
from src.visualization import dataVisualization
from src.estimate_sleep_from_step import estimateSleepFromStep_Around, estimateSleepFromStep_Median
from src.module.time_function import ConvertToH

# コマンドライン引数を受け取って処理を行う
[function, id, bed, wake] = sys.argv
# print(f"id:{id}, bed:{bed}, wake:{wake}")

# 数字四桁である場合は，0200->2，1030->10.5，2400->0に変換する
# エラーハンドリング

# test
# [id, bed, wake] = ["KY", "0200", "1030"]
# [id, bed, wake] = ["T08", "0030", "0830"]

# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 睡眠と歩数の可視化(初期のみ実行)
dataVisualization(mode["sleep"], [id, bed, wake])
dataVisualization(mode["step"], [id, bed, wake])

# 回答してもらった時刻をもとに精査する方法
estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [[ConvertToH(bed), ConvertToH(wake)], [2, 3]], 24, [id, bed, wake])


# nhkの調査をもとに精査する方法
estimateSleepFromStep_Median([mode["estimate_sleep_from_step"], "percent"], [[94, 4], [94, 4]], 24, [id, bed, wake])