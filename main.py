#2022-11-26

"""
- 기업가치 = 자기자본 + (초과이익/할인율)
: 자기자본 = 지배기업소유주지분(지배주주지분)
: 할인율 = BBB- 등급 회사채 5년 수익률 (매일 갱신) https://www.kisrating.com/ratingsStatistics/statics_spread.do
: 초과이익 = 자기자본 * (가중평균 3년 ROE - 할인율)
- 적정주가 = 기업가치 / 유통주식수

"""

import requests

api_key = 'b64695f3f2a79d07bde772ffa630f935e0d050c0'

samsung = '00126380'

#res = requests.get('https://opendart.fss.or.kr/api/company.json', params={'crtfc_key' : api_key, 'corp_code' : samsung})
res = requests.get('https://www.fnspace.com/Api/FinanceApi?key=sample&format=json&code=A005930&item=M111000,M111100,M111600,M113000&consolgb=M&annualgb=A&fraccyear=2014&toaccyear=2018')
res.raise_for_status()
print(res)
data = res.json()

print(data)