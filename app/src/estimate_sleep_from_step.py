import json
import numpy as np
import pandas as pd
from src.module.data_frame_settings import dataFrameSettings
from src.module.draw_heatmap import drawHeatmap
from src.module.set_reference_time import setReferenceTime
    
# 時間をヒートマップの形式に対応するように変換する関数
ConvertToHeatmapCompatible = lambda time: int(288 * time / 24)

# 平均就寝時間と平均起床時間の前後を精査して，歩数から睡眠を推定する関数
def estimateSleepFromStep_Around(mode, time_specified_data, step_observation_threshold, file_name):
    
    # 推定に必要な設定
    data_frame_settings = dataFrameSettings(mode)
    [df, unique_dates, heatmap_data] = data_frame_settings
    #-------------------------------------------
    
    # 日を跨ぐかどうか
    is_cross_day = True
    
    # ステップ観測閾値が9~24の間であるかどうかを判断する必要があるか？
    
    if(12 < time_specified_data[0] <= 24):
        is_cross_day = False
    
    # それぞれの時刻をヒートマップの形式に対応するように変換
    bed_time_average = ConvertToHeatmapCompatible(time_specified_data[0])
    wake_time_average = ConvertToHeatmapCompatible(time_specified_data[1])
    bed_time_threshold = ConvertToHeatmapCompatible(2) if time_specified_data[2] == "-" else ConvertToHeatmapCompatible(time_specified_data[2])
    wake_time_threshold = ConvertToHeatmapCompatible(2) if time_specified_data[3] == "-" else ConvertToHeatmapCompatible(time_specified_data[3])
    
    # 推定するアルゴリズムを実装
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        set_bed_time = False
        set_wake_time = False
        is_skip = False
        end_tmp = 0
        estimate_index_array = [[], []]
        
        for _, row in date_data.iterrows():
            start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
            end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
            if(start_index - end_tmp > ConvertToHeatmapCompatible(step_observation_threshold)):#9_15
                is_skip = True
                # print(row["startDate"].strftime("%Y-%m-%d"), unique_dates[i])
                # unique_dates.remove(row["startDate"].strftime("%Y-%m-%d"))
                # 日にちを消す処理をしたい
                # delete_date_index.append(unique_dates[i])
                # del unique_dates[i]
                break
            else:
                is_skip = False
                if((abs(end_index - bed_time_average) < bed_time_threshold)):
                    estimate_index_array[0].append(end_index)
                    set_bed_time = True
                elif(set_bed_time == False):
                    estimate_index_array[0].append(bed_time_average)
                if((abs(start_index - wake_time_average) < wake_time_threshold)):
                    estimate_index_array[1].append(start_index)
                    set_wake_time = True
                elif(set_wake_time == False):
                    estimate_index_array[1].append(wake_time_average)
            end_tmp = end_index
          
        # 日をスキップしない場合はヒートマップ用のデータを更新  
        if(is_skip == False):
            # 平均就寝時間が24時を超えない場合とそうでない場合
            # 各行に対して、startDate から endDate の範囲を1に設定
            if(is_cross_day == False):
                heatmap_data[i, max(estimate_index_array[0]):288] = 1
                heatmap_data[i, 0:min(estimate_index_array[1])] = 1
            else:
                heatmap_data[i, max(estimate_index_array[0]):min(estimate_index_array[1])] = 1
    
    
    #-------------------------------------------            
    # ヒートマップの描画
    data_info = f"bed time Avg:{time_specified_data[0]}, wake time Avg:{time_specified_data[1]}, \nbed time Thd:{"2" if time_specified_data[2] == "-" else time_specified_data[2]}, wake time Thd:{"2" if time_specified_data[3] == "-" else time_specified_data[3]}, \nstep observation threshold:{step_observation_threshold}"
    drawHeatmap("Around", mode, heatmap_data, data_info, unique_dates, file_name)
    
    

# 平均就寝時間と平均起床時間の中央時刻の前後を精査して，歩数から睡眠を推定する関数
def estimateSleepFromStep_Median(mode, time_specified_data, step_observation_threshold, file_name):
    setReferenceTime(50, 50)
     # 推定に必要な設定
 
    data_frame_settings = dataFrameSettings(mode)
    [df, unique_dates, heatmap_data] = data_frame_settings
    #-------------------------------------------

    # 推定するアルゴリズムを実装
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        end_tmp = 0
        estimate_index_array = [[], []]
       
        
        for _, row in date_data.iterrows():
            start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
            end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
            if(start_index - end_tmp > ConvertToHeatmapCompatible(step_observation_threshold)):#9_15
                is_skip = True
                break
            else:
                break
                # 処理を実装