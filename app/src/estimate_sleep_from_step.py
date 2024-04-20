import pandas as pd
from src.module.data_frame_settings import dataFrameSettings
from src.module.draw_heatmap import drawHeatmap
from src.module.set_reference_time import setReferenceTime
from src.module.time_function import ConvertToHeatmapCompatible, ConvertToHHMM, time_to_decimal, add_time, subtract_time
from src.module.calculate_error import calculate_error
import itertools

# 正解データを格納したテキストファイルのパス
actual_data_pass = "./extraction_data/actual_sleep_data.txt"
pred_data_pass = ""

# 平均就寝時間と平均起床時間の前後を精査して，歩数から睡眠を推定する関数
def estimateSleepFromStep_Around(mode, time_specified_data, step_observation_threshold, subject_data):
    
    # 推定に必要な設定
    # 必要なデータをセット
    data_frame_settings = dataFrameSettings(mode, subject_data)
    [df, unique_dates, heatmap_data] = data_frame_settings
    #-------------------------------------------
    
    # 日を跨ぐかどうか
    is_cross_day = True
    
    # 前日のデータを格納する変数
    previous_day_data = []
    
    # ステップ観測閾値が9~24の間であるかどうかを判断する必要があるか？
    
    if(12 < time_specified_data[0][0] <= 24):
        is_cross_day = False
    
    # それぞれの時刻をヒートマップの形式に対応するように変換
    # bed_time_average = ConvertToHeatmapCompatible(time_specified_data[0][0])
    # wake_time_average = ConvertToHeatmapCompatible(time_specified_data[0][1])
    # bed_time_threshold = ConvertToHeatmapCompatible(2) if time_specified_data[1][0] == "-" else ConvertToHeatmapCompatible(time_specified_data[1][0])
    # wake_time_threshold = ConvertToHeatmapCompatible(2) if time_specified_data[1][1] == "-" else ConvertToHeatmapCompatible(time_specified_data[1][1])
    
    bed_time_average = ConvertToHHMM(time_specified_data[0][0])
    wake_time_average = ConvertToHHMM(time_specified_data[0][1])
    bed_time_threshold = ConvertToHHMM(2) if time_specified_data[1][0] == "-" else ConvertToHHMM(time_specified_data[1][0])
    wake_time_threshold = ConvertToHHMM(2) if time_specified_data[1][1] == "-" else ConvertToHHMM(time_specified_data[1][1])
  
    # それぞれの精査範囲の時刻を設定
    if(is_cross_day == True):
        bed_time_range = [subtract_time(bed_time_average, bed_time_threshold), add_time(bed_time_average, bed_time_threshold)]
        wake_time_range = [subtract_time(wake_time_average, wake_time_threshold), add_time(wake_time_average, wake_time_threshold)]
    else:
        bed_time_range = [subtract_time(bed_time_average, bed_time_threshold), "23:59:59"]# ConvertToHHMM(24 + time_specified_data[0][0] - time_specified_data[1][0])
        wake_time_range = [subtract_time(wake_time_average, wake_time_threshold), add_time(wake_time_average, wake_time_threshold)]
    print(bed_time_range, wake_time_range)
    
    # 推定するアルゴリズムを実装
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        set_bed_time = False
        set_wake_time = False
        is_skip = False
        end_tmp = 0
        # estimate_index_array = [[], []]
        estimate_index_array = []
        
              
        # if(len(previous_day_data) > 0):
        #     print(f"-----------------{date}")
            # print(previous_day_data["endDate"])
        
        # 閾値が時刻を超えて前日を遡る場合：一旦00:00から閾値までのデータを取得
        # MEMO: 前日を遡るように修正する必要がある
        if(time_specified_data[0][0] - time_specified_data[1][0] >= 0):
            bed_date_data = date_data[(date_data["endDate"].dt.time >= pd.to_datetime(bed_time_range[0], format='%H:%M:%S').time()) & (date_data["endDate"].dt.time <= pd.to_datetime(bed_time_range[1], format='%H:%M:%S').time())]
        else:
            # previous_time = 24 + time_specified_data[0][0] - time_specified_data[1][0]
            # print(bed_time_range[0])
            bed_date_data = date_data[(date_data["endDate"].dt.time >= pd.to_datetime('00:00:00', format='%H:%M:%S').time()) & (date_data["endDate"].dt.time <= pd.to_datetime(bed_time_range[1], format='%H:%M:%S').time())]
            # previous_date_data = previous_day_data[(date_data["endDate"].dt.time >= pd.to_datetime('00:00:00', format='%H:%M:%S').time()) & (date_data["endDate"].dt.time <= pd.to_datetime(bed_time_range[1], format='%H:%M:%S').time())]
        
        # 就寝時刻を推定
        if(len(bed_date_data) > 0):
            bed_time = int((bed_date_data['endDate'].max().hour * 60 + bed_date_data['endDate'].max().minute) / 5)
            estimate_index_array.append(bed_time)
        else:
            estimate_index_array.append(time_to_decimal(bed_time_average[:-3]))
        
        # 起床時刻を推定
        wake_date_data = date_data[(date_data["startDate"].dt.time >= pd.to_datetime(wake_time_range[0], format='%H:%M:%S').time()) & (date_data["startDate"].dt.time <= pd.to_datetime(wake_time_range[1], format='%H:%M:%S').time())]
        if(len(wake_date_data) > 0):
            wake_time = int((wake_date_data['startDate'].min().hour * 60 + wake_date_data['startDate'].min().minute) / 5)
            estimate_index_array.append(wake_time)
        else:
            estimate_index_array.append(time_to_decimal(wake_time_average[:-3]))
        # print(f"-----------------{date}")
        # print(estimate_index_array)
        
        # 中央時刻より前のデータがある場合
        # if(len(sleep_date_data) > 0):
        #     # 日毎のdfのendDateの最後の時間(最大値)を取得してヒートマップの形式に変換
        #     # end_indexが就寝時間
        #     bed_time = int((sleep_date_data['endDate'].max().hour * 60 + sleep_date_data['endDate'].max().minute) / 5)
        #     estimate_index_array.append(bed_time)
        #     print(bed_time)
        #     print(sleep_date_data["endDate"].max())
        # else:
        #     print("No data")
        
        #TODO:
        #ここfor文ではなくて，平均就寝時刻(起床時刻)の前後のデータをのみを取得して
        #date_data["startDate"].dt.time <= pd.to_datetime(set_bed_range[0], format='%H:%M').time()のように範囲を指定
        #その中のdfの最大値/最小値を取得してそれを就寝時刻(起床時刻)とする
        
        #ここからは前の実装---------
        # for _, row in date_data.iterrows():
        #     start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
        #     end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
        #     if(start_index - end_tmp > ConvertToHeatmapCompatible(step_observation_threshold)):#9_15
        #         is_skip = True
        #         # print(row["startDate"].strftime("%Y-%m-%d"), unique_dates[i])
        #         # unique_dates.remove(row["startDate"].strftime("%Y-%m-%d"))
        #         # 日にちを消す処理をしたい
        #         # delete_date_index.append(unique_dates[i])
        #         # del unique_dates[i]
        #         break
        #     else:
        #         is_skip = False
        #         if((abs(end_index - bed_time_average) < bed_time_threshold)):
        #             estimate_index_array[0].append(end_index)
        #             set_bed_time = True
        #         elif(set_bed_time == False):
        #             estimate_index_array[0].append(bed_time_average)
        #         if((abs(start_index - wake_time_average) < wake_time_threshold)):
        #             estimate_index_array[1].append(start_index)
        #             set_wake_time = True
        #         elif(set_wake_time == False):
        #             estimate_index_array[1].append(wake_time_average)
        #     end_tmp = end_index
        
        # print(previous_day_data["endDate"])
          
        # 日をスキップしない場合はヒートマップ用のデータを更新  
        if(is_skip == False):
            # 平均就寝時間が24時を超えない場合とそうでない場合
            # 各行に対して、startDate から endDate の範囲を1に設定
            if(is_cross_day == False):
           
                heatmap_data[i, estimate_index_array[0]:288] = 1
                heatmap_data[i, 0:estimate_index_array[1]] = 1
            else:
                if((time_specified_data[0][0] - time_specified_data[1][0] < 0) & (len(previous_day_data) > 0) & (i > 0)):
                    heatmap_data[i - 1, int((previous_day_data['endDate'].min().hour * 60 + previous_day_data['endDate'].min().minute) / 5):288] = 1
                    heatmap_data[i, 0:estimate_index_array[1]] = 1
                else:
                    heatmap_data[i, estimate_index_array[0]:estimate_index_array[1]] = 1
                
        previous_day_data = date_data[(date_data["endDate"].dt.time >= pd.to_datetime(bed_time_range[0], format='%H:%M:%S').time())]
    
    # ヒートマップデータをテキストファイルに出力(推定データ)
    pred_data_pass = "./extraction_data/pred_sleep_data(Around).txt"
    file = open(pred_data_pass, "w")
    for d in list(itertools.chain.from_iterable(heatmap_data)):
        file.write(f"{d} ")
    file.close()
    
    # 誤差の計算
    calc_error = calculate_error(actual_data_pass, pred_data_pass, "Around", subject_data)
    
    #-------------------------------------------            
    # ヒートマップの描画
    data_info = f"bed time Avg:{time_specified_data[0][0]}, wake time Avg:{time_specified_data[0][1]}, \nbed time Thd:{"2" if time_specified_data[1][0] == "-" else time_specified_data[1][0]}, wake time Thd:{"2" if time_specified_data[1][1] == "-" else time_specified_data[1][1]}, \nstep observation threshold:{step_observation_threshold}"
    # calc_info = f"accuracy:{calc_error[0]}, \nprecision:{calc_error[1]}, \nrecall:{calc_error[2]}, \nf1_measure:{calc_error[3]}\n"
    calc_info="debug"
    drawHeatmap("Around", mode, heatmap_data, data_info, calc_info, unique_dates, subject_data[0])
    
    
    

