import time

import pyupbit
import numpy as np
import requests

url = "https://api.upbit.com/v1/candles/minutes/1"

querystring = {"market":"KRW-ETH","count":"200"}

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)

price = response.json()

print(price)
print(price[0]['low_price'])



def get_ror(k=0.5):
    range = price[0]['high_price'] -price[0]['low_price']*k
    target = price[1]['opening_price'] + range


    fee = 0.001
    df['ror'] = np.where(price[1]['high_price'] > target,
                         price[1]['trade_price'] / target - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.05):
    ror = get_ror(k)
    print("%.2f %f" % (k, ror))
    time.sleep(0.2)