import json
from binance import ThreadedWebsocketManager
import config
import boto3
import os
import logging
import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


api_key = config.BINANCE_CONFIG["API_KEY"]
api_secret = config.BINANCE_CONFIG["SECRET_KEY"]

client = boto3.client("kinesis", "ap-northeast-2")


def main():
    idx = int(os.getenv("INDEX"))  # 331/batch
    logger.info(f"index: {idx}")
    batch = 20  # 한번에 조회할 코인 갯수
    streams = []

    # 조회할 코인 목록 만들기
    f = open("symbols.txt").read()
    sym_list = f.strip().split("\n")
    streams = [
        x.lower() + "@kline_1m" for x in sym_list[idx * batch : (idx + 1) * batch]
    ]

    # 코인 종류 한번에 지정하기

    logger.info(f"streams: {streams}")

    # 레코드 임시 저장소
    kinesis_records = []

    # 코인별 최신 정보 저장용 딕셔너리
    dic_current = dict()

    # symbol만 받아서 dic_current의 key로 사용
    for stream in streams:
        coin = stream.split("@")[0].upper()
        dic_current[coin] = ""

    def format_json_keys(data):
        new_format = {
            "t": "opentime",
            "s": "symbol",
            "o": "open_price",
            "c": "close_price",
            "h": "high_price",
            "l": "low_price",
            "n": "num_trades",
            "q": "quote_asset_volume",
        }
        want = ["t", "s", "o", "c", "h", "l", "n", "q"]

        data_filtered = dict()
        for col in want:
            data_filtered[col] = data[col]

        new_data = dict(
            (new_format[key], value) for (key, value) in data_filtered.items()
        )

        return new_data

    def to_KRW(data):
        key_float = [
            "open_price",
            "close_price",
            "high_price",
            "low_price",
            "quote_asset_volume",
        ]
        # 빗썸에서 실시간 국내 비트코인 가격 받아오기
        # uri = "https://api.bithumb.com/public/ticker/BTC"
        # bitcoin = requests.get(uri).json()
        # price = int(bitcoin["data"]["closing_price"])

        # 비트코인 가격 고정해서 사용하기
        price = 40000000
        for key in key_float:
            data[key] = float(data[key]) * price
        return data
    
    def to_timestamp(data):
        # unixtime to datetime
        data["opentime"] = datetime.datetime.fromtimestamp((data["opentime"])/1000).strftime('%Y-%m-%d %H:%M:%S')
        return data

    # 각 쓰레드에서 msg 들어왔을때 작동할 메서드
    def handle_socket_message(msg):
        data = format_json_keys(msg["data"]["k"])  # dict type, 새로 받아온 데이터
        data = to_KRW(data)
        # data = to_timestamp(data)
        coin = msg["data"]["s"]  # str type, 지금 다루고 있는 symbol, uppercase
        prev = dic_current[coin]  # 이전 값 불러오기
        dic_current[coin] = data  # 새로운 값 넣기

        # 이전 값이 null이 아니고 새로운 값이랑 시작 시간이 다르면
        # 이전 값을 kinesis_records에 append
        if (prev != "") and (prev["opentime"] != dic_current[coin]["opentime"]):
            data = json.dumps(data)
            kinesis_records.append({"Data": data, "PartitionKey": coin})
            # 레코드가 10개 모이면 배치 전송, 테스트가 10개라서 10개로 함
            if len(kinesis_records) == batch:
                response = client.put_records(
                    Records=kinesis_records, StreamName="coinBoard"
                )
                logger.info(f"Records are sent: {response}")
                kinesis_records.clear()

    # 소켓 시작
    logger.info("Socket Started!")
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
    twm.join()


if __name__ == "__main__":
    main()
