#from librerias import *
import pandas as pd
import requests
import numpy as np
import json

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

            __securities_columns = ['Nombre', 'Precio', 'Var%', 'Volumen']
            __filter_columns=["symbol","closingPrice","imbalance",'volume']
            __numeric_columns = ['last', 'open', 'high', 'low', 'volume', 'turnover', 'operations', 'change', 'bid_size', 'bid', 'ask_size', 'ask', 'previous_close']

            __fixedIncome_columns = ['Nombre', 'Var%', 'Fecha de madurez', 'Moneda', 'Volumen', 'Días hasta la maturity', 'Precio','Cantidad Ofrecida']
            __filter_columns_fixedIncome=["symbol","imbalance","maturityDate","denominationCcy","volume","daysToMaturity","closingPrice",'quantityOffer']

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
                data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
                response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/negociable-obligations', headers=__headers, data=data)
                panel_ons = json.loads(response.text)
                df= pd.DataFrame(panel_ons)
                df = df[__filter_columns_fixedIncome].copy()
                df.columns = __fixedIncome_columns
                df.set_index('Nombre', inplace=True)
                df=df[~df.index.duplicated(keep='first')]
                df_bonos_cor= df[['Precio','Var%','Moneda','Fecha de madurez', 'Días hasta la maturity', 'Volumen','Cantidad Ofrecida']]
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
                df_iamc=df_iamc.drop(columns=['Hora','Fecha de Cotización'])
                df_iamc=df_iamc.rename(columns={'Moneda de emisión':'Nombre Completo'})

                
            except: df_iamc=None

            return df_bonos_cor,df_iamc
        except:
             pass
             #st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
