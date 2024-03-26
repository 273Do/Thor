
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def drawHeatmap(method, mode, heatmap_data, data_info, unique_dates, file_name):
    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成
    plt.imshow(heatmap_data, cmap=ListedColormap(['white', 'blue']), aspect='auto', interpolation='none')

    # タイトル，軸の設定
    plt.title(mode["heatmap"]["title"] + " (" + method + ")")
    # plt.text(260, -1, f"bed time Avg:{time_specified_data[0]}, wake time Avg:{time_specified_data[1]}, \nbed time Thd:{"2" if time_specified_data[2] == "-" else time_specified_data[2]}, wake time Thd:{"2" if time_specified_data[3] == "-" else time_specified_data[3]}, \nstep observation threshold:{step_observation_threshold}", fontsize=7)
    plt.text(260, -1, data_info, fontsize=7)
    plt.xlabel(mode["heatmap"]["x_label"])
    plt.ylabel(mode["heatmap"]["y_label"])
    # plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)
    plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)
    
    # 以下から共通化可能
    # x軸の目盛りを設定
    time_labels = np.arange(0, 289, 6*12)  # 6時間ごとに目盛りを表示
    plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])
    
    # カラーバーを表示
    cbar = plt.colorbar(ticks=[0, 1])
    cbar.set_ticklabels(mode["color_bar"]["tick_labels"])
    cbar.set_label(mode["color_bar"]["label"])
    
    # グラフを保存
    plt.savefig(mode["metadata"]["image_name"] + "_" + method + "_" + file_name + ".png")
    # ---ここまで共通化--