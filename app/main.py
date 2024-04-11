# 実行ファイル
import json
from src.visualization import dataVisualization
from src.estimate_sleep_from_step import estimateSleepFromStep_Around, estimateSleepFromStep_Median
from src.module.calculate_error import calculate_error_mse, calculate_error_mae
import numpy as np
# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 被験者ID
id = "id"

# 実行
# dataVisualization(mode["sleep"], id)
# dataVisualization(mode["step"], id)

# estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [[2, 10.5], [2, 3]], 24, "new")
# estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [[2, 10.5], [2, 3]], 24, "test")
# estimateSleepFromStep_Around(mode["estimate_sleep_from_step"], [[2, 10.5], [2, 3]], 24, "test")


# estimateSleepFromStep_Median([mode["estimate_sleep_from_step"], "percent"], [[94, 4], [94, 4]], 24, "test_median")#平日中央，平日精査先，休日中央，休日精査先

# y_trueが真の値，y_predが予測値
true_array_pass = "./extraction_data/true_sleep_data.txt"
pred_array_pass = "./extraction_data/pred_sleep_data(Around).txt"

calculate_error_mse(true_array_pass, pred_array_pass)
calculate_error_mae(true_array_pass, pred_array_pass)