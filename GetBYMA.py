import json
import datetime
import requests
import urllib3
import numpy as np
import pandas as pd
from pytz import timezone
import streamlit as st


def __convert_to_numeric_columns(df, columns):
    for col in columns:
        #df[col] = df[col].apply(lambda x: x.replace('.', '').replace(',','.') if isinstance(x, str) else x)
        df[col] = pd.to_numeric(df[col].apply(lambda x: np.nan if x == '-' else x))
    return df


@st.cache_data()
def GetBYMA():
        __columns_filter=["description","symbol","price","variation","highValue","minValue","previousClosingPrice"]
        __index_columns=["description","symbol","last","change","high","low","previous_close"]

        __securities_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last','close', 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'group']
        __filter_columns=["symbol","settlementType","quantityBid","bidPrice","offerPrice","quantityOffer","settlementPrice","closingPrice","imbalance","openingPrice","tradingHighPrice","tradingLowPrice","previousClosingPrice","volumeAmount","volume","numberOfOrders","tradeHour","securityType"]
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


        data = '{"Content-Type":"application/json"}'
        response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/index-price', headers=__headers, data=data, verify=False)
        indices = json.loads(response.text)['data']
        df = pd.DataFrame(indices)
        df = df[__columns_filter].copy()
        df.columns = __index_columns
        df_indice=df

        data = '{"excludeZeroPxAndQty":false,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/leading-equity', headers=__headers, data=data)
        panel_acciones_lideres = json.loads(response.text)
        df= pd.DataFrame(panel_acciones_lideres['data'])
        df = df[__filter_columns].copy()
        df.columns = __securities_columns
        df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
        df = __convert_to_numeric_columns(df, __numeric_columns)
        df_merval=df

        data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/general-equity', headers=__headers, data=data)
        panel = json.loads(response.text)
        df= pd.DataFrame(panel['data'])
        df = df[__filter_columns].copy()
        df.columns = __securities_columns
        df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
        df = __convert_to_numeric_columns(df, __numeric_columns)
        df_general= df

        data = '{"excludeZeroPxAndQty":false,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/cedears', headers=__headers, data=data)
        panel = json.loads(response.text)
        df= pd.DataFrame(panel)
        df = df[__filter_columns].copy()
        df.columns = __securities_columns
        df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
        df = __convert_to_numeric_columns(df, __numeric_columns)
        df_cedears= df


        data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/public-bonds', headers=__headers, data=data)
        panel = json.loads(response.text)
        df = pd.DataFrame(panel['data'])
        df = df[__filter_columns_fixedIncome].copy()
        df.columns = __fixedIncome_columns
        df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
        df.expiration=pd.to_datetime(df.expiration)
        df = __convert_to_numeric_columns(df, __numeric_columns)
        df_bonos_gob= df

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
        df_letras= df      

        data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/negociable-obligations', headers=__headers, data=data)
        panel_ons = json.loads(response.text)
        df= pd.DataFrame(panel_ons)
        df = df[__filter_columns_fixedIncome].copy()
        df.columns = __fixedIncome_columns
        df.settlement = df.settlement.apply(lambda x: __diction[x] if x in __diction else '')
        df.expiration=pd.to_datetime(df.expiration)
        df = __convert_to_numeric_columns(df, __numeric_columns)
        df_bonos_cor= df
    
        #No estoy seguro que son
        data = '{"page_number":1, "page_size":500, "Content-Type":"application/json"}'
        response = __s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/bnown/seriesHistoricas/iamc/bonos', headers=__headers, data=data)
        st.write(__diction)
        bonos_iamc = json.loads(response.text)
        df_bonos_iamc = pd.DataFrame(bonos_iamc['data'])
        st.write(df_bonos_iamc)
        colList=df_bonos_iamc.columns.values
        error=0
        st.write(colList)
        st.divider()
        for i in range(len(colList)):
            try:
                colList[i]=__diction[colList[i]]
                st.write(__diction[colList[i]])
            except:
                error=error+1
        st.divider()
        df_bonos_iamc.columns=colList
        df_iamc= df_bonos_iamc.drop(["notas"],axis=1)
        return df_indice,df_bonos_gob,df_letras,df_bonos_cor,df_merval,df_general,df_cedears,df_iamc

