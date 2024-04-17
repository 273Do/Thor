# 許可
# chmod +x thor_main_script.sh

# 処理の実装
# ./thor_main_script.sh

# データを格納しているフォルダに移動
cd data

# データ数のカウント
count=0

#処理時間計測
SECONDS=0

# カレントディレクトリ内のすべてのzipファイルに対して処理を行う
for file in *; do

    # id，回答就寝時刻，回答起床時刻を抽出
    IFS='_' read -r -a time <<<"${file%.*}"
    bed=${time[-2]}
    wake=${time[-1]}
    id=${file//$bed/}
    id=${id//$wake/}
    id=${id//_/}
    # echo "id:$id, bed:$bed, wake:$wake"

    # appディレクトリに戻る
    cd ..

    # python3 main.py実行時に名前と時刻を指定するようにする．
    # 実行ファイルを実行
    python3 main.py $id $bed $wake
    cd data

    # 被験者idのフォルダを作成して，そこにデータを全て移動
    mkdir "../extraction_data/$id"_"$bed"_"$wake"
    mv "../extraction_data"/*.png "../extraction_data/$id"_"$bed"_"$wake"

    # 区切り線を表示
    echo "-------------------------------------------"

    # データの数をカウントする
    count=$(expr $count + 1)
done

# テキストファイルを削除する．
rm "../extraction_data/"/*.txt

# データの数を出力
echo "データ量：${count}"

# 処理にかかった時間を出力
time=$SECONDS
echo "${time}秒"
