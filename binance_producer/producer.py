import json
import requests
from binance import ThreadedWebsocketManager
import config
import boto3

api_key = config.BINANCE_CONFIG["API_KEY"]
api_secret = config.BINANCE_CONFIG["SECRET_KEY"]

session = boto3.Session(profile_name="default")
client = session.client("kinesis")


def main():

    # get all symbols
    uri = "https://api.binance.com/api/v1/exchangeInfo"
    sym = requests.get(uri).json()
    sym_list = []

    for i in range(len(sym["symbols"])):
        if sym["symbols"][i]["quoteAsset"] == "BTC":
            sym_list.append(sym["symbols"][i]["symbol"])
    print(sym_list)
    print(len(sym_list))

    # 코인 종류 한번에 지정하기
    # streams = []
    # for i in range(50):
    #     streams.append(sym_list[i].lower() + "@kline_1m")
    # print()
    # print(streams)
    # print()

    # 테스트용 10개짜리
    streams = [
        "ethbtc@kline_1m",
        "dogebtc@kline_1m",
        "adabtc@kline_1m",
        "bnbbtc@kline_1m",
        "xrpbtc@kline_1m",
        "dotbtc@kline_1m",
        "maticbtc@kline_1m",
        "tfuelbtc@kline_1m",
        "solbtc@kline_1m",
        "linkbtc@kline_1m",
    ]

    # 레코드 임시 저장소
    kinesis_records = []

    # 코인별 최신 정보 저장용 딕셔너리
    dic_current = dict()

    # symbol만 받아서 dic_current의 key로 사용
    for stream in streams:
        coin = stream.split("@")[0].upper()
        dic_current[coin] = ""

    # 각 쓰레드에서 msg 들어왔을때 작동할 메서드
    def handle_socket_message(msg):
        data = msg["data"]["k"]  # dict type, 새로 받아온 데이터
        coin = msg["data"]["s"]  # str type, 지금 다루고 있는 symbol, uppercase
        prev = dic_current[coin]  # 이전 값 불러오기
        dic_current[coin] = data  # 새로운 값 넣기

        # 이전 값이 null이 아니고 새로운 값이랑 시작 시간이 다르면
        # 이전 값을 kinesis_records에 append
        if (prev != "") and (prev["t"] != dic_current[coin]["t"]):
            data = json.dumps(data)
            kinesis_records.append({"Data": data, "PartitionKey": coin})
            # 레코드가 10개 모이면 배치 전송, 테스트가 10개라서 10개로 함
            if len(kinesis_records) == 10:
                response = client.put_records(
                    Records=kinesis_records, StreamName="coinBoard"
                )
                print(json.dumps(response, sort_keys=True))
                kinesis_records.clear()

    # 소켓 시작
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
    twm.join()


if __name__ == "__main__":
    main()