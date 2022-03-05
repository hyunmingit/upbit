import time
import pyupbit
from collections import deque

#주문은 초당 8회, 분당 200회 / 주문 외 요청은 초당 30회, 분당 900회 사용 가능합니다.

# 업비트 access key, secret key 변수
upbit_access = "your_access_key"
upbit_secret = "your_secret_key"

# 코인 리스트
tickers = []
# 코인 종가 담을 deque 변수
ma20 = deque(maxlen=20)
ma60 = deque(maxlen=60)
ma120 = deque(maxlen=120)

# 원화로 매매 가능한 코인 리스트 만들기
tickers = pyupbit.get_tickers(fiat="KRW")

# login
upbit = pyupbit.Upbit(upbit_access, upbit_secret)

# 잔고 조회 krw
def get_balance_krw():
    balance = upbit.get_balance("KRW")
    return balance

# 코인 심볼 하나씩 받아와서 이동평균선 구한 후 매수 조건 탐색
def get_ticker_ma(ticker):

    '''get_ohlcv 함수는 고가/시가/저가/종가/거래량을 DataFrame으로 반환합니다'''
    df = pyupbit.get_ohlcv(ticker, interval='day') # 일봉 데이터 프레임 생성

    ma20.extend(df['close'])    # ma20 변수에 종가 넣기
    ma60.extend(df['close'])    # ma60 변수에 종가 넣기
    ma120.extend(df['close'])   # ma120 변수에 종가 넣기

    curr_ma20 = sum(ma20) / len(ma20)       # ma20값 더해서 나누기 = 20일선 이동평균
    curr_ma60 = sum(ma60) / len(ma60)       # ma60값 더해서 나누기 = 60일선 이동평균
    curr_ma120 = sum(ma120) / len(ma120)    # ma20값 더해서 나누기 = 120일선 이동평균

    now_price = pyupbit.get_current_price(ticker)       # 코인의 현재가
    open_price = df['open'][-1]                 # 당일 시가 구하기
    buy_target_price = open_price + (open_price * 0.02) # 목표가 = 당일 시가 보다 2프로 이상 상승 금액

    # 이동 평균선 정배열 / 목표가 보다 현재가  높을 경우 매수
    if curr_ma20 <= curr_ma60 and curr_ma60 <= curr_ma120 and buy_target_price <= now_price:
        # 50만원치 매수
        volume = round(500000 / now_price * 0.995, 4)
        buy_order(ticker, volume)
    else:
        print('시세 감시 중')
        pass

# 매수 주문
def buy_order(ticker, volume):
    try:
        while True:
            buy_result = upbit.buy_market_order(ticker, volume)
            if buy_result == None or 'error' in buy_result:
                print("매수 재 주문")
                time.sleep(1)
            else:
                return buy_result
    except:
        print("매수 주문 이상")

# 코인 리스트에서 이동 평균선 함수로 하나씩 꺼내서 보내기
while True:
    try:
        for tk in tickers:
            get_ticker_ma(tk)
            time.sleep(2)
    except:
        print('오류 발생 무시')
        pass