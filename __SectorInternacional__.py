from librerias import *

@st.cache_resource(show_spinner=False)
def get_eu():
    mro=pd.read_csv('https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.MRR_FR.LEV?startPeriod=2000-01&detail=dataonly&format=csvdata')
    mro=mro[['TIME_PERIOD','OBS_VALUE']]
    mro.TIME_PERIOD=pd.to_datetime(mro.TIME_PERIOD, format='%Y-%m-%d')
    mro.set_index('TIME_PERIOD',inplace=True)
    mro=mro.resample('M').last()
    mro=mro.rename(columns={'OBS_VALUE':'MRO'})
    mro.index=mro.index.strftime('%b-%Y')


    inf=pd.read_csv('https://data-api.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.ANR?startPeriod=2000-01&detail=dataonly&format=csvdata')
    inf=inf[['TIME_PERIOD','OBS_VALUE']]
    inf.TIME_PERIOD=pd.to_datetime(inf.TIME_PERIOD, format='%Y-%m')
    inf.set_index('TIME_PERIOD',inplace=True)
    inf=inf.rename(columns={'OBS_VALUE':'Inflacion'})
    inf.index=inf.index.strftime('%b-%Y')


    une=pd.read_csv('https://data-api.ecb.europa.eu/service/data/LFSI/M.I9.S.UNEHRT.TOTAL0.15_74.T?startPeriod=2000-01&detail=dataonly&format=csvdata')
    une=une[['TIME_PERIOD','OBS_VALUE']]
    une.TIME_PERIOD=pd.to_datetime(une.TIME_PERIOD, format='%Y-%m-%d')
    une.set_index('TIME_PERIOD',inplace=True)
    une=une.rename(columns={'OBS_VALUE':'Desempleo'})
    une.index=une.index.strftime('%b-%Y')
    return mro,inf,une

def make_internacional():
    with st.container(border=True):
        c1,c2,c3=st.columns(3)
        with c1: st.metric('Precio WTI','-')
        with c2: st.metric('Precio Trigo','-')
        with c3: st.metric('Precio Soja','-')

    c1,c2=st.columns(2)
    with c1:
        st.title('EEUU')
    with c2:
        st.title('Europa')
    c1,c2=st.columns(2)
    with c1:
        st.title('EEUU')
    with c2:
        st.title('Europa')