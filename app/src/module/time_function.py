from datetime import datetime, timedelta

# 時間をヒートマップの形式に対応するように変換する関数
ConvertToHeatmapCompatible = lambda time: int(288 * time / 24)

# h形式の時間をhh:mmに変換する関数
ConvertToHHMM = lambda time: f"{int(time):02d}:{round((time - int(time)) * 60):02d}:00"

# hhmmをh形式の時間に変換する関数
def ConvertToH(time_str):
    if len(time_str) == 4:
        hours = int(time_str[:2])
        minutes = int(time_str[2:])
    elif len(time_str) == 3:
        hours = int(time_str[0])
        minutes = int(time_str[1:])
    else:
        raise ValueError("無効な時刻形式です")
    
    decimal_time = hours + minutes / 60
    return decimal_time

# 時間をヒートマップの形式に対応するように変換する関数 (hh:mm -> 5分刻みのindex)
def time_to_decimal(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return ConvertToHeatmapCompatible(hours + minutes / 60)

# 時間の和を求める関数
def add_time(time_str1, time_str2):
    # 時間文字列を datetime オブジェクトに変換
    time1 = datetime.strptime(time_str1, '%H:%M:%S')
    time2 = datetime.strptime(time_str2, '%H:%M:%S')
    
    # 時間の足し算
    result_time = time1 + (time2 - datetime(1900, 1, 1))
    
    # 結果を文字列に変換して返す
    return result_time.strftime('%H:%M:%S')

# 時間の差を求める関数
def subtract_time(time_str1, time_str2):
    # 時間文字列を datetime オブジェクトに変換
    time1 = datetime.strptime(time_str1, '%H:%M:%S')
    time2 = datetime.strptime(time_str2, '%H:%M:%S')
    
    # 時間の引き算
    result_time = time1 - (time2 - datetime(1900, 1, 1))
    
    # 結果を文字列に変換して返す
    return result_time.strftime('%H:%M:%S')