# 実行ファイル
import json
from src.visualization import data_visualization

json_open = open('./src/settings.json', 'r')
mode = json.load(json_open)

data_visualization(mode["sleep"])
data_visualization(mode["step"])