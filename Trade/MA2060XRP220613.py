import time
import pyupbit
import datetime
from datetime import datetime as dt
from pytz import timezone


today = dt.now(timezone('Asia/Seoul'))

access = "qzgW0puZ6zHBeixr52BWRKOKWkEGNZvC1qeMz7Ez"
secret = "ZepLSuiKR3u40xcILRFQozGl22xIMTpS5vYurax3"

def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_ma60(ticker):
    """60일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=60)
    ma60 = df['close'].rolling(60).mean().iloc[-1]
    return ma60

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute720", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute720", count=1)
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
    today = dt.now(timezone('Asia/Seoul'))
    print('working...')
    print(today)
    try:
        now = today
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(hours=12)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            #ma20, ma60 비교로 상승장,하락장 판별
            ma20 = get_ma20("KRW-XRP")
            ma60 = get_ma60("KRW-XRP")
            if ma20 > ma60:
                target_price = get_target_price("KRW-XRP", 0.5)
            else:
                target_price = get_target_price("KRW-XRP", 0.9)
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-XRP", krw*0.9995)
        else:
            btc = get_balance("XRP")
            if btc > 15:
                upbit.sell_market_order("KRW-XRP", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
        """ㅓㅓㄹ"""