import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from src.module.time_function import time_to_decimal
from datetime import datetime

# ヒートマップの描画


def drawHeatmap(method, mode, heatmap_data, data_info, calc_info, unique_dates, file_name, correction):
    if (type(correction) == list):
        answer = f"_{correction[0]}"
    else:
        answer = ""

    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成
    plt.imshow(heatmap_data, cmap=ListedColormap(
        ['#ffffff', '#08306b']), aspect='auto', interpolation='none')

    # タイトル，軸の設定
    # plt.title(f"{mode["heatmap"]["title"]}({method})")
    # plt.text(260, -1, f"bed time Avg:{time_specified_data[0]}, wake time Avg:{time_specified_data[1]}, \nbed time Thd:{"2" if time_specified_data[2] == "-" else time_specified_data[2]}, wake time Thd:{"2" if time_specified_data[3] == "-" else time_specified_data[3]}, \nstep observation threshold:{step_observation_threshold}", fontsize=7)
    plt.text(260, -1, data_info, fontsize=7)
    # plt.text(260, 34.4, f"MSE: {calc_error[0]}\nMAE: {calc_error[1]}", fontsize=7)
    plt.text(-52, 0.2, calc_info, fontsize=7)
    # 32or34.4
    plt.xlabel(mode["heatmap"]["x_label"])
    plt.ylabel(mode["heatmap"]["y_label"])
    # plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)
    plt.yticks(range(len(unique_dates)), [date.strftime(
        '%Y-%m-%d') for date in unique_dates], fontsize=8)

    # x軸の目盛りを設定
    time_labels = np.arange(0, 289, 6*12)  # 6時間ごとに目盛りを表示
    plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])

    # カラーバーを表示
    cbar = plt.colorbar(ticks=[0, 1])
    cbar.set_ticklabels(mode["color_bar"]["tick_labels"])
    cbar.set_label(mode["color_bar"]["label"])

    # グラフを保存
    plt.savefig(f"{mode["metadata"]["image_name"]}_{method}_{file_name}{answer}.png")

# 混同行列のヒートマップの描画


def confusionMatrixHeatmap(confusion_matrix, method, data_info, subject_data, correction):
    if (type(correction) == list):
        answer = f"_{correction[0]}"
    else:
        answer = ""

    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成

    plt.imshow(confusion_matrix, cmap='Blues', interpolation='nearest')

    # plt.title(f'Estimation Sleep ({method})')
    # plt.text(1.65, -0.55, data_info, fontsize=7)
    plt.colorbar(label='')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.xticks(ticks=[0, 1], labels=['Positive', 'Negative'])
    plt.yticks(ticks=[0, 1], labels=['Positive', 'Negative'])

    for i in range(2):
        for j in range(2):
            text_color = 'white' if confusion_matrix[i, j] >= 0.5 else 'black'
            plt.text(j, i, format(
                confusion_matrix[i, j], ".2f"), ha='center', va='center', color=text_color)

    plt.savefig(
        f'extraction_data/confusion_matrix_{method}_{subject_data[0]}{answer}.png')

# 正解データと推定データの比較のヒートマップの描画


