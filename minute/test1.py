import requests

url = "https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=2"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

res = response.text

print(response.text)