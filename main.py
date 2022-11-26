#2022-11-26
import requests

api_key = 'b64695f3f2a79d07bde772ffa630f935e0d050c0'

samsung = '00126380'

res = requests.get('https://opendart.fss.or.kr/api/company.json', params={'crtfc_key' : api_key, 'corp_code' : samsung})
res.raise_for_status()
print(res)
data = res.json()

print(data)