def heatmapOfCompareTrueDataAndEstimatedData(actual_data, pred_data, pred_dates, time_average,  data_info, calc_info, method, subject_data, correction):
    if (type(correction) == list):
        answer = f"_{correction[0]}"
    else:
        answer = ""

    # データを区別するため2をかける
    actual_data = actual_data * 2

    unique_dates = []
    # 日付データを２回ずつループ
    for date in pred_dates:
        unique_dates.append(date)
        unique_dates.append("")

    # データの結合
    mix_data = np.array([])
    # print(actual_data[0].tolist())
    for i, date in enumerate(actual_data):
        mix_data = np.append(mix_data, actual_data[i])
        mix_data = np.append(mix_data, pred_data[i])

    mix_data = mix_data.reshape(-1, 288)

    # 休日かどうかを保持
    isHoliday = False
    if (method == "Around"):
        for j, _ in enumerate(unique_dates):
            mix_data[j, time_average[0]:time_average[0]+1] = 3
            mix_data[j, time_average[1]-1:time_average[1]] = 3
    else:
        for j, date in enumerate(unique_dates):
            if (date != ""):
                if ((datetime.strptime(date, "%Y-%m-%d").weekday() == 5 or (datetime.strptime(date, "%Y-%m-%d").weekday() == 6))):
                    isHoliday = True
                    mix_data[j, time_to_decimal(time_average[1][0]):time_to_decimal(
                        time_average[1][0])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[1][1])-1:time_to_decimal(time_average[1][1])] = 3
                    mix_data[j, time_to_decimal(time_average[1][2]):time_to_decimal(
                        time_average[1][2])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[1][3])-1:time_to_decimal(time_average[1][3])] = 3
                else:
                    isHoliday = False
                    mix_data[j, time_to_decimal(time_average[0][0]):time_to_decimal(
                        time_average[0][0])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[0][1])-1:time_to_decimal(time_average[0][1])] = 3
                    mix_data[j, time_to_decimal(time_average[0][2]):time_to_decimal(
                        time_average[0][2])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[0][3])-1:time_to_decimal(time_average[0][3])] = 3
            else:
                if (isHoliday == True):
                    mix_data[j, time_to_decimal(time_average[1][0]):time_to_decimal(
                        time_average[1][0])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[1][1])-1:time_to_decimal(time_average[1][1])] = 3
                    mix_data[j, time_to_decimal(time_average[1][2]):time_to_decimal(
                        time_average[1][2])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[1][3])-1:time_to_decimal(time_average[1][3])] = 3
                else:
                    mix_data[j, time_to_decimal(time_average[0][0]):time_to_decimal(
                        time_average[0][0])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[0][1])-1:time_to_decimal(time_average[0][1])] = 3
                    mix_data[j, time_to_decimal(time_average[0][2]):time_to_decimal(
                        time_average[0][2])+1] = 3
                    mix_data[j, time_to_decimal(
                        time_average[0][3])-1:time_to_decimal(time_average[0][3])] = 3

    # ヒートマップの描画
    plt.figure()  # 新しいFigureを作成
    plt.imshow(mix_data, cmap=ListedColormap(
        ['#ffffff', '#aacfe5', "#08306b", "#f172a3"]), aspect='auto', interpolation='none')

    # タイトル，軸の設定
    # plt.title(f"Compare({method})")
    # plt.text(260, -1, f"bed time Avg:{time_specified_data[0]}, wake time Avg:{time_specified_data[1]}, \nbed time Thd:{"2" if time_specified_data[2] == "-" else time_specified_data[2]}, wake time Thd:{"2" if time_specified_data[3] == "-" else time_specified_data[3]}, \nstep observation threshold:{step_observation_threshold}", fontsize=7)
    plt.text(260, -1.5, data_info, fontsize=7)
    # plt.text(260, 34.4, f"MSE: {calc_error[0]}\nMAE: {calc_error[1]}", fontsize=7)
    plt.text(-52, 0.2, calc_info, fontsize=7)
    # 32or34.4
    plt.xlabel("Time (5-minute intervals)")
    plt.ylabel("Data")
    # plt.yticks(range(len(unique_dates)), [date.strftime('%Y-%m-%d') for date in unique_dates], fontsize=8)
    plt.yticks(range(len(unique_dates)), [
               date for date in unique_dates], fontsize=8)

    # x軸の目盛りを設定
    time_labels = np.arange(0, 289, 6*12)  # 6時間ごとに目盛りを表示
    plt.xticks(time_labels, [f"{h//12}:{h%12*5:02d}" for h in time_labels])

    # カラーバーを表示
    cbar = plt.colorbar(ticks=[0, 1, 2, 3])
    cbar.set_ticklabels(
        ["No Sleep", "Sleep(pred)", "Sleep(actual)", "Answered Avg"])
    cbar.set_label("Sleep Status")

    # グラフを保存
    plt.savefig(
        f"extraction_data/compare_{method}_{subject_data[0]}{answer}.png")
