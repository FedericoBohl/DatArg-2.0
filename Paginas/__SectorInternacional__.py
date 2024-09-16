#from librerias import *
from _globals_ import *
import streamlit as st
from streamlit import session_state as S
import pandas as pd
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import requests
import io
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

@st.cache_resource(show_spinner=False)
def load_canasta(end):
    data={
        'ARS':[0.0692911639106725,'https://www.google.com/finance/quote/USD-ARS?hl=es',0.9998],
        'COP':[0.0604214503862096,'https://www.google.com/finance/quote/USD-COP?hl=es',1976.5],
        'BRL':[0.301541171878207,'https://www.google.com/finance/quote/USD-BRL?hl=es',1.784],
        'MXN':[0.484520491738942,'https://www.google.com/finance/quote/USD-MXN?hl=es',9.587],
        'CLP':[0.0842257220859683,'https://www.google.com/finance/quote/USD-CLP?hl=es',517.95]
        }
    total=0
    for i in data:
        response=requests.get(data[i][1])
        soup=BeautifulSoup(response.text, 'html.parser')
        _=soup.find('div', {'data-source': 'USD'})
        __=float(_.get_text().split(' ')[0].replace('.','').replace(',','.'))
        _=100*__/data[i][2]
        total+=__*data[i][0]
        data[i][1]=__
    df=pd.read_csv("His Data/his-canasta.csv",delimiter=';',index_col=0)
    df.index=pd.to_datetime(df.index,format='%d/%m/%Y')
    new_val=pd.DataFrame({df.columns[0]:[total]},index=[datetime.today()])
    df=pd.concat([df,new_val])
    return df,data

@st.cache_resource(show_spinner=False)
def get_eu(_) -> None:
    c1,c2,c3=st.columns((0.4,0.6/2,0.6/2),vertical_alignment='center')
    c1.header('Europa')
    
    mro=pd.read_csv('https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.MRR_FR.LEV?startPeriod=2000-01&detail=dataonly&format=csvdata')
    mro=mro[['TIME_PERIOD','OBS_VALUE']]
    mro.TIME_PERIOD=pd.to_datetime(mro.TIME_PERIOD, format='%Y-%m-%d')
    mro.set_index('TIME_PERIOD',inplace=True)
    mro=mro.rename(columns={'OBS_VALUE':'MRO'})
    mro_last=mro.iloc[-1]['MRO']
    index_last=mro.index[-1]
    mro=mro.resample('M').last()
    c2.metric(f"MRO ({index_last.strftime('%d-%b')})",f"{mro_last}%",f"{round(mro_last-mro.iloc[-2]['MRO'],2)}PP",delta_color="inverse")


    #mro.index=mro.index.strftime('%b-%Y') 

    inf=pd.read_csv('https://data-api.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.ANR?startPeriod=2000-01&detail=dataonly&format=csvdata')
    inf=inf[['TIME_PERIOD','OBS_VALUE']]
    inf.TIME_PERIOD=pd.to_datetime(inf.TIME_PERIOD, format='%Y-%m')
    inf.set_index('TIME_PERIOD',inplace=True)
    inf=inf.rename(columns={'OBS_VALUE':'Inflación'})
    with c3:st.metric(f"Inflación ({inf.index[-1].strftime('%b')})",f"{inf.iloc[-1]['Inflación']}%",f"{round(inf.iloc[-1]['Inflación']-inf.iloc[-2]['Inflación'],2)}PP",delta_color="inverse")
    #inf.index=inf.index.strftime('%b-%Y')


    une=pd.read_csv('https://data-api.ecb.europa.eu/service/data/LFSI/M.I9.S.UNEHRT.TOTAL0.15_74.T?startPeriod=2000-01&detail=dataonly&format=csvdata')
    une=une[['TIME_PERIOD','OBS_VALUE']]
    une.TIME_PERIOD=pd.to_datetime(une.TIME_PERIOD, format='%Y-%m')
    une.set_index('TIME_PERIOD',inplace=True)
    une=une.rename(columns={'OBS_VALUE':'Desempleo'})
    #une.index=une.index.strftime('%b-%Y')

    graph_eu,table_eu=st.tabs(['Gráfico','Tabla'])
    fig=make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=mro.index,y=mro['MRO'],name='MRO',line=dict(width=3,dash="dashdot"),marker_color="#FFDD00"),secondary_y=False)
    fig.add_trace(go.Bar(x=mro.index,y=inf['Inflación'],name="Inflación",marker_color="#001489"),secondary_y=False)
    fig.add_trace(go.Scatter(x=mro.index,y=une['Desempleo'],name='Desempleo',line=dict(width=2),marker_color='lime'),secondary_y=True)

    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1), legend=dict( 
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            bordercolor=black,
                            borderwidth=2
                        ),
                yaxis=dict(showgrid=False, zeroline=True, showline=True,title="% - Inflación/MRO"),
                yaxis2=dict(showgrid=False, zeroline=True, showline=True,title="% - Desempleo"),
                xaxis=dict(
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=6,
                                        label="6m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=1,
                                        label="1y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(count=5,
                                        label="5y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(step="all")
                                ])
                            ),
                            rangeslider=dict(
                                visible=True
                            )
                        )
                    )    
    with graph_eu:st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    mro.index=mro.index.strftime('%b-%Y')
    inf.index=inf.index.strftime('%b-%Y')
    une.index=une.index.strftime('%b-%Y')
    data=pd.concat([mro,inf],axis=1)
    data=pd.concat([data,une],axis=1)
    data.index.name='Fecha'
    with table_eu:st.dataframe(data,use_container_width=True)

