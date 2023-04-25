import pandas as pd
import matplotlib.pyplot as plt
import mojito

key = ""
secret =  ""
acc_no = ""

broker = mojito.KoreaInvestment(
    api_key = key,
    api_secret = secret,
    acc_no = acc_no,
    mock=True
)

def get_total_evaluation():
    resp = broker.fetch_balance()
    return int(resp['output2'][0]['tot_evlu_amt'])

def get_avlb_amt():
    resp = broker.fetch_balance()
    return int(resp['output2'][0]['dnca_tot_amt'])

def get_base_price(code):
    resp = broker.fetch_price(code)
    return int(resp['output']['stck_sdpr'])

def get_curr_price(code):
    resp = broker.fetch_price(code)
    return int(resp['output']['stck_prpr'])

# print(resp['output']['per'], resp['output']['pbr'], resp['output']['prdy_ctrt'])
# symbols = broker.fetch_kospi_symbols() 코스피 심볼들 받아오기

def get_price_graph(code, dateType):
    resp = broker.fetch_ohlcv(
        symbol=code,
        timeframe=dateType,
        adj_price=True
    )
    #print(resp['output1']['hts_kor_isnm'])

    df = pd.DataFrame(resp['output2'])
    dt = pd.to_datetime(df['stck_bsop_date'], format="%Y%m%d")
    df.set_index(dt, inplace=True)
    df = df[['stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_clpr']]
    df.columns = ['open', 'high', 'low', 'close']
    #pd.to_numeric(df['close'], errors='ignore')
    df = df.apply(pd.to_numeric)
    df.index.name = "date"

    if dateType == "D":
        dateType = "Daily"
    elif dateType == "W":
        dateType = "Weekly"
    elif dateType == "M":
        dateType = "Monthly"

    graph = df['close'].plot(title=code+' '+dateType).get_figure()
    graph.savefig("%s%s.png"%(resp['output1']['hts_kor_isnm'], dateType))

# broker.create_limit_buy_order(    
#     symbol="005930",
#     price=65000,
#     quantity=1
# )

# a = get_total_evaluation()
# b = get_avlb_amt()
# print(a, b)

# resp = broker.fetch_price("005930")
# print(resp)


