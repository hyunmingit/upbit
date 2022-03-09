import pyupbit
import numpy as np

"""
하락장 일때 13이평선 정도는 유리할수 있으나 유의미한 차이는 없고,
대부분의 경우에는 MA조건 없이 실행하는것이 좋다.
"""

df = pyupbit.get_ohlcv("KRW-ETH", count=100) #count 만큼 당일 시가 고가 저가 종가 거래량 조회

# 변동폭 * k 계산, (고가-저가) * k 값
df['range'] = (df['high'] - df['low']) * 0.35

# target(매수가), range 컬럼을 한칸씩 밑으로 내림 (.shifht(1))
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.001

def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

#ror = 수익률 , np.where(조건문, 참일때 값, 거짓일 때 값)

ma20 = get_ma20("KRW-ETH")

df['ror'] = np.where( (df['high'] > df['target']) & (df['target'] > ma20),
                     df['close'] / df['target'] - fee,
                     1)
#누적 수익률
df['hpr'] = df['ror'].cumprod()

df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")