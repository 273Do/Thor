import csv
import json
import pandas as pd
import numpy as np
from datetime import datetime
from src.module.time_function import median_time, shift_time, time_to_minutes

output_data = {
    "id": None,
    "mode": None,
    "date": None,
    "last_step": None,
    "first_step": None,
    "actual_bed": None,
    "actual_wake": None,
    "actual_median": None,
    "estimate_bed": None,
    "estimate_wake": None,
    "estimate_median": None,
    "bed_error": None,
    "wake_error": None,
}

actual_sleep_data = {}

actual_step_data = {}

# 回答に対する間時間の平均を保存するブジェクト
survey_list = {"survey_0": {'よく持ち歩く': None, '持ち歩く': None, 'あまり持ち歩かない': None, 'ほとんど持ち歩かない': None},
               "survey_1": {'よく持ち歩く': None, '持ち歩く': None,
                            'あまり持ち歩かない': None, 'ほとんど持ち歩かない': None},
               "survey_2": {'帰宅後': None, '就寝直前': None,
                            '帰宅して就寝直前までの間': None, 'その他': None},
               "survey_3": {'就寝直前': None, '15分前程度': None,
                            '30分前程度': None, '1時間前程度': None, '2時間より以前': None, '充電しない': None},
               "survey_4": {'よく持ち歩く': None, '持ち歩く': None,
                            'あまり持ち歩かない': None, 'ほとんど持ち歩かない': None},
               "survey_5": {'起床直後': None, '家を出る直後': None, '起床直後から家を出るまでの間': None, 'その他': None},
               "survey_6": {'触らない': None, '15分程度': None,
                            '30分程度': None, '1時間程度': None, '2時以上': None}, }

# actual_sleep_dataとoutput_dataを紐ずけてcsvファイルに格納する関数


def appendToCSV(habit_time):
    print(f"habit_time:{habit_time}")

    # with open("../../extraction_data/all_output_data.csv", 'a', newline='') as file:
    # actual_sleep_dataのデータを参照して[]でない場合はoutput_dataに格納してcsvに記録
    # #print(actual_sleep_data[output_data["date"]])
    # #print(output_data["date"] in actual_sleep_data)
    # if(len(actual_sleep_data[output_data["date"]]) != 0):
    if output_data["date"] in actual_sleep_data:
        output_data["last_step"] = actual_step_data[output_data["date"]][0]
        output_data["first_step"] = actual_step_data[output_data["date"]][1]

        output_data["actual_bed"] = actual_sleep_data[output_data["date"]][0]
        output_data["actual_wake"] = actual_sleep_data[output_data["date"]][1]

        actual_median = median_time(
            output_data["actual_bed"], output_data["actual_wake"])
        estimate_median = median_time(
            output_data["estimate_bed"], output_data["estimate_wake"])

        # それぞれの時間の中央時間を格納
        output_data["actual_median"] = actual_median
        output_data["estimate_median"] = estimate_median

        # output_data["shift"], output_data["shift_value"] = shift_time(
        #     actual_median, estimate_median)
        a_e_shift = shift_time(actual_median, estimate_median)
        if (pd.to_datetime('00:30', format='%H:%M').time() >= pd.to_datetime(a_e_shift[1], format='%H:%M').time()):
            output_data["shift"] = 0
        else:
            output_data["shift"] = a_e_shift[0]
        output_data["shift_value"] = a_e_shift[1]

        if (habit_time != ""):
            # 大体の時間と実際の時間の中央値とシフト位置を求める
            habit_median = median_time(
                habit_time[0][:-3], habit_time[1][:-3])
            print(habit_median)

            h_a_shift = shift_time(
                habit_median, actual_median)
            print(h_a_shift)
            if (pd.to_datetime('00:30', format='%H:%M').time() >= pd.to_datetime(h_a_shift[1], format='%H:%M').time()):
                output_data["h_a_shift"] = 0
            else:
                output_data["h_a_shift"] = h_a_shift[0]

            h_e_shift = shift_time(
                habit_median, estimate_median)
            print(h_e_shift)
            if (pd.to_datetime('00:30', format='%H:%M').time() >= pd.to_datetime(h_e_shift[1], format='%H:%M').time()):
                output_data["h_e_shift"] = 0
            else:
                output_data["h_e_shift"] = h_e_shift[0]
        else:
            output_data["h_a_shift"] = "NoAround"
            output_data["h_e_shift"] = "NoAround"

        # 実際と推定の誤差を算出
        output_data["bed_error"] = shift_time(
            output_data["actual_bed"], output_data["estimate_bed"])[1]
        output_data["wake_error"] = shift_time(
            output_data["actual_wake"], output_data["estimate_wake"])[1]

        # print(output_data["id"], output_data["mode"], output_data["date"], output_data["actual_bed"], output_data["actual_wake"],
        #   output_data["actual_median"], output_data["estimate_bed"], output_data["estimate_wake"], output_data["estimate_median"])

        # 統合ファイルに書き込み
        with open("extraction_data/z_all_output/all_output_data.csv", mode='a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    output_data["id"],
                    output_data["mode"],
                    output_data["date"],
                    output_data["last_step"],
                    output_data["first_step"],
                    output_data["actual_bed"],
                    output_data["actual_wake"],
                    output_data["actual_median"],
                    output_data["estimate_bed"],
                    output_data["estimate_wake"],
                    output_data["estimate_median"],
                    output_data["shift"],
                    output_data["shift_value"],
                    output_data["h_a_shift"],
                    output_data["h_e_shift"],
                    output_data["bed_error"],
                    output_data["wake_error"],
                ]
            )

