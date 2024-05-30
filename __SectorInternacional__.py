from librerias import *
jp_id='7e63dd6ff7421e096fbdcf688af7b2c8ad69d814'

@st.cache_resource(show_spinner=False)
def get_eu(_) -> None:
    c1,c2,c3=st.columns((0.3,0.7/2,0.7/2))
    with c1:st.header('Europa')
    mro=pd.read_csv('https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.MRR_FR.LEV?startPeriod=2000-01&detail=dataonly&format=csvdata')
    mro=mro[['TIME_PERIOD','OBS_VALUE']]
    mro.TIME_PERIOD=pd.to_datetime(mro.TIME_PERIOD, format='%Y-%m-%d')
    mro.set_index('TIME_PERIOD',inplace=True)
    mro=mro.rename(columns={'OBS_VALUE':'MRO'})
    mro=mro.resample('M').last()
    with c2:st.metric(f'MRO ({mro.index[-1].strftime('%d-%b')})',f'{mro.iloc[-1]['MRO']}%',f'{round(mro.iloc[-1]['MRO']-mro.iloc[-2]['MRO'],2)}PP',delta_color="inverse")


    #mro.index=mro.index.strftime('%b-%Y') 

    inf=pd.read_csv('https://data-api.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.ANR?startPeriod=2000-01&detail=dataonly&format=csvdata')
    inf=inf[['TIME_PERIOD','OBS_VALUE']]
    inf.TIME_PERIOD=pd.to_datetime(inf.TIME_PERIOD, format='%Y-%m')
    inf.set_index('TIME_PERIOD',inplace=True)
    inf=inf.rename(columns={'OBS_VALUE':'Inflación'})
    with c3:st.metric(f'Inflación ({inf.index[-1].strftime('%b')})',f'{inf.iloc[-1]['Inflación']}%',f'{round(inf.iloc[-1]['Inflación']-inf.iloc[-2]['Inflación'],2)}PP',delta_color="inverse")
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
    with graph_eu:st.plotly_chart(fig)
    mro.index=mro.index.strftime('%b-%Y')
    inf.index=inf.index.strftime('%b-%Y')
    une.index=une.index.strftime('%b-%Y')
    data=pd.merge(mro,inf,left_index=True,right_index=True)
    data=pd.merge(data,une,left_index=True,right_index=True)
    data.index.name='Fecha'
    with table_eu:st.dataframe(data,use_container_width=True)

@st.cache_resource(show_spinner=False)
def get_uk(_) -> None:
    c1,c2,c3=st.columns((0.4,0.6/2,0.6/2))
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
    tas=tas.resample('M').median()
    tas_t=tas['Tasa'].iloc[-1]
    tas_t1=tas['Tasa'].iloc[-2]
    with c2:st.metric(f'Bank Rate ({tas.index[-1].strftime('%d-%b')})',f'{tas_t}%',f'{round(tas_t-tas_t1,2)}PP',delta_color="inverse")

    url='https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/l55o/mm23'
    response=requests.get(url)
    data = io.StringIO(response.text)
    inf = pd.read_csv(data,skiprows=316,names=['Fecha','Inflacion'])
    inf.columns=['Fecha','Inflacion']
    inf['Fecha']=pd.to_datetime(inf['Fecha'], format='%Y %b')
    inf.set_index('Fecha',inplace=True)
    inf_t=inf.iloc[-1]['Inflacion']
    inf_t1=inf.iloc[-2]['Inflacion']
    with c3:st.metric(f'Inflación ({inf.index[-1].strftime('%b')})',f'{inf_t}%',f'{round(inf_t-inf_t1,2)}PP',delta_color="inverse")

    url='https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms'
    response=requests.get(url)
    data = io.StringIO(response.text)
    une = pd.read_csv(data,skiprows=621,names=['Fecha','Inflacion'])
    une.columns=['Fecha','Desempleo']
    une['Fecha']=pd.to_datetime(une['Fecha'], format='%Y %b')
    une.set_index('Fecha',inplace=True)


    graph_eu,table_eu=st.tabs(['Gráfico','Tabla'])
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
    with graph_eu:st.plotly_chart(fig)
    tas.index=tas.index.strftime('%b-%Y')
    inf.index=inf.index.strftime('%b-%Y')
    une.index=une.index.strftime('%b-%Y')
    data=pd.merge(tas,inf,left_index=True,right_index=True)
    data=pd.merge(data,une,left_index=True,right_index=True)
    with table_eu:st.dataframe(data,use_container_width=True)

@st.cache_resource(show_spinner=False)
def get_usa(_):
    fred = Fred(api_key="6050b935d2f878f1100c6f217cbe6753")
    cpi_data = fred.get_series('CPIAUCNS').loc[f'{1999}':]
    df_cpi = pd.DataFrame(cpi_data, columns=['Inflacion'])
    df_cpi['Inflacion']=(df_cpi['Inflacion']/df_cpi['Inflacion'].shift(12) -1)*100
    df_cpi=df_cpi.dropna()
    unemployment_data = fred.get_series('UNRATE').loc[f'{2000}':]
    df_unemployment = pd.DataFrame(unemployment_data, columns=['Desempleo'])
    fed_funds_data = fred.get_series('FEDFUNDS').loc[f'{2000}':]
    df_fed_funds = pd.DataFrame(fed_funds_data, columns=['Tasa de la FED'])
    st.write(df_cpi)

def make_internacional():
    with st.container(border=True):
        c1,c2,c3=st.columns(3)
        with c1: st.metric('Precio WTI','-')
        with c2: st.metric('Precio Trigo','-')
        with c3: st.metric('Precio Soja','-')

    c1,c2=st.columns(2)
    with c1:
        st.header('EEUU')
        get_usa()
    with c2:
        with st.container(border=True):get_eu(datetime.now().strftime("%Y%m%d"))

    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):get_uk(datetime.now().strftime("%Y%m%d"))
    with c2:
        st.header('Japón')
    c1,c2=st.columns(2)
    with c1:
        st.header('Brasil')
    with c2:
        st.header('Nueva Zelanda')