# 平均就寝時間と平均起床時間の中央時刻の前後を精査して，歩数から睡眠を推定する関数
def estimateSleepFromStep_Median(method, time_specified_data, step_observation_threshold, subject_data):
    
    # 推定に必要な設定
    
    # modeと手法のタイプを取得
    mode, method_type = method
    
    # それぞれの時刻をヒートマップに対応する形に変換する．hh:mm -> 5分刻みのindex
    set_reference_time = setReferenceTime(time_specified_data[0], time_specified_data[1])
    # weekday_time, holiday_time = [list(map(time_to_decimal, set_reference_time[i])) for i in range(2)]
    weekday_time, holiday_time = set_reference_time
    print(weekday_time, holiday_time)
 
    # 必要なデータをセット
    data_frame_settings = dataFrameSettings(mode, subject_data)
    [df, unique_dates, heatmap_data] = data_frame_settings
    #-------------------------------------------
    
    # 前日のデータを格納する変数
    previous_day_data_ = []

    # 推定するアルゴリズムを実装
    for i, date in enumerate(unique_dates):
        date_data = df[df['startDate'].dt.date == date]
        end_tmp = 0
        set_bed_range = []
        set_wake_range = []
        estimate_index_array = []
        
        # 日を跨ぐかどうか
        is_cross_day_ = True
        
        # その日が平日か土日かによって，中央時刻と精査先時刻を設定
        if (date.weekday() == 5 or (date.weekday() == 6)):
            set_bed_range = [holiday_time[0], holiday_time[3]]
            set_wake_range = [holiday_time[1], holiday_time[2]]
        else: 
            set_bed_range = [weekday_time[0], weekday_time[3]]
            set_wake_range = [weekday_time[1], weekday_time[2]]
        # print(set_bed_range, set_wake_range)
        
        # 就寝時刻を推定：中央時刻より前のデータを取得
        bed_date_data = date_data[date_data["endDate"].dt.time <= pd.to_datetime(set_bed_range[0], format='%H:%M').time()]
        
        # print(f"-----------------{date}")
        # print(bed_date_data["endDate"])
        # 中央時刻より前のデータがある場合
        if(len(bed_date_data) > 0):
            # 日毎のdfのendDateの最後の時間(最大値)を取得してヒートマップの形式に変換
            # end_indexが就寝時間
            bed_time = int((bed_date_data['endDate'].max().hour * 60 + bed_date_data['endDate'].max().minute) / 5)
            estimate_index_array.append(bed_time)
            # print(f"bed:{bed_time}")
            # print(bed_date_data["endDate"].max())
        else:
            # TODO: 前日に遡る処理を追加
            # データがない場合，就寝時刻を何に設定するか考える必要がある
            is_cross_day_  = False
            if(len(previous_day_data_) > 0):
                # 前日のデータがある場合に前日のデータを取得精査してヒートマップの形式に変換
                bed_time=int((previous_day_data_['endDate'].max().hour * 60 + previous_day_data_['endDate'].max().minute) / 5)
                estimate_index_array.append(bed_time)
                # bed_time = int((previous_day_data['endDate'].max().hour * 60 + previous_day_data['endDate'].max().minute) / 5)
                # estimate_index_array.append(bed_time)
            else:
                is_cross_day_  = True
                # estimate_index_array.append(0)
                estimate_index_array.append(time_to_decimal(set_bed_range[0]))
            # print("No data")
       
        # 起床時刻を推定：中央時刻より前のデータを取得
        wake_date_data = date_data[(date_data["startDate"].dt.time >= pd.to_datetime(set_wake_range[0], format='%H:%M').time()) & (date_data["startDate"].dt.time <= pd.to_datetime(set_wake_range[1], format='%H:%M').time())]
        
        if(len(wake_date_data) > 0):
            # 日毎のdfのendDateの最後の時間(最大値)を取得してヒートマップの形式に変換
            # end_indexが就寝時間
            # print(wake_date_data['startDate'])
            wake_time = int((wake_date_data['startDate'].min().hour * 60 + wake_date_data['startDate'].min().minute) / 5)
            estimate_index_array.append(wake_time)
            
            # print(f"wake:{wake_time}")
            # print(wake_date_data["startDate"].max())
        else:
            # estimate_index_array.append(time_to_decimal(wake_time_average[:-3]))
            # print(time_to_decimal(set_wake_range[0]))
            # TODO: データがない場合，起床時刻を何に設定するか考える必要がある
            estimate_index_array.append(time_to_decimal(set_wake_range[1]))
            #  estimate_index_array.append(time_to_decimal(set_wake_range[1]))
            # print("No data")
        # for j in range(len(date_data) - 1, -1, -1):
        #     row = date_data.iloc[j] #sleep_date_data
        #     start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
        #     end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
        
        
        
        
        # for _, row in date_data.iterrows():
        #     start_index = int(((row['startDate'] - pd.Timedelta(days=1)).hour * 60 + (row['startDate'] - pd.Timedelta(days=1)).minute) / 5)
        #     end_index = int((row['endDate'].hour * 60 + row['endDate'].minute) / 5)
            
            # print(start_index, end_index, i)
        #     # if(start_index - end_tmp > ConvertToHeatmapCompatible(step_observation_threshold)):#9_15
        #     #     is_skip = True
        #     #     break
        #     # else:
        #     #     break
        #         # 処理を実装

    # 日をスキップしない場合はヒートマップ用のデータを更新  
        
                
    # heatmap_data[i, estimate_index_array[0]:288] = 1
    # heatmap_data[i, 0:estimate_index_array[1]] = 1
        # print(estimate_index_array)
        if((is_cross_day_ == False )& (i > 0)):
            heatmap_data[i-1, estimate_index_array[0]:288] = 1
            heatmap_data[i, 0:estimate_index_array[1]] = 1
        else:
            heatmap_data[i, estimate_index_array[0]:estimate_index_array[1]] = 1
        
        previous_day_data_ = date_data[date_data["endDate"].dt.time >= pd.to_datetime(set_bed_range[1], format='%H:%M').time()]
    
    # ヒートマップデータをテキストファイルに出力(推定データ)
    pred_data_pass = f"./extraction_data/pred_sleep_data(Median-{method_type}).txt"
    file = open(pred_data_pass, "w")
    for d in list(itertools.chain.from_iterable(heatmap_data)):
        file.write(f"{d} ")
    file.close()
    
    # 誤差の計算
    calc_error = calculate_error(actual_data_pass, pred_data_pass, f"Median-{method_type}", subject_data)
    
    #-------------------------------------------            
    # ヒートマップの描画
    data_info = f"bed time Avg:{time_specified_data[0][0]}, wake time Avg:{time_specified_data[0][1]}, \nbed time Thd:{"2" if time_specified_data[1][0] == "-" else time_specified_data[1][0]}, wake time Thd:{"2" if time_specified_data[1][1] == "-" else time_specified_data[1][1]}, \nstep observation threshold:{step_observation_threshold}"
    # calc_info = f"accuracy:{calc_error[0]}, \nprecision:{calc_error[1]}, \nrecall:{calc_error[2]}, \nf1_measure:{calc_error[3]}\n"
    calc_info="debug"
    drawHeatmap(f"Median-{method_type}", mode, heatmap_data, data_info, calc_info, unique_dates, subject_data[0])
    
    # set_bed_range = [weekday_time[0], weekday_time[3]]
        #     set_wake_range = [weekday_time[1], weekday_time[2]]
        # else:  
        #     set_bed_range = [holiday_time[0], holiday_time[3]]
        #     set_wake_range = [holiday_time[1], holiday_time[2]]