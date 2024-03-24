# 実行ファイル
import json
from src.visualization import dataVisualization
from src.estimate_sleep_from_step import estimateSleepFromStep

# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 被験者ID
id = "id"

# 実行
# dataVisualization(mode["sleep"], id)
# dataVisualization(mode["step"], id)
estimateSleepFromStep(mode["around"], [2, 10.5, 2, 3], 24, "test")
# estimateSleepFromStep(mode["estimate_sleep_from_step"], [0.5, 8.5, 2, 2], 24, id)