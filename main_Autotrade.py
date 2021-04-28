import time
import pyupbit
import datetime

access = "37w9Ple15Epe5AxRkhaMOp7ZyiuDkYwjQt69rlgd"          # 본인 값으로 변경
secret = "9ttdPjuolevVIkmGsLYPdHXe9dh7wH2Nx15u0I1c"          # 본인 값으로 변경

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def buy_coin(ticker):
    """코인 구매"""
    target_price = get_target_price(ticker, 0.5)
    current_price = get_current_price(ticker)
    # print(target_price)
    # print(current_price)
    # print()
    if target_price < current_price:
        krw = get_balance("KRW")
        if krw > 5000:
            upbit.buy_market_order(ticker, krw*0.4)
    return 0

def sell_coin(ticker):
    """코인 판매"""
    coin_num = upbit.get_balance(ticker)
    corrent_num=pyupbit.get_current_price(ticker)
    if corrent_num*coin_num > 1200:
        upbit.sell_market_order(ticker, coin_num*0.9995)
    return 0
                


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:

    coins=["KRW-DAWN","KRW-XRP","KRW-BTT","KRW-DOGE","KRW-VET","KRW-BTC","KRW-ETC","KRW-ETH","KRW-BTG","KRW-STRK","KRW-MED","KRW-MVL"]
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            
            for coin in coins:
                print("###")
                print(coin)
                buy_coin(coin)
                time.sleep(0.05)





        else:
            for coin in coins:
                sell_coin(coin)
                time.sleep(0.05)


        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)