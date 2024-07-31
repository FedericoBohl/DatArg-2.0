import streamlit as st
import pandas as pd
import requests
from datetime import datetime,timedelta
#from streamlit_js_eval import streamlit_js_eval
#from streamlit_javascript import st_javascript
#from user_agents import parse
import streamlit.components.v1 as components

########################    Lottie Animation    #######################



#@st.cache_data()
#def page_info():
#    page_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',  want_output = True)
#    if page_width==None:page_width=2000
#    ua_string = st_javascript("""window.navigator.userAgent;""")
#    user_agent = parse(ua_string)
#    is_session_pc = not user_agent.is_mobile
#    return page_width,is_session_pc

def get_data(id:str|list[str],start_date:str,col_list:list[str]|str|None=None):
    now=datetime.now().strftime("%Y-%m-%d")
    if isinstance(id,list):
        link="https://apis.datos.gob.ar/series/api/series?ids="
        for i in id[:-1]:link+=f"{i},"
        link+=id[-1]
    else :link=f"https://apis.datos.gob.ar/series/api/series?ids={id}"
    result = requests.get(f"{link}&start_date={start_date}&end_date={now}").json()
    df=pd.DataFrame(result["data"])
    df.set_index(0,inplace=True)
    df.index = pd.to_datetime(df.index)
    while (df.index.max()<=datetime.strptime(now, "%Y-%m-%d")):
        try:
            __=(df.index.max()+timedelta(days=1)).strftime("%Y-%m-%d")
            _=requests.get(f"{link}&start_date={__}&end_date={now}").json()
            _=pd.DataFrame(_["data"])
            _.set_index(0,inplace=True)
            _.index = pd.to_datetime(_.index)
            df=pd.concat([df,_])
        except:break
    if isinstance(id, list):
        if isinstance(col_list, list) and len(id)==len(col_list):
            names={}
            for i in range(1,len(id)+1):
                names[i]=col_list[i-1]
            df.rename(columns=names,inplace=True)
        else:
            names={}
            for i in range(1,len(id)+1):
                names[i]=result["meta"][i]["field"]["description"]
            df.rename(columns=names,inplace=True)
    else:
        if isinstance(col_list, str):
            df.rename(columns={1:col_list},inplace=True)
        else:
            df.rename(columns={1:result["meta"][1]["field"]["description"]},inplace=True)
    return df[~df.index.duplicated(keep='first')]


########    Debería modificarse para que tome como ancla el ULTIMO valor del PBI real
@st.cache_data(show_spinner=False)
def get_pbi()->list:
    data=[450307.061,
    451549.5601,
    450180.8253,
    440397.1537,
    452623.3005,
    464034.4662,
    477195.8933,
    485623.35,
    488497.2797,
    495181.8567,
    499431.2304,
    494991.4836,
    513169.6373,
    522648.9433,
    531754.432,
    546349.5048,
    554877.5349,
    555242.8815,
    562857.8556,
    569639.5272,
    571952.2454,
    581715.0665,
    593272.4033,
    608695.1754,
    615988.7476,
    628466.8354,
    627383.2247,
    640254.5207,
    640873.2651,
    649344.0644,
    663103.4493,
    669176.6364,
    676463.1284,
    683225.0125,
    686843.1319,
    709405.7874,
    713307.6826,
    736797.2492,
    752550.5135,
    753135.7695,
    782686.6059,
    806147.8755,
    823476.2183,
    850780.1413,
    885121.0764,
    914314.9547,
    937174.5681,
    944128.3375,
    960924.6624,
    969358.191,
    986648.5299,
    1048324.388,
    1070322.5,
    1059696.493,
    1102932.805,
    1121146.326,
    1133563.054,
    1116498.914,
    1104762.654,
    1068182.198,
    1064677.617,
    1095193.53,
    1070821.983,
    1078313.126,
    1092229.985,
    1115189.547,
    1141681.474,
    1171914.475,
    1208709.579,
    1236714.424,
    1262078.507,
    1260282.94,
    1337188.139,
    1383921.97,
    1453265.605,
    1521319.545,
    1566580.331,
    1608471.89,
    1612818.172,
    1643726.414,
    1653162.766,
    1687190.425,
    1768767.21,
    1795856.46,
    1875083.17,
    1875023.225,
    1906620.65,
    1959770.277,
    2044560.836,
    2074787.654,
    2111381.057,
    2144991.616,
    2216840.393,
    2242418.353,
    2267198.381,
    2303664.724,
    2346588.291,
    2327835.72,
    2374564.287,
    2390115.947,
    2414940.255,
    2469347.764,
    2574397.593,
    2640792.361,
    2707208.869,
    2766484.861,
    2804075.994,
    2898941.031,
    2880495.146,
    2992240.837,
    3047948.966,
    3110037.171,
    3160271.11,
    3229307.983,
    3279754.613,
    3401234.258,
    3470471.961,
    3513887.548,
    3591115.972,
    3663754.656,
    3717272.943,
    3920872.062,
    4108277.164,
    4252079.443,
    4367892.088,
    4456874.787,
    4533561.087,
    4609430.66,
    4721371.042,
    4856391.275,
    4966187.451,
    5048569.401,
    5094363.738,
    5322796.503,
    5408367.666,
    5587558.983,
    5715233.607,
    5872127.721,
    5929211.574,
    6037733.964,
    6102365.883,
    6234954.585,
    6298928.692,
    6388976.382,
    6767132.235,
    7010425.041,
    7155706.146,
    7303549.679,
    7526530.841,
    7826523.093,
    7952991.063,
    8196487.581,
    8214331.992,
    8353292.78,
    8571413.265,
    8759941.882,
    8914553.954,
    9077093.479,
    9353093.413,
    9580212.874,
    9774062.635,
    10002822.33,
    10195567.08,
    10343076.96,
    10597447.98,
    10792032.12,
    10997459.42,
    11315902.88,
    11416778.78,
    11770258,
    11991591.92,
    11955172.68,
    12022780.74,
    12374305.15,
    12799710.31,
    13561294.62,
    14105620.49,
    14903603.09,
    15163021.57,
    15573345.91,
    16045871.81,
    16901324.92,
    17459931.76,
    18084714.22,
    18886553.52,
    19307051.26,
    20002604.72,
    20658386.89,
    21257303.07,
    22468400.74,
    22946604.03,
    23629869.93,
    24324758.07,
    24518076.57,
    22829797.23,
    19598676.33,
    22037869.2,
    23937303,
    24722994.45,
    25905953.27,
    27073512.8,
    28587761.97,
    29789921.08,
    31398006.04,
    33569526.93,
    34214648.33,
    36501677.62,
    37706822.04,
    38786904.7,
    40782690.76,
    42107798.63,
    43705126.55,
    45577814.71,
    47020360.16,
    49033837.15,
    52184329.22,
    53072375.01,
    56271293.35,
    59682735.43,
    64159198.96,
    67456962.95,
    71652940.63,
    76940851.72,
    81893396.13,
    86698819.4,
    91559097.13,
    95527930.16,
    99965140.81,
    107143103.5,
    114209398.6,
    122681703.4,
    130398339.1,
    138895970.6,
    147387587.7,
    159979201.3,
    181630312.3,
    205082861,
    221693473.9,
    246068095,
    299117957.8
    ]
    _=get_data(id=["145.3_INGNACNAL_DICI_M_15","143.3_NO_PR_2004_A_21"],start_date="2024-01-01")
    for i in range(len(_)):
        data.append(
            (_.iloc[i,1]*460369.442232949/100)*_.iloc[i,0]/7.72681211
        )
    return data


