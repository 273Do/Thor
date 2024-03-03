# 実行ファイル
import json
from src.visualization import dataVisualization
from src.estimate_sleep_from_step import estimateSleepFromStep

# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 実行

dataVisualization(mode["sleep"], "test")
dataVisualization(mode["step"], "test")
# estimateSleepFromStep(mode["estimate_sleep_from_step"], [2, 10.5, 2, 3], 15, "test")
estimateSleepFromStep(mode["estimate_sleep_from_step"], [0.5, 8.5, "-", "-"], 9, "test")


# estimateSleepFromStep(mode["estimate_sleep_from_step"], [2, 10.5, 2, 3], "test")