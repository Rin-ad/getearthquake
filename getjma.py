import requests
import csv
import epicenter as epi

p2pzishin = "https://api.p2pquake.net/v2/jma/quake?limit=100&order=1&since_date=20240101&until_date=20240102&min_scale=40"

zishin = requests.get(p2pzishin).json()

count = 0

# CSVファイルを書き込みモードで開く
with open('earthquake_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # CSVライターを作成
    csv_writer = csv.writer(csvfile)

    # ヘッダーを書き込む
    csv_writer.writerow(['Count', 'Time', 'Hypocenter', 'Max Scale', 'Magnitude', 'depth(km)'])

    # データをCSVに書き込む
    for i in range(0, 100):  # 100件までのデータを処理
        if zishin[i]['earthquake']['hypocenter']['name'] != '':
            count += 1
            depth = str(zishin[i]['earthquake']['hypocenter']['depth']) + "km"
            name = str(zishin[i]['earthquake']['hypocenter']['name'])  # 震源位置
            maxScale_raw = str(zishin[i]['earthquake']['maxScale'])  # 最大震度(変換前)
            time = str(zishin[i]['earthquake']['time'])  # 発生した時刻
            lat = float(zishin[i]['earthquake']['hypocenter']['latitude'])
            lon = float(zishin[i]['earthquake']['hypocenter']['longitude'])
            magnitude = str(zishin[i]['earthquake']['hypocenter']['magnitude'])  # マグニチュード

            ms = {
                '-1': 'None',
                '10': '1',
                '20': '2',
                '30': '3',
                '40': '4',
                '45': '5-',
                '50': '5+',
                '55': '6-',
                '60': '6+',
                '70': '7',
            }
            maxScale = ms[maxScale_raw]  # 最大震度を一般的な形に

            if name == "":
                name = "None"

            if magnitude == "-1":
                magnitude = "None"

            # データをCSVに書き込む
            csv_writer.writerow([count, time, name, maxScale, magnitude, depth])
            epi.genmap(lat,lon,f'{count}_{name}')

            print(f"{count}|{time}|震源地:{name}|最大震度:{maxScale}|マグニチュード:{magnitude}|緯度:{lat}|経度:{lon}")

print("CSVファイルに書き込みが完了しました。")
