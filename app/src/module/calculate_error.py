import numpy as np

# 誤差の計算
def calculate_error(true_data_pass, pred_data_pass):
    
    # ファイルからデータを読み込む
    true_file = open(true_data_pass, 'r')
    true_array = true_file.read().split()
    
    pred_file = open(pred_data_pass, 'r')
    pred_array = pred_file.read().split()
    
    # np配列に変換
    true_array = np.array(true_array, dtype=float)
    pred_array = np.array(pred_array, dtype=float)
    print(len(true_array))
    print(len(pred_array))
    
    # 長さが同じ場合
    if(len(true_array) == len(pred_array)):
        mse = np.mean((true_array - pred_array) ** 2)
        mae = np.mean(np.abs(true_array - pred_array))    
        print(f"MSE: {mse}") # 平均二乗誤差
        print(f"MAE: {mae}") # 平均絶対誤差
    else:
        mse = "Data length does not match"
        mae = "Data length does not match"
        
    

    result = [mse, mae]
    
    return result
