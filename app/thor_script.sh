# 許可
# chmod +x thor_script.sh

# 処理の実装
# ./thor_script.sh

# データの抽出
# python3 applehealthdata.py data/export.xml

# 処理の実装
# python3 main.py

cd export_zip
# ディレクトリ内のファイルを取得
zip_files=$(ls)

# # ファイルの一覧を表示
# echo "$zip_files"

# カレントディレクトリ内のすべてのファイル名を表示

for file in *; do

    #日付と拡張子を削除
    rename=$(echo "$file" | sed 's/.* - \(.*\)\.zip/\1/')

    # id，回答就寝時刻，回答起床時刻を抽出
    IFS='_' read -r -a time <<<"${rename%.*}"
    bed=${time[-2]}
    wake=${time[-1]}
    id=${rename//bed/}
    id=${id//$wake/}
    id=${id//_/}
    echo "id:$id, bed:$bed, wake:$wake"

    # bedとwakeが数字四桁ではない場合はハイフンにする．
    # 数字四桁である場合は，0200->2，1030->10.5，2400->0に変換する(python側でもいい)

    # データ自動抽出処理
    # unzip -d ../data $file                            # zipファイルを解凍
    # mv ../data/apple_health_export/export.xml ../data # export.xmlをdataディレクトリに移動
    # rm -r ../data/apple_health_export                 # apple_health_exportディレクトリを削除

    # python3 main.py実行時に名前と時刻を指定するようにする．
done