@st.cache_resource(show_spinner=False)
def get_uk(_) -> None:
    c1,c2,c3=st.columns((0.4,0.6/2,0.6/2),vertical_alignment='center')
    with c1:st.header('Inglaterra')

    url = 'http://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp?csv.x=yes'
    payload = {
        'Datefrom'   : '01/Jan/2000',
        #'Dateto'     : '01/Oct/2018',
        'SeriesCodes': 'IUDBEDR',
        'CSVF'       : 'TN',
        'UsingCodes' : 'Y',
        'VPD'        : 'Y',
        'VFD'        : 'N'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/54.0.2840.90 '
                    'Safari/537.36'
    }
    response = requests.get(url, params=payload, headers=headers)
    tas = pd.read_csv(io.BytesIO(response.content),names=['Fecha','Tasa'],skiprows=1)
    tas['Fecha']=pd.to_datetime(tas['Fecha'], format='%d %b %Y')
    tas.set_index('Fecha',inplace=True)
    tas_last=tas.iloc[-1]['Tasa']
    index_last=tas.index[-1]
    tas=tas.resample('M').last()
    tas_t1=tas['Tasa'].iloc[-2]
    with c2:st.metric(f"Bank Rate ({index_last.strftime('%d-%b')})",f"{tas_last}%",f"{round(tas_last-tas_t1,2)}PP",delta_color="inverse")

    url='https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/l55o/mm23'
    response=requests.get(url)
    data = io.StringIO(response.text)
    inf = pd.read_csv(data,skiprows=316,names=['Fecha','Inflacion'])
    inf.columns=['Fecha','Inflacion']
    inf['Fecha']=pd.to_datetime(inf['Fecha'], format='%Y %b')
    inf.set_index('Fecha',inplace=True)
    inf_t=inf.iloc[-1]['Inflacion']
    inf_t1=inf.iloc[-2]['Inflacion']
    with c3:st.metric(f"Inflación ({inf.index[-1].strftime('%b')})",f"{inf_t}%",f"{round(inf_t-inf_t1,2)}PP",delta_color="inverse")

    url='https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms'
    response=requests.get(url)
    data = io.StringIO(response.text)
    une = pd.read_csv(data,skiprows=621,names=['Fecha','Inflacion'])
    une.columns=['Fecha','Desempleo']
    une['Fecha']=pd.to_datetime(une['Fecha'], format='%Y %b')
    une.set_index('Fecha',inplace=True)


    graph_uk,table_uk=st.tabs(['Gráfico','Tabla'])
    fig=make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=tas.index,y=tas['Tasa'],name='Bank Rate',line=dict(width=3,dash="dashdot"),marker_color="#C8102E"),secondary_y=False)
    fig.add_trace(go.Bar(x=tas.index,y=inf['Inflacion'],name="Inflación",marker_color="#012169"),secondary_y=False)
    fig.add_trace(go.Scatter(x=tas.index,y=une['Desempleo'],name='Desempleo',line=dict(width=2),marker_color=gray),secondary_y=True)

    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1), legend=dict( 
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            bordercolor=black,
                            borderwidth=2
                        ),
                yaxis=dict(showgrid=False, zeroline=True, showline=True,title="% - Inflación/Bank Rate"),
                yaxis2=dict(showgrid=False, zeroline=True, showline=True,title="% - Desempleo"),
                xaxis=dict(
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=6,
                                        label="6m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=1,
                                        label="1y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(count=5,
                                        label="5y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(step="all")
                                ])
                            ),
                            rangeslider=dict(
                                visible=True
                            )
                        )
                    )    
    with graph_uk:st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    tas.index=tas.index.strftime('%b-%Y')
    inf.index=inf.index.strftime('%b-%Y')
    une.index=une.index.strftime('%b-%Y')
    data=pd.concat([tas,inf.iloc[1:]],axis=1)
    data=pd.concat([data,une.iloc[1:]],axis=1)
    with table_uk:st.dataframe(data,use_container_width=True)

