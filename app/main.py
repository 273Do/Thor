# 実行ファイル
import json
from src.visualization import dataVisualization
from src.estimate_sleep_from_step import estimateSleepFromStep_Around, estimateSleepFromStep_Median

# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 被験者ID
id = "id"

# 初期のみ実行
dataVisualization(mode["sleep"], id)
dataVisualization(mode["step"], id)

estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [[2, 10.5], [2, 3]], 24, "new")


estimateSleepFromStep_Median([mode["estimate_sleep_from_step"], "percent"], [[94, 4], [94, 4]], 24, "test_median")#平日中央，平日精査先，休日中央，休日精査先