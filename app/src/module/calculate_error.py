import numpy as np

# 誤差
# 平均二乗誤差
def calculate_error_mse(true_array_pass, pred_array_pass):
    
    # ファイルからデータを読み込む
    true_file = open(true_array_pass, 'r')
    true_array = true_file.read().split()
    
    pred_file = open(pred_array_pass, 'r')
    pred_array = pred_file.read().split()
    
    # np配列に変換
    true_array = np.array(true_array, dtype=float)
    pred_array = np.array(pred_array, dtype=float)
    
    mse = np.mean((true_array - pred_array) ** 2)
    print(f"MSE: {mse}")
    
# 平均絶対誤差
def calculate_error_mae(true_array_pass, pred_array_pass):
     # ファイルからデータを読み込む
    true_file = open(true_array_pass, 'r')
    true_array = true_file.read().split()
    
    pred_file = open(pred_array_pass, 'r')
    pred_array = pred_file.read().split()
    
    # np配列に変換
    true_array = np.array(true_array, dtype=float)
    pred_array = np.array(pred_array, dtype=float)
    
    mae = np.mean(np.abs(true_array - pred_array))
    print(f"MAE: {mae}")