def make_usa(today):
    @st.cache_resource(show_spinner=False)
    def load_policy(_):
        fred = Fred(api_key="6050b935d2f878f1100c6f217cbe6753")
        cpi_data = fred.get_series('CPIAUCNS').loc[f'{1999}':]
        df_cpi = pd.DataFrame(cpi_data, columns=['Inflacion'])
        df_cpi['Inflacion']=round(df_cpi['Inflacion']/df_cpi['Inflacion'].shift(12) -1,4)*100
        df_cpi=df_cpi.dropna()
        unemployment_data = fred.get_series('UNRATE').loc[f'{2000}':]
        df_unemployment = pd.DataFrame(unemployment_data, columns=['Desempleo'])
        fed_funds_data = fred.get_series('FEDFUNDS').loc[f'{2000}':]
        df_fed_funds = pd.DataFrame(fed_funds_data, columns=['Tasa'])
        df_fed_funds.index=df_fed_funds.index.strftime('%b-%Y')
        df_cpi.index=df_cpi.index.strftime('%b-%Y')
        df_unemployment.index=df_unemployment.index.strftime('%b-%Y')
        data=pd.concat([df_fed_funds,df_cpi],axis=1)
        data=pd.concat([data,df_unemployment],axis=1)
        return data

    @st.cache_resource(show_spinner=False)
    def plot_policy(data):
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=data.index,y=data['Tasa'],name='FED',line=dict(width=3,dash="dashdot"),marker_color="#B31942"),secondary_y=False)
        fig.add_trace(go.Bar(x=data.index,y=data['Inflacion'],name="Inflación",marker_color="#0A3161"),secondary_y=False)
        fig.add_trace(go.Scatter(x=data.index,y=data['Desempleo'],name='Desempleo',line=dict(width=2),marker_color=lavender),secondary_y=True)

        fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1), legend=dict( 
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1,
                                bordercolor=black,
                                borderwidth=2
                            ),
                    yaxis=dict(showgrid=False, zeroline=True, showline=True,title="% - Inflación/Tasa de la FED"),
                    yaxis2=dict(showgrid=False, zeroline=True, showline=True,title="% - Desempleo"),
                    xaxis=dict(
                                rangeselector=dict(
                                    buttons=list([
                                        dict(count=6,
                                            label="6m",
                                            step="month",
                                            stepmode="backward"),
                                        dict(count=1,
                                            label="1y",
                                            step="year",
                                            stepmode="backward"),
                                        dict(count=5,
                                            label="5y",
                                            step="year",
                                            stepmode="backward"),
                                        dict(step="all")
                                    ])
                                ),
                                rangeslider=dict(
                                    visible=True
                                )
                            )
                        )    
        st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

    @st.cache_resource(show_spinner=False)
    def make_metrics(data):
        c1,c2,c3=st.columns((0.4,0.6/2,0.6/2),vertical_alignment='center')
        c1.header('EE.UU.')
        fed_t=data.dropna(subset = ['Tasa']).iloc[-1]['Tasa']
        fed_t1=data.dropna(subset = ['Tasa']).iloc[-2]['Tasa']
        c2.metric(f"Fed Funds Rate ({data.dropna(subset = ['Tasa']).index[-1].split('-')[0]})",f"{fed_t:.2f}%",f"{round(fed_t-fed_t1,2)}PP",delta_color="inverse")
        inf_t=data.dropna(subset = ['Inflacion']).iloc[-1]['Inflacion']
        inf_t1=data.dropna(subset = ['Inflacion']).iloc[-2]['Inflacion']
        c3.metric(f"Inflación ({data.dropna(subset = ['Inflacion']).index[-1].split('-')[0]})",f"{inf_t:.2f}%",f"{round(inf_t-inf_t1,2)}PP",delta_color="inverse")

    @st.cache_resource(show_spinner=False)
    def get_focm_rates(_):
        url='https://www.investing.com/central-banks/fed-rate-monitor'
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text,'html.parser')

        data={}
        tables = soup.find_all('div',class_="cardWrapper")
        for table in tables:
            date = table.find('div', class_='fedRateDate').get_text(strip=True)

            focm={}
            for tr in table.find_all('tr')[1:]:
                tds = tr.find_all('td')
                focm["-".join([str(num) for num in [int(float(i)*100) for i in tds[0].get_text(strip=True).split(' - ')]])]=[float(td.get_text(strip=True)[:-1]) for td in tds[1:]]
            
            _today_=datetime.strptime(" ".join(table.find('div', class_='fedUpdate').get_text(strip=True).split()[1:4]), '%b %d, %Y')
            _yest_=_today_-timedelta(days=1)
            _lastweek_=_today_-timedelta(days=7)
            focm=pd.DataFrame(focm).transpose()
            focm.columns=[_today_.strftime('%b %d, %Y'),_yest_.strftime('%b %d, %Y'),_lastweek_.strftime('%b %d, %Y')]
            data[date]=focm
        return data
    
    @st.cache_resource(show_spinner=False)
    def dot_plot(_):
        data=pd.read_csv('dotplot.csv')
        data.set_index('TARGET RATE',inplace=True)
        def generar_numeros(base, numero):
            mitad = numero // 2
            if numero % 2 != 0:  # Si es impar
                numeros=[]
                for i in range(1,1+mitad):
                    numeros.append(base+0.1*i)
                    numeros.append(base-0.1*i)
                numeros.append(base)
                numeros.sort()
            else:  # Si es par
                numeros=[]
                for i in range(1,1+mitad):
                    numeros.append(base+0.1*i-0.05)
                    numeros.append(base-0.1*i+0.05)
                numeros.sort()
            return numeros
        plot_dict={}
        for col in data.columns:
            plot_data={}
            if col=='Largo Plazo':
                year=int(data.columns[-2])+1
            else:
                year=int(col)
            year_data=data.dropna(subset=[col])[col]
            for val in year_data.index:
                plot_data[val]=generar_numeros(int(year),int(year_data[val]))
            plot_dict[col]=plot_data

        fig = go.Figure()
        for year, rates in plot_dict.items():
            for rate, votes in rates.items():
                fig.add_trace(go.Scatter(
                    x=votes,
                    y=[rate] * len(votes),
                    mode='markers',
                    marker=dict(size=10,color='navy'),
                    name=str(year)
                ))
        texts=[k for k in plot_dict.keys()]
        vals=[(int(k) if k!="Largo Plazo" else (int(texts[-2])+1)) for k in texts]
        fig.update_layout(
            title="Dot Plot del FOMC",
            plot_bgcolor='white',
            xaxis_title="Año",
            yaxis_title="Tasa de Interés (%)",
            showlegend=False,
            xaxis=dict(tickmode='array',tickvals=vals,ticktext=texts),
            yaxis=dict(range=[0,data.index.max().max()*1.1],showline=True, linewidth=0.5, linecolor='black',gridcolor='lightslategrey',gridwidth=0.35)
        )
        st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    
    def make_probabilities(data:dict):
        st.selectbox('Reunión del FOCM',options=list(data.keys()),key='focm_selected')
        prob_df=data[S.focm_selected]
        df=prob_df[prob_df.columns[0]]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=prob_df.index,
            y=prob_df[prob_df.columns[0]].values,
            marker_color='crimson',  # Color bordo
            text=[f'{value}%' for value in df.values],  # Mostrar valores en porcentaje
            textposition='outside',
            marker=dict(cornerradius="15%", line=dict(color='darkred', width=2)),
            visible=True  # Esta traza será visible inicialmente
        ))

        fig.add_trace(go.Bar(
            x=prob_df.index,
            y=prob_df[prob_df.columns[1]].values,
            marker_color='crimson',  # Color bordo
            text=[f'{value}%' for value in df.values],  # Mostrar valores en porcentaje
            textposition='outside',
            marker=dict(cornerradius="15%", line=dict(color='darkred', width=2)),
            visible=False  # Esta traza estará oculta inicialmente
        ))

        fig.add_trace(go.Bar(
            x=prob_df.index,
            y=prob_df[prob_df.columns[2]].values,
            marker_color='crimson',  # Color bordo
            text=[f'{value}%' for value in df.values],  # Mostrar valores en porcentaje
            textposition='outside',
            marker=dict(cornerradius="15%", line=dict(color='darkred', width=2)),
            visible=False  # Esta traza estará oculta inicialmente
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            yaxis=dict(range=[0, 100],showline=True, linewidth=2, linecolor='black',gridcolor='lightslategrey',gridwidth=0.35),
            title="Policy Rate esperada",
            xaxis_title="Tasa objetivo (Basis Points)",
            yaxis_title="Probabilidad",
            showlegend=False,
            )
        fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        active=0,
                        x=0.75,
                        xanchor='right',
                        y=1.3,
                        bgcolor='#f0f7ff',
                        bordercolor='#b3c7e6',
                        buttons=list([
                            dict(label="Hoy",
                                method="update",
                                args=[{"visible": [True,False,False]}]),
                            dict(label="Ayer",
                                method="update",
                                args=[{"visible": [False,True,False]}]),
                            dict(label="Hace una semana",
                                method="update",
                                args=[{"visible": [False,False,True]}])
                        ]),
                    )
                ])
        st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
        st.dataframe(prob_df,use_container_width=True)

    fed=load_policy(today)
    focm=get_focm_rates(today)
    make_metrics(fed)
    graph_usa,table_usa,probabilities,dotplot=st.tabs(['Gráfico','Tabla','Probabilidades de Tasa','Dot-Plot'])
    with graph_usa:plot_policy(fed)
    with table_usa: st.dataframe(fed,use_container_width=True)
    with dotplot: dot_plot(today)
    with probabilities: make_probabilities(focm)

