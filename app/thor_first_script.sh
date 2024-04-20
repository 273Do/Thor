# 許可
# chmod +x thor_first_script.sh

# 処理の実装
# ./thor_first_script.sh

# zipファイルを格納しているフォルダに移動
cd export_zip

# データ数のカウント
count=0

#処理時間計測
SECONDS=0

# カレントディレクトリ内のすべてのzipファイルに対して処理を行う
for file in *; do
    # ファイル名から空白を削除

    mv "$file" $(echo $file | tr -d ' ')
    rename_file=$(echo $file | tr -d ' ')

    ##日付と拡張子を削除
    rename=$(echo "$file" | sed 's/.*-\(.*\)\.zip/\1/')

    # id，回答就寝時刻，回答起床時刻を抽出
    IFS='_' read -r -a time <<<"${rename%.*}"
    bed=${time[-2]}
    wake=${time[-1]}
    id=${rename//$bed/}
    id=${id//$wake/}
    id=${id//_/}
    echo "id:$id, bed:$bed, wake:$wake"

    # データ自動抽出処理
    unzip -d ../data $rename_file                     # zipファイルを解凍
    mv ../data/apple_health_export/export.xml ../data # export.xmlをdataディレクトリに移動
    rm -r ../data/apple_health_export                 # apple_health_exportディレクトリを削除

    # appディレクトリに戻る
    cd ..

    # applehealthdata.pyを実行
    python3 applehealthdata.py data/export.xml

    cd export_zip

    # 被験者idのフォルダを作成して，そこにデータを全て移動
    mkdir "../data/$id"_"$bed"_"$wake"
    mv "../data"/*.csv "../data/$id"_"$bed"_"$wake"

    # 画像格納用のフォルダを作成
    mkdir "../extraction_data/$id"_"$bed"_"$wake"

    # 区切り線を表示
    echo "-------------------------------------------"

    # データの数をカウントする
    count=$(expr $count + 1)
done

# export.xmlを削除する．
rm "../data/export.xml"

# データの数を出力
echo "データ量：${count}"

# 処理にかかった時間を出力
time=$SECONDS
echo "${time}秒"
