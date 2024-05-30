from librerias import *

@st.cache_resource(show_spinner=False)
def get_eu(_) -> None:
    c1,c2=st.columns((0.3,0.7))
    with c1:st.header('Europa')
    with c2:
        with st.container():
            c21,c22=st.columns(2)
    mro=pd.read_csv('https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.MRR_FR.LEV?startPeriod=2000-01&detail=dataonly&format=csvdata')
    mro=mro[['TIME_PERIOD','OBS_VALUE']]
    mro.TIME_PERIOD=pd.to_datetime(mro.TIME_PERIOD, format='%Y-%m-%d')
    mro.set_index('TIME_PERIOD',inplace=True)
    st.write(mro[-1])
    mro=mro.resample('M').median()
    mro=mro.rename(columns={'OBS_VALUE':'MRO'})
    #mro.index=mro.index.strftime('%b-%Y') 

    inf=pd.read_csv('https://data-api.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.ANR?startPeriod=2000-01&detail=dataonly&format=csvdata')
    inf=inf[['TIME_PERIOD','OBS_VALUE']]
    inf.TIME_PERIOD=pd.to_datetime(inf.TIME_PERIOD, format='%Y-%m')
    inf.set_index('TIME_PERIOD',inplace=True)
    inf=inf.rename(columns={'OBS_VALUE':'Inflación'})
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
    fig.add_trace(go.Bar(x=mro.index,y=inf['Inflación'],name="Infl. Interanual",marker_color="#001489"),secondary_y=False)
    fig.add_trace(go.Scatter(x=mro.index,y=une['Desempleo'],name='Tasa de Desempleo',line=dict(width=2),marker_color='lime'),secondary_y=True)

    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),height=450, legend=dict( 
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            bordercolor=black,
                            borderwidth=2
                        ),
                yaxis=dict(showgrid=False, zeroline=True, showline=True,title="% - Inflación"),
                yaxis2=dict(showgrid=False, zeroline=True, showline=True,title="% - Tasa"),
                xaxis=dict(
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=6,
                                        label="6m",
                                        step="month",
                                        stepmode="backward"),
                                    dict(count=1,
                                        label="YTD",
                                        step="year",
                                        stepmode="todate"),
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

def make_internacional():
    with st.container(border=True):
        c1,c2,c3=st.columns(3)
        with c1: st.metric('Precio WTI','-')
        with c2: st.metric('Precio Trigo','-')
        with c3: st.metric('Precio Soja','-')

    c1,c2=st.columns(2)
    with c1:
        st.header('EEUU')
    with c2:
        st.header('Europa')
        get_eu(datetime.now().strftime("%Y%m%d"))

    c1,c2=st.columns(2)
    with c1:
        st.header('Inglaterra')
    with c2:
        st.header('Japón')
    c1,c2=st.columns(2)
    with c1:
        st.header('Brasil')
    with c2:
        st.header('México')