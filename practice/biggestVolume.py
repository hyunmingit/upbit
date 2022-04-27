import time
import pyupbit as ub
import datetime
import requests
import pandas as pd

"""
access = "RLiPx3Sw77GaJmGJF0jiEx5ex3C2tk3BoRZoKELC"
secret = "jbDUQl89zUoUxVWqlFdn6ziWTwpcoBTz1sBpJGva"

뭐가 순서가 안맞음 이유는 모름
biggest + 1을 해야 맞는데 왜 맞는지 모르겠음 왜지
"""
url = "https://api.upbit.com/v1/market/all"
resp = requests.get(url)
data = resp.json()





tickers = ub.get_tickers(fiat='KRW') #원화 마켓 코인 목록 받아오기
volumes = []
for ticker in tickers:
    df = ub.get_ohlcv(ticker, interval="hour", count=24)
    volumes.insert(-1,round(df.iloc[-1]["value"])) #거래대금 목록에 추가
    print(ticker)
    print(round(df.iloc[-1]["value"]))

    time.sleep(0.1)
    #print("working...")


#print(volumes)
tmp = max(volumes)
biggest = volumes.index(tmp)

print("tickers[biggest] : ",tickers[biggest])
print("biggest : " ,biggest)
print("len(tickers) : ",len(tickers))
print("len(volumes) : ", len(volumes))
print("doge index : ", tickers.index("KRW-DOGE"))

print("result : ", tickers[biggest + 1])

