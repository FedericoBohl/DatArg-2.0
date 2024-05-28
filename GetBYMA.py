from librerias import *


def __convert_to_numeric_columns(df, columns):
    for col in columns:
        #df[col] = df[col].apply(lambda x: x.replace('.', '').replace(',','.') if isinstance(x, str) else x)
        df[col] = pd.to_numeric(df[col].apply(lambda x: np.nan if x == '-' else x))
    return df


#@st.cache_data(show_spinner=False)
def GetBYMA():
        try:
            __columns_filter=["description","symbol","price","variation","highValue","minValue","closingPrice"]
            __index_columns=["description","symbol","last","change","high","low","previous_close"]

            __securities_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last','close', 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'group']
            __filter_columns=["symbol","closingPrice","previousClosingPrice"]
            __numeric_columns = ['last', 'open', 'high', 'low', 'volume', 'turnover', 'operations', 'change', 'bid_size', 'bid', 'ask_size', 'ask', 'previous_close']

            __fixedIncome_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last','close', 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'group',"expiration"]
            __filter_columns_fixedIncome=["symbol","settlementType","quantityBid","bidPrice","offerPrice","quantityOffer","settlementPrice","closingPrice","imbalance","openingPrice","tradingHighPrice","tradingLowPrice","previousClosingPrice","volumeAmount","volume","numberOfOrders","tradeHour","securityType","maturityDate"]

            __s = requests.session()
            __s.get('https://open.bymadata.com.ar/#/dashboard', verify=False)

            __headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                'sec-ch-ua-platform': '"Windows"',
                'Origin': 'https://open.bymadata.com.ar',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://open.bymadata.com.ar/',
                'Accept-Language': 'es-US,es-419;q=0.9,es;q=0.8,en;q=0.7',
            }
            response = __s.get('https://open.bymadata.com.ar/assets/api/langs/es.json', headers=__headers)
            __diction=json.loads(response.text)

            try:
                data = '{"Content-Type":"application/json"}'
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/index-price', headers=__headers, data=data, verify=False)
                indices = json.loads(response.text)['data']
                df = pd.DataFrame(indices)
                df = df[__columns_filter].copy()
                df.columns = __index_columns
                df_indice=df
            except: df_indice=None

            try:
                data = '{"excludeZeroPxAndQty":false,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/leading-equity', headers=__headers, data=data)
                panel_acciones_lideres = json.loads(response.text)
                df= pd.DataFrame(panel_acciones_lideres['data'])
                df = df[__filter_columns].copy()
                df.columns = __securities_columns
                try:
                    df['change']=df['close']/df['previous_close']-1
                except: df['change']=None
                df.set_index('symbol', inplace=True)
                df[~df.index.duplicated(keep='first')]
                df_merval=df
            except: df_merval=None

            try:
                data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/general-equity', headers=__headers, data=data)
                panel = json.loads(response.text)
                df= pd.DataFrame(panel['data'])
                df = df[__filter_columns].copy()
                df.columns = __securities_columns
                df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
                df = __convert_to_numeric_columns(df, __numeric_columns)
                df.set_index('symbol', inplace=True)
                df_general= df
            except: df_general=None
            
            try:
                data = '{"excludeZeroPxAndQty":false,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/cedears', headers=__headers, data=data)
                panel = json.loads(response.text)
                df= pd.DataFrame(panel)
                df = df[__filter_columns].copy()
                df.columns=['symbol','close','previous_close']
                try:
                    df['change']=df['close']/df['previous_close']-1
                except: df['change']=None
                #df.set_index('symbol', inplace=True)   #Para que pueda filtrar el threemap
                df=df.drop_duplicates(subset='symbol', keep='first')
                df_cedears= df
            except: df_cedears=None

            try:
                data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/public-bonds', headers=__headers, data=data)
                panel = json.loads(response.text)
                df = pd.DataFrame(panel['data'])
                df = df[__filter_columns_fixedIncome].copy()
                df.columns = __fixedIncome_columns
                df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
                df.expiration=pd.to_datetime(df.expiration)
                df = __convert_to_numeric_columns(df, __numeric_columns)
                df.set_index('symbol', inplace=True)
                df_bonos_gob= df
            except: df_bonos_gob=None

            try:
                data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/lebacs', headers=__headers, data=data)
                panel_letras = json.loads(response.text)
                df = pd.DataFrame(panel_letras['data'])
                numeric_columns = ['last', 'open', 'high', 'low', 'volume', 'turnover', 'operations', 'change', 'bid_size', 'bid', 'ask_size', 'ask', 'previous_close']
                filter_columns_fixedIncome=["symbol","settlementType","quantityBid","bidPrice","offerPrice","quantityOffer","settlementPrice","closingPrice","imbalance","openingPrice","tradingHighPrice","tradingLowPrice","previousClosingPrice","volumeAmount","volume","numberOfOrders","securityType","maturityDate","denominationCcy"]
                df = df[filter_columns_fixedIncome].copy()
                fixedIncome_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last', 'close' ,'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'group',"expiration","currency"]
                df.columns = fixedIncome_columns
                df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')

                df.expiration=pd.to_datetime(df.expiration)
                df = __convert_to_numeric_columns(df, numeric_columns)
                df.set_index('symbol', inplace=True)
                df_letras= df      
            except: df_letras=None

            try:
                data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/negociable-obligations', headers=__headers, data=data)
                panel_ons = json.loads(response.text)
                df= pd.DataFrame(panel_ons)
                df = df[__filter_columns_fixedIncome].copy()
                df.columns = __fixedIncome_columns
                df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
                df.expiration=pd.to_datetime(df.expiration)
                df = __convert_to_numeric_columns(df, __numeric_columns)
                df.set_index('symbol', inplace=True)
                df[~df.index.duplicated(keep='first')]
                df_bonos_cor= df
            except: df_bonos_cor=None

            try: 
                data = '{"page_number":1, "page_size":500, "Content-Type":"application/json"}'
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/bnown/seriesHistoricas/iamc/bonos', headers=__headers, data=data)
                bonos_iamc = json.loads(response.text)
                df_bonos_iamc = pd.DataFrame(bonos_iamc['data'])
                colList=df_bonos_iamc.columns.values
                error=0
                for i in range(len(colList)):
                    try:
                        colList[i]=__diction[colList[i]]
                    except:
                        error=error+1
                df_bonos_iamc.columns=colList
                df_iamc= df_bonos_iamc.drop(["notas"],axis=1)
                df_iamc.set_index('Especie', inplace=True)
                df_iamc[~df_iamc.index.duplicated(keep='first')]
                
            except: df_iamc=None

            return df_indice,df_bonos_gob,df_letras,df_bonos_cor,df_merval,df_general,df_cedears,df_iamc
        except:
             st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
