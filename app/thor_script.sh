# 許可
# chmod +x thor_script.sh

# 処理の実装
# ./thor_script.sh

# データの抽出
# python3 applehealthdata.py data/export.xml

# データを格納しているフォルダに移動
cd export_zip
pwd

# データ数のカウント
count=0

# エラーが出たデータのカウント

# カレントディレクトリ内のすべてのzipファイルに対して処理を行う
for file in *; do
    # ファイル名から空白を削除
    mv "$file" $(echo $file | tr -d ' ')
    rename_file=$(echo $file | tr -d ' ')
    # echo $rename_file

    ##日付と拡張子を削除
    rename=$(echo "$file" | sed 's/.*-\(.*\)\.zip/\1/')

    # id，回答就寝時刻，回答起床時刻を抽出
    IFS='_' read -r -a time <<<"${rename%.*}"
    bed=${time[-2]}
    wake=${time[-1]}
    id=${rename//$bed/}
    id=${id//$wake/}
    id=${id//_/}
    # echo "id:$id, bed:$bed, wake:$wake"

    # データ自動抽出処理
    unzip -d ../data $rename_file                     # zipファイルを解凍
    mv ../data/apple_health_export/export.xml ../data # export.xmlをdataディレクトリに移動
    rm -r ../data/apple_health_export                 # apple_health_exportディレクトリを削除

    # applehealthdata.pyを実行
    cd ..
    python3 applehealthdata.py data/export.xml

    # python3 main.py実行時に名前と時刻を指定するようにする．
    # 実行ファイルを実行
    python3 main.py $id $bed $wake
    cd ./export_zip

    # 区切り線を表示
    echo "-------------------------------------------"

    # export.xmlを削除してループを再開する．

    # データの数をカウントする
    count=$(expr $count + 1)
done

# データの数を出力
echo "データ量：${count}"