def create_widget(html_code,height,width):
    components.html(html_code,height=height,width=width)

w_calendar_tv="""<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://es.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Siga los mercados en TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
  {
  "colorTheme": "white",
  "isTransparent": true,
  "width": "100%",
  "height": "365",
  "locale": "es",
  "importanceFilter": "-1,0,1",
  "countryFilter": "ar",
  "backgroundColor": "#E8EBF3"

}
  </script>
</div>"""

w_barra_stocks="""<!-- TradingView Widget BEGIN -->
                <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
                {
                "symbols": [
                    {
                    "description": "S&Y 500",
                    "proName": "AMEX:SPY"
                    },
                    {
                    "description": "NASDAQ",
                    "proName": "NASDAQ:QQQ"
                    },
                    {
                    "description": "IBOVESPA",
                    "proName": "BMFBOVESPA:IBOV"
                    },
                    {
                    "description": "YPF",
                    "proName": "NYSE:YPF"
                    },
                    {
                    "description": "Galicia",
                    "proName": "NASDAQ:GGAL"
                    },
                    {
                    "description": "Banco BBVA",
                    "proName": "NYSE:BBAR"
                    },
                    {
                    "description": "Banco Macro",
                    "proName": "NYSE:BMA"
                    },
                    {
                    "description": "Banco Supervielle",
                    "proName": "NYSE:SUPV"
                    },
                    {
                    "description": "Edenor",
                    "proName": "NYSE:EDN"
                    },
                    {
                    "description": "Oro",
                    "proName": "TVC:GOLD"
                    },
                    {
                    "description": "Plata",
                    "proName": "TVC:SILVER"
                    },
                    {
                    "description": "Cobre",
                    "proName": "CAPITALCOM:COPPER"
                    },
                    {
                    "description": "Crudo WTI",
                    "proName": "BLACKBULL:WTI"
                    },
                    {
                    "description": "Crudo Brent",
                    "proName": "BLACKBULL:BRENT"
                    },
                    {
                    "description": "Trigo",
                    "proName": "CAPITALCOM:WHEAT"
                    },
                    {
                    "description": "Soja",
                    "proName": "CAPITALCOM:SOYBEAN"
                    },
                    {
                    "description": "Maíz",
                    "proName": "CAPITALCOM:CORN"
                    }
                ],
                "showSymbolLogo": true,
                "isTransparent": true,
                "displayMode": "compact",
                "colorTheme": "white",
                "locale": "es",
                "backgroundColor": "#E8EBF3"

                }
                </script>
                </div>
                <!-- TradingView Widget END -->"""


def add_gdp(df:pd.DataFrame)->pd.DataFrame:
    values=get_pbi()
    if len(df) == len(values):
        df['PBI'] = values
    else:
        if len(df) > len(values):
            values = list(values) + [None] * (len(df) - len(values))
        else:
            values = values[:len(df)]
        df['PBI'] = values
    return df