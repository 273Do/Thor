# 実行ファイル
import json
from src.visualization import data_visualization

# モードの設定ファイルを読み込む
json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

# 実行
data_visualization(mode["sleep"], "test")
data_visualization(mode["step"], "sleepTest3",)

# 推定するアルゴリズムの関数を実行