@st.cache_resource(show_spinner=False)
def get_jp(_):
    c1,c2,c3=st.columns((0.4,0.6/2,0.6/2),vertical_alignment='center')
    with c1:st.header('Japón')
    #       Tasa de Interés
    url = 'https://www.stat-search.boj.or.jp/ssi/mtshtml/fm01_d_1_en.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    df = pd.read_html(io.StringIO(str(tables[0])))[0]
    df=df.iloc[7:]
    df.columns=['Fecha','Tasa']
    df.Fecha=pd.to_datetime(df.Fecha,format='%Y/%m/%d')
    df.set_index('Fecha',inplace=True)
    df['Tasa'] = df['Tasa'].str.replace(',', '').astype(float)
    df.dropna(inplace=True)
    jp_last=df.iloc[-1]['Tasa']
    index_last=df.index[-1]
    df=df.resample('M').last()
    df=df.loc['2000':]
    c2.metric(f"Call Overnight ({index_last.strftime('%d-%b')})",f"{jp_last}%",f"{round(jp_last-df.iloc[-2]['Tasa'],2)}PP",delta_color="inverse")
    rate=df.copy()
    
    #       Inflación
    url = 'https://www.stat-search.boj.or.jp/ssi/mtshtml/pr01_m_1_en.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    df = pd.read_html(io.StringIO(str(tables[0])))[0]
    df=df.iloc[7:][[0,1]]
    df.columns=['Fecha','Inflación']
    df.Fecha=pd.to_datetime(df.Fecha,format='%Y/%m')
    df.set_index('Fecha',inplace=True)
    df=df.loc['2000':]
    df.index = df.index.to_period('M').to_timestamp('M')
    df['Inflación'] = df['Inflación'].str.replace(',', '').astype(float)
    df.dropna(inplace=True)
    with c3:st.metric(f"Inflación ({df.index[-1].strftime('%b')})",f"{df.iloc[-1]['Inflación']}%",f"{round(df.iloc[-1]['Inflación']-df.iloc[-2]['Inflación'],2)}PP",delta_color="inverse")
    inf=df.copy()
    #       Desempleo
    url = "https://www.e-stat.go.jp/en/stat-search/file-download?statInfId=000031831365&fileKind=0"
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_excel(io.BytesIO(response.content))
    df=df.iloc[369:][df.columns[1:5]]
    df.index=pd.date_range(start='2000-01-01', periods=len(df), freq='M')
    df.columns=['1','2','3','Desempleo']
    df.drop(columns=['1','2','3'],inplace=True)
    df['Desempleo'] = pd.to_numeric(df['Desempleo'], errors='coerce')
    df = df.dropna()

    #   Plot y datos
    graph_jp,table_jp=st.tabs(['Gráfico','Tabla'])
    fig=make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=rate.index,y=rate['Tasa']*100,name='Call Overnight',line=dict(width=3,dash="dashdot"),marker_color="#BC002D"),secondary_y=False)
    fig.add_trace(go.Bar(x=inf.index,y=inf['Inflación'],name="Inflación",marker_color="#7A1CAC"),secondary_y=True)
    fig.add_trace(go.Scatter(x=df.index,y=df['Desempleo'],name='Desempleo',line=dict(width=2),marker_color='#3C3D37'),secondary_y=True)

    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1), legend=dict( 
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            bordercolor=black,
                            borderwidth=2
                        ),
                yaxis=dict(showgrid=False, zeroline=True, showline=True,title="Basis Points - Call Overnight"),
                yaxis2=dict(showgrid=False, zeroline=True, showline=True,title="% - Inflación/Desempleo"),
                xaxis=dict(
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=6,
                                        label="6m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=1,
                                        label="1y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(count=5,
                                        label="5y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(step="all")
                                ])
                            ),
                            rangeslider=dict(
                                visible=True
                            )
                        )
                    )    
    graph_jp.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    rate.index=rate.index.strftime('%b-%Y')
    inf.index=inf.index.strftime('%b-%Y')
    df.index=df.index.strftime('%b-%Y')
    data=pd.concat([rate['Tasa'],inf['Inflación']],axis=1)
    data=pd.concat([data,df['Desempleo']],axis=1)
    table_jp.dataframe(data,use_container_width=True)
    
    