# 回答によるカテゴリー分けを行う関数


def dataCategorization():
    # print("データのカテゴリー分けを行う")
    # all_output_data.csvからデータを読み込んで，all_preliminary_data.csvをもとにして
    # data_categorization.jsonにデータを格納する

    df = pd.read_csv("extraction_data/z_all_output/all_output_data.csv")
    survey_df = pd.read_csv(
        "extraction_data/z_all_output/all_preliminary_data.csv")

    # 使用できるデータを抽出
    available_laststep_data_df = df[(df['mode'] == "Median")]
    available_firststep_data_df = df[(df['mode'] == "Median")]
    # available_laststep_data_df = df[(df['mode'] == "Median") & (
    #     df['last_step'] != "NoData")]
    # available_firststep_data_df = df[(df['mode'] == "Median") & (
    #     df['first_step'] != "NoData")]
    # available_laststep_data_df = df[(df['mode'] == "Around") & (
    #     df['last_step'] != "NoData")]
    # available_firststep_data_df = df[(df['mode'] == "Around") & (
    #     df['first_step'] != "NoData")]

    # 被験者の回答ごとにリストに間時間を格納していく
    for survey_data in survey_list:
        # print("-----------------")
        # print(survey_data)

        # 質問の回答ごとに間時間の平均値を求める
        for answer in survey_list[survey_data]:
            # フィルタリングするidを格納する配列
            ids_to_filter = []

            # print(answer)
            filtered_df = survey_df[survey_df[survey_data] == answer]

            # 配列にidを格納
            for id in filtered_df['id']:
                ids_to_filter.append(id)

            # print(ids_to_filter)

            # それぞれの回答ごとに間時間の平均値を求める
            if (survey_data == "survey_0"):
                # print("就寝間時間，起床間時間の平均値を求める")
                #  全被験者の間時間の平均値を求める方法
                available_laststep_data = available_laststep_data_df[available_laststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                    datetime.strptime(shift_time(row['estimate_bed'], row['actual_bed'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                available_firststep_data = available_firststep_data_df[available_firststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                    datetime.strptime(shift_time(row['estimate_wake'], row['actual_wake'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                # available_laststep_data = available_laststep_data_df[available_laststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                #     datetime.strptime(shift_time(row['last_step'], row['actual_bed'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                # available_firststep_data = available_firststep_data_df[available_firststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                #     datetime.strptime(shift_time(row['first_step'], row['actual_wake'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                # print(f"{survey_data}：「{answer}」の間就寝時間の平均値：", format(np.mean(
                # available_laststep_data), ".0f"))
                # print(f"{survey_data}：「{answer}」の間起床時間の平均値：", format(np.mean(
                # available_firststep_data), ".0f"))
                if (len(available_laststep_data) > 0):
                    survey_list[survey_data][answer] = [
                        format(np.mean(available_laststep_data), ".0f"), format(np.mean(available_firststep_data), ".0f")]

            elif ((survey_data == "survey_1") or (survey_data == "survey_2") or (survey_data == "survey_3")):
                # print("就寝間時間の平均値を求める")
                available_laststep_data = available_laststep_data_df[available_laststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                    datetime.strptime(shift_time(row['estimate_bed'], row['actual_bed'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                # available_laststep_data = available_laststep_data_df[available_laststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                #     datetime.strptime(shift_time(row['last_step'], row['actual_bed'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                # print(f"{survey_data}：「{answer}」の間就寝時間の平均値：", format(np.mean(
                # available_laststep_data), ".0f"))
                if (len(available_laststep_data) > 0):
                    survey_list[survey_data][answer] = format(np.mean(
                        available_laststep_data), ".0f")
            else:
                # print("起床間時間の平均値を求める")
                available_firststep_data = available_firststep_data_df[available_firststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                    datetime.strptime(shift_time(row['estimate_wake'], row['actual_wake'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                # available_firststep_data = available_firststep_data_df[available_firststep_data_df['id'].isin(ids_to_filter)] .apply(lambda row: time_to_minutes(
                #     datetime.strptime(shift_time(row['first_step'], row['actual_wake'])[1], "%H:%M").strftime("%H:%M")), axis=1)
                # print(f"{survey_data}：「{answer}」の間起床時間の平均値：", format(np.mean(
                # available_firststep_data), ".0f"))
                if (len(available_firststep_data) > 0):
                    survey_list[survey_data][answer] = format(np.mean(
                        available_firststep_data), ".0f")

    with open('extraction_data/z_all_output/data_categorization.json', 'w') as f:
        json.dump(survey_list, f, indent=2, ensure_ascii=False)
