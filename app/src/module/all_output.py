import csv
from src.module.time_function import median_time

output_data = {
    "id": None,
    "mode": None,
    "date": None,
    "actual_bed": None,
    "actual_wake": None,
    "actual_median": None,
    "estimate_bed": None,
    "estimate_wake": None,
    "estimate_median": None
}

actual_sleep_data = {}

actual_step_data = {}

# actual_sleep_dataとoutput_dataを紐ずけてcsvファイルに格納する関数


def append_to_csv():
    # with open("../../extraction_data/all_output_data.csv", 'a', newline='') as file:
    # actual_sleep_dataのデータを参照して[]でない場合はoutput_dataに格納してcsvに記録
    # print(actual_sleep_data[output_data["date"]])
    print(output_data["date"] in actual_sleep_data)
    # if(len(actual_sleep_data[output_data["date"]]) != 0):
    if output_data["date"] in actual_sleep_data:
        output_data["actual_bed"] = actual_sleep_data[output_data["date"]][0]
        output_data["actual_wake"] = actual_sleep_data[output_data["date"]][1]

        # それぞれの時間の中央時間を格納
        output_data["actual_median"] = median_time(
            output_data["actual_bed"], output_data["actual_wake"])
        output_data["estimate_median"] = median_time(
            output_data["estimate_bed"], output_data["estimate_wake"])

        print(output_data["id"], output_data["mode"], output_data["date"], output_data["actual_bed"], output_data["actual_wake"],
              output_data["actual_median"], output_data["estimate_bed"], output_data["estimate_wake"], output_data["estimate_median"])

        # 統合ファイルに書き込み
        with open("extraction_data/all_output_data.csv", mode='a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    output_data["id"],
                    output_data["mode"],
                    output_data["date"],
                    output_data["actual_bed"],
                    output_data["actual_wake"],
                    output_data["actual_median"],
                    output_data["estimate_bed"],
                    output_data["estimate_wake"],
                    output_data["estimate_median"]
                ]
            )
