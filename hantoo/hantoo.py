# backtesting : https://www.quantconnect.com/
import pandas as pd
import matplotlib.pyplot as plt
import mojito
import os
from datetime import datetime,timezone,timedelta
'''
with open("./mock_api.key") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    acc_no = lines[2].strip()
    f.close()
'''
broker = mojito.KoreaInvestment(
    api_key = os.environ['mock_key'],
    api_secret = os.environ['mock_secret'],
    acc_no = os.environ['mock_acc_no'],
    mock=True
)

def get_total_evaluation() -> int:
    resp = broker.fetch_balance()
    return int(resp['output2'][0]['tot_evlu_amt'])

def get_avlb_amt() -> int:
    resp = broker.fetch_balance()
    return int(resp['output2'][0]['dnca_tot_amt'])

def get_base_price(code) -> int:
    resp = broker.fetch_price(code)
    return int(resp['output']['stck_sdpr'])

def get_curr_price(code) -> int:
    resp = broker.fetch_price(code)
    return int(resp['output']['stck_prpr'])

# print(resp['output']['per'], resp['output']['pbr'], resp['output']['prdy_ctrt'])
# symbols = broker.fetch_kospi_symbols() 코스피 심볼들 받아오기

def get_price_graph(code, dateType):
    """
    Date types format : "D" / "W" / "M"
    """

    resp = broker.fetch_ohlcv(
        symbol=code,
        timeframe=dateType,
        adj_price=True
    )
    # print(resp['output1']['hts_kor_isnm']) : 한글 종목명

    df = pd.DataFrame(resp['output2'])
    dt = pd.to_datetime(df['stck_bsop_date'], format="%Y%m%d")
    df.set_index(dt, inplace=True)
    df = df[['stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_clpr']]
    df.columns = ['open', 'high', 'low', 'close']
    df = df.apply(pd.to_numeric)
    df.index.name = "date"

    if dateType == "D":
        dateType = "Daily"
    elif dateType == "W":
        dateType = "Weekly"
    elif dateType == "M":
        dateType = "Monthly"

    graph = df['close'].plot(title=f"{code} {dateType}").get_figure()
    graph.savefig(f"{resp['output1']['hts_kor_isnm']}{dateType}.png")

def get_loss_cut_price(code, trade_type) -> float:
    """
    Trade types : "long" / "short"
    """
    # 금액별 호가 단위 반영 필요
    margin_rate = 0.01
    base = get_base_price(code)
    if trade_type == "long":
        loss_cut = base - (base * margin_rate)
    elif trade_type == "short":
        loss_cut = base + (base * margin_rate)
    return loss_cut

# offset time diff (UTC -> KST)
utc_time = datetime.utcnow()
timezone_kst = timezone(timedelta(hours=9))
kst_time = utc_time.astimezone(timezone_kst)

print("hii")
