import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from src.module.draw_heatmap import confusionMatrixHeatmap
import sys

# 誤差の計算
def calculate_error(actual_data_pass, pred_data_pass, method, subject_data):
    
    # ファイルからデータを読み込む
    actual_file = open(actual_data_pass, 'r')
    actual_array = actual_file.read().split()
    
    pred_file = open(pred_data_pass, 'r')
    pred_array = pred_file.read().split()
    
    # np配列に変換
    actual_array = np.array(actual_array, dtype=float)
    pred_array = np.array(pred_array, dtype=float)
    
    print(len(actual_array))
    print(len(pred_array))
    
    #長さが同じ場合
    if(len(actual_array) == len(pred_array)):
        # mse = np.mean((actual_array - pred_array) ** 2)
        # mae = np.mean(np.abs(actual_array - pred_array))    
        # print(f"MSE: {mse}") # 平均二乗誤差
        # print(f"MAE: {mae}") # 平均絶対誤差
        
        # 混同行列を出力
        cm = confusion_matrix(actual_array, pred_array, labels=[1, 0])
        print("confusion_matrix")
        print(np.array(cm))
        confusionMatrixHeatmap(np.array(cm), method, subject_data)
    
        # 正解率を出力
        accuracy = accuracy_score(actual_array, pred_array)
        print("accuracy")
        print(accuracy)

        # 適合率を出力
        precision = precision_score(actual_array, pred_array)
        print("precision")
        print(precision)

        # 再現率を出力
        recall = recall_score(actual_array, pred_array)
        print("recall")
        print(recall)

        # F値を出力-F1-measure
        f1_measure = f1_score(actual_array, pred_array)
        print("f1_measure")
        print(f1_measure)

        # sys.exit()
        return [accuracy, precision, recall, f1_measure]
        
    else:
        mse = "Data length does not match"
        mae = "Data length does not match"
        
    

    result = [mse, mae]
    
    return result