def make_internacional_web():
    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):
            make_usa(datetime.now().strftime("%Y%m%d"))
            #get_usa(datetime.now().strftime("%Y%m%d"))
    with c2:
        with st.container(border=True):get_eu(datetime.now().strftime("%Y%m%d"))

    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):get_uk(datetime.now().strftime("%Y%m%d"))
    with c2:
        with st.container(border=True):get_jp(datetime.now().strftime("%Y%m%d"))
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center;'>Canasta de Monedas de Latam</h3>", unsafe_allow_html=True)
        df,fx=load_canasta(datetime.now().strftime("%Y%m%d"))
        df_men=df.pct_change()*100
        df_an=df.pct_change(periods=12)*100
        c1,c2=st.columns((0.6,0.4))
        with c1:
            fig=make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=df.index,y=df['Canasta'],marker_color=navy,line=dict(width=3.5),name='Índice'),secondary_y=True)
            fig.add_trace(go.Bar(x=df_men.index,y=df_men['Canasta'],marker_color=green,name='Var. Mensual'),secondary_y=False)
            fig.add_trace(go.Scatter(x=df_an.index,y=df_an['Canasta'],marker_color=lavender,name='Var. Interanual',line=dict(dash='dashdot',width=1.5)),secondary_y=False)
            fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1), legend=dict( 
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            bordercolor=black,
                            borderwidth=2
                        ),
                yaxis=dict(showgrid=False, zeroline=True, showline=True,title="%"),
                yaxis2=dict(showgrid=False, zeroline=True, showline=True,title="Índice"),
                xaxis=dict(
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=6,
                                        label="6m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=1,
                                        label="1y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(count=5,
                                        label="5y",
                                        step="year",
                                        stepmode="backward"),
                                    dict(step="all")
                                ])
                            ),
                            rangeslider=dict(
                                visible=True
                            )
                        )
                    )  
            st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
        with c2:
            c21,c22=st.columns(2)
            c21.metric('Argentina',f"{fx['ARS'][1]:.2f} USD",delta=f'Share: {(100*fx["ARS"][0]):.2f}%',delta_color='off')
            c22.metric('Brasil',f"{fx['BRL'][1]:.2f} USD",delta=f'Share: {(100*fx["BRL"][0]):.2f}%',delta_color='off')
            c21.metric('Colombia',f"{fx['COP'][1]:.2f} USD",delta=f'Share: {(100*fx["COP"][0]):.2f}%',delta_color='off')
            c22.metric('Chile',f"{fx['CLP'][1]:.2f} USD",delta=f'Share: {(100*fx["CLP"][0]):.2f}%',delta_color='off')
            c21.metric('México',f"{fx['MXN'][1]:.2f} USD",delta=f'Share: {(100*fx["MXN"][0]):.2f}%',delta_color='off')
        st.caption('El índice en en base Enero-2000=100 y las ponderaciones en base a la participación en el comercio mundial de cada año. La idea es crear una métrica que se asemeje al Broad Dolar Index pero con respecto a Latinoamérica.')