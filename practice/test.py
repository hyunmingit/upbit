import pyupbit

access = "vPTsY97GkPAhQcbvfx3OXeyHQgEQVfmiTYdHQ8gQ"          # 본인 값으로 변경
secret = "Rua7oyeKTenNW2JCHMJNVSEdvdjzWgqDJcQnjB1p"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회