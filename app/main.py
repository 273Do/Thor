# 実行ファイル
import json
from src.visualization import dataVisualization
from src.estimate_sleep_from_step import estimateSleepFromStep_Around, estimateSleepFromStep_Median

# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 被験者ID
id = "id"

# 実行
# dataVisualization(mode["sleep"], id)
# dataVisualization(mode["step"], id)

# estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [[2, 10.5], [2, 3]], 24, "test")
## estimateSleepFromStep(mode["estimate_sleep_from_step"], [[0.5, 8.5], [2, 2]], 24, id)

estimateSleepFromStep_Median([mode["estimate_sleep_from_step"], "percent"], [[93, 6], [93, 6]], 24, "test")#平日中央，平日精査先，休日中央，休日精査先