import itertools
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from src.module.draw_heatmap import confusionMatrixHeatmap
import sys

# 誤差の計算
def calculate_error(actual_data_pass, pred_data_pass, method, subject_data):
    
    # ファイルからデータを読み込む
    actual_file = open(actual_data_pass, 'r')
    actual_array = actual_file.read().splitlines()
    pred_file = open(pred_data_pass, 'r')
    pred_array = pred_file.read().splitlines()
        
    # print(len(actual_array))
    if(len(actual_array) > 1):
        actual_data = actual_array[0].split()
        actual_dates = actual_array[1].split()

        pred_data = pred_array[0].split()
        pred_dates = pred_array[1].split()
            
        # np配列に変換，288個ずつに分割
        actual_data = np.array(actual_data, dtype=float).reshape(-1, 288)
        pred_data = np.array(pred_data, dtype=float).reshape(-1, 288)

        # 日付をkeyとして，それぞれのデータのオブジェクト(辞書)を作成する
        actual_dictionary = {}
        pred_dictionary = {}
        
        for i in range(len(actual_data)):
            key = pred_dates[i]
            actual_dictionary[key] = actual_data[i]
            pred_dictionary[key] = pred_data[i]
    
        # keyと実際に観測された正解データとkeyを比較してデータを抽出する
        extracted_actual_data = []
        extracted_pred_data = []
        for key in actual_dictionary.keys():
            if key in actual_dates:
                extracted_actual_data.append(actual_dictionary[key])
                extracted_pred_data.append(pred_dictionary[key])
        extracted_actual_data = list(itertools.chain.from_iterable(extracted_actual_data))
        extracted_pred_data = list(itertools.chain.from_iterable(extracted_pred_data))
    
    
    
    # mse = np.mean((actual_array - pred_array) ** 2)
    # mae = np.mean(np.abs(actual_array - pred_array))    
    # print(f"MSE: {mse}") # 平均二乗誤差
    # print(f"MAE: {mae}") # 平均絶対誤差
        
        # 混同行列を出力
        cm = confusion_matrix(extracted_actual_data, extracted_pred_data, labels=[1, 0])
        print("confusion_matrix")
        print(np.array(cm))
    
        data_info = f"valid date count:{len(actual_dates)}, \ndata count:{len(extracted_actual_data)}"
        confusionMatrixHeatmap(np.array(cm), method, data_info, subject_data)
    
        # 正解率を出力
        accuracy = accuracy_score(extracted_actual_data, extracted_pred_data)
        print("accuracy")
        print(accuracy)

        # 適合率を出力
        precision = precision_score(extracted_actual_data, extracted_pred_data)
        print("precision")
        print(precision)

        # 再現率を出力
        recall = recall_score(extracted_actual_data, extracted_pred_data)
        print("recall")
        print(recall)

        # F値を出力-F1-measure
        f1_measure = f1_score(extracted_actual_data, extracted_pred_data)
        print("f1_measure")
        print(f1_measure)

        # sys.exit()
        return [accuracy, precision, recall, f1_measure]
    
    else:
        print("正解データが観測されていません．")
        return ["NoData", "NoData", "NoData", "NoData"]
