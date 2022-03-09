import time
import pyupbit
import datetime

access = "vPTsY97GkPAhQcbvfx3OXeyHQgEQVfmiTYdHQ8gQ"
secret = "Rua7oyeKTenNW2JCHMJNVSEdvdjzWgqDJcQnjB1p"


"""
k = 0.3 or 0.35 일때 가장 유리한데
하락장에는 비교적 0.35가 안전하다
상승장이라고 판단되면 0.3으로 바꿀것 유의미한 차이가 있다.
ETH가 아닌 다른종목은 다른  k값을 찾아야함
하지만 메이저 종목중 ETH만이 같은 K값에 대한 일관적인 결과를 보여줌
"""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="min", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="min", count=1)
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
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(minutes=1)

        if start_time < now < end_time - datetime.timedelta(seconds=5):
            target_price = get_target_price("KRW-ETH", 0.35)
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)
        else:
            btc = get_balance("ETH")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-ETH", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)