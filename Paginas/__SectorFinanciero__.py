#from GetBYMA import GetBYMA
from Docta import DoctaCap
from _globals_ import *
import streamlit as st
from streamlit import session_state as S
import pandas as pd
from Paginas.librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import requests
import numpy as np

@st.cache_data(show_spinner=False)
def make_cedears(data_now : pd.DataFrame):
    with st.container(border=True):
        c1,c2,c3,c4,c5=st.columns(5)
        with c1:
            st.metric('SPY (ARS)',data_now.loc[data_now['Nombre']=='SPY','Precio'].values[0],f"{data_now.loc[data_now['Nombre']=='SPY','Var%'].values[0]*100:.2f}%")
        with c2:
            st.metric('NASDAQ (ARS)',data_now.loc[data_now['Nombre']=='QQQ','Precio'].values[0],f"{data_now.loc[data_now['Nombre']=='QQQ','Var%'].values[0]*100:.2f}%")
        with c3:
            st.metric('Down Jones (ARS)',data_now.loc[data_now['Nombre']=='DIA','Precio'].values[0],f"{data_now.loc[data_now['Nombre']=='DIA','Var%'].values[0]*100:.2f}%")
        with c4:
            st.metric('Dólar Oficial','-')
        with c5:
            st.metric('Dolar Blue/MEP/CCL','-')
    data=pd.read_csv('data_bolsa/bolsa_cedears.csv',delimiter=';')
    data_now=data_now.drop_duplicates(subset='Nombre', keep='first')
    data=pd.merge(data_now,data,on='Nombre').dropna()
    data['Var%']=data["Var%"]*100
    df_grouped = data.groupby(["Sector","Nombre"])[["Weigths","Var%","Nombre Completo","Precio"]].min().reset_index()
    fig = px.treemap(df_grouped, 
                    path=[px.Constant("CEDEARS"), 'Sector',  'Nombre'],
                    values='Weigths',
                    hover_name="Var%",
                    custom_data=["Nombre Completo",'Precio',"Var%"],
                    color='Var%', 
                    range_color =[-6,6],color_continuous_scale=colorscale,
                    labels={'Value': 'Number of Items'},
                    color_continuous_midpoint=0)
    fig.update_traces(marker_line_width = 1.5,marker_line_color=black,
        hovertemplate="<br>".join([
        "<b>Empresa<b>: %{customdata[0]}",
        "<b>Precio (ARS)<b>: %{customdata[1]}"
        ])
        )
    fig.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[2]}%"
    fig.update_traces(marker=dict(cornerradius=10))
    fig.update_layout(margin=dict(l=1, r=1, t=10, b=1))
    st.markdown("""<h2 style='text-align: center; color: #404040; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>S&P 500 en Cedears</h2>""", unsafe_allow_html=True)
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    data.set_index('Nombre', inplace=True)
    data=data.drop(columns=['Name','Weigths'])

@st.cache_data(show_spinner=False)
def make_acciones(data_now_merv : pd.DataFrame , data_now_gen : pd.DataFrame):
    data=pd.read_csv('data_bolsa/bolsa_arg.csv',delimiter=';')
    data_merv=pd.merge(data_now_merv,data,on='Nombre').dropna()
    data_merv['Var%']=data_merv["Var%"]*100
    #data_gen=pd.merge(data_now_gen,data,on='symbol').dropna()
    #data_gen['change']=data_gen["change"]*100

    #-------------- Fig del Merval  --------------
    df_grouped = data_merv.groupby(["Sector","Nombre"])[["CAP (MM)","Var%","Nombre Completo","Precio"]].min().reset_index()
    fig_merv = px.treemap(df_grouped, 
                    path=[px.Constant("Bolsa Argentina"), 'Sector',  'Nombre'], #Quite 'Industria', en 3
                    values='CAP (MM)',
                    hover_name="Var%",
                    custom_data=["Nombre Completo",'Precio',"Var%"],
                    color='Var%', 
                    range_color =[-6,6],color_continuous_scale=colorscale,
                    labels={'Value': 'Number of Items'},
                    color_continuous_midpoint=0)
    fig_merv.update_traces(marker_line_width = 1.5,marker_line_color=black,
        hovertemplate="<br>".join([
        "<b>Empresa<b>: %{customdata[0]}",
        "<b>Precio (ARS)<b>: %{customdata[1]}"
        ])
        )
    fig_merv.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[2]}%"
    fig_merv.update_traces(marker=dict(cornerradius=10))
    fig_merv.update_layout(margin=dict(l=1, r=1, t=10, b=1))

    #-------------- Fig del General  --------------
    #df_grouped = data_gen.groupby(["Sector","symbol"])[["CAP (MM)","change","Nombre","last"]].min().reset_index()
    #fig_gen = px.treemap(df_grouped, 
    #                path=[px.Constant("Bolsa Argentina"), 'Sector',  'symbol'], #Quite 'Industria', en 3
    #                values='CAP (MM)',
    #                hover_name="change",
    #                custom_data=["Nombre",'last',"change"],
    #                color='change', 
    #                range_color =[-6,6],color_continuous_scale=colorscale,
    #                labels={'Value': 'Number of Items'},
    #                color_continuous_midpoint=0)
    #fig_gen.update_traces(marker_line_width = 1.5,marker_line_color=black,
    #    hovertemplate="<br>".join([
    #    "<b>Empresa<b>: %{customdata[0]}",
    #    "<b>Precio (ARS)<b>: %{customdata[1]}"
    #    ])
    #    )
    #fig_gen.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[2]}%"
    #fig_gen.update_traces(marker=dict(cornerradius=10))
    #fig_gen.update_layout(margin=dict(l=1, r=1, t=10, b=1))
    return fig_merv,None#,fig_gen

def get_ecovalores():
    url='https://bonos.ecovalores.com.ar/eco/listado.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup=BeautifulSoup(response.text,'html.parser')
    tables=soup.find_all('table')
    data=None
    for i in range(len(tables)):
        try:
            table=tables[i]
            headers = table.find_all('th')
            header_texts = [header.get_text(strip=True) for header in headers]
            if 'TIR' in header_texts:
                data=[[td.text for td in tr.find_all('td')] for tr in table.find_all('tr')]
                data=pd.DataFrame(data,columns=header_texts).dropna()
                data.set_index('Título',inplace=True)
                data['TIR']=[float(i.replace('.','').replace('%','').replace(',','.')) for i in data['TIR']]
                data['Duration']=[float(i.replace(',','.')) for i in data['Duration']]
                data['Var %']=[i.replace('+','') for i in data['Var %']]#[float(i.replace('.','').replace('%','').replace(',','.').replace('+','')) for i in data['Var %']]
                data['Int. Corrido']=[float(i.replace('.','').replace(',','.')) for i in data['Int. Corrido']]
                data['VT']=[float(i.replace('.','').replace(',','.')) for i in data['VT']]
                data['Precio']=[float(i.replace('.','').replace(',','.')) for i in data['Precio']]
                data['Vencimiento']=pd.to_datetime(data['Vencimiento'],format='%d/%m/%Y')
                data['Próx. Vto.']=pd.to_datetime(data['Próx. Vto.'],format='%d/%m/%Y')
                break
        except:continue
    return data

@st.cache_resource(show_spinner=False)
def curva_soberanos(data):
    sob=go.Figure()
    #Curva Ley Extrangera
    GD=data[data.index.str.startswith('GD')]
    coefficients = np.polyfit(GD['Duration'], GD['TIR'], 2)
    polynomial = np.poly1d(coefficients)
    vencimiento_linea = np.linspace(GD['Duration'].min(), GD['Duration'].max(), 100)
    tir_linea = polynomial(vencimiento_linea)
    sob.add_trace(go.Scatter(x=vencimiento_linea, y=tir_linea, marker_color='#EBD9B4',line=dict(dash="dash",width=4),name="Ley ny",showlegend=False,legendgroup="Ley ny",hoverinfo='none',visible=True))
    sob.add_trace(go.Scatter(x=GD['Duration'], y=GD['TIR'],name="Ley N.Y.",legendgroup="Ley ny",mode="markers",marker=dict(color="#EBD9B4"),text=GD.index.values,hovertemplate = '%{text}: %{y:.2f}%<extra></extra>',visible=True))
    sob.update_traces(marker=dict(size=15,line=dict(width=2,color=black)),selector=dict(mode='markers'))

    #Curva Ley Local
    AL = data[data.index.str.startswith('AL') | data.index.str.startswith('AE')]
    coefficients = np.polyfit(AL['Duration'], AL['TIR'], 2)
    polynomial = np.poly1d(coefficients)
    vencimiento_linea = np.linspace(AL['Duration'].min(), AL['Duration'].max(), 100)
    tir_linea = polynomial(vencimiento_linea)
    sob.add_trace(go.Scatter(x=vencimiento_linea, y=tir_linea, marker_color='#9E9FA5',line=dict(dash="dash",width=4),name="Ley arg",showlegend=False,legendgroup="Ley arg",hoverinfo='none',visible=True))
    sob.add_trace(go.Scatter(x=AL['Duration'], y=AL['TIR'],name="Ley Arg.",legendgroup="Ley arg",mode="markers",marker=dict(color="#9E9FA5"),text=AL.index.values,hovertemplate = '%{text}: %{y:.2f}%<extra></extra>',visible=True))
    sob.update_traces(marker=dict(size=15,line=dict(width=2,color=black)),selector=dict(mode='markers'))
    sob.update_layout(margin=dict(l=1, r=1, t=75, b=1),
            height=450, 
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bordercolor="Black",
                borderwidth=2
            ))
    sob.update_xaxes(showline=True, linewidth=2, linecolor=black,title="Mod. Duration")
    sob.update_yaxes(showline=True, linewidth=2, linecolor=black,title="TIR")
    
    #Curva Bopreales
    bop=go.Figure()
    BP=data[data.index.str.startswith('BP')]
    coefficients = np.polyfit(BP['Duration'], BP['TIR'], 2)
    polynomial = np.poly1d(coefficients)
    vencimiento_linea = np.linspace(BP['Duration'].min(), BP['Duration'].max(), 100)
    tir_linea = polynomial(vencimiento_linea)
    bop.add_trace(go.Scatter(x=vencimiento_linea, y=tir_linea, marker_color='purple',line=dict(dash="dash",width=4),name="Bopreales",showlegend=False,legendgroup="Bopreales",hoverinfo='none'))
    bop.add_trace(go.Scatter(x=BP['Duration'], y=BP['TIR'],name="BOPREALES",legendgroup="Bopreales",mode="markers",marker=dict(color="purple"),text=BP.index.values,hovertemplate = '%{text}: %{y:.2f}%<extra></extra>'))
    bop.update_traces(marker=dict(size=15,line=dict(width=2,color=black)),selector=dict(mode='markers'))

    bop.update_layout(margin=dict(l=1, r=1, t=75, b=1),
            height=450, 
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bordercolor="Black",
                borderwidth=2
            ))
    bop.update_xaxes(showline=True, linewidth=2, linecolor=black,title="Mod. Duration")
    bop.update_yaxes(showline=True, linewidth=2, linecolor=black,title="TIR")
    return sob,bop

@st.cache_resource(show_spinner=False)
def curva_DL(data):
    fig=go.Figure()
    #Curva Bopreales
    coefficients = np.polyfit(data['Duration'], data['TIR'], 2)
    polynomial = np.poly1d(coefficients)
    vencimiento_linea = np.linspace(data['Duration'].min(), data['Duration'].max(), 100)
    tir_linea = polynomial(vencimiento_linea)
    fig.add_trace(go.Scatter(x=vencimiento_linea, y=tir_linea, marker_color='royalblue',line=dict(dash="dash",width=4),name="Dollar Linked",showlegend=False,legendgroup="Dollar Linked",hoverinfo='none'))
    fig.add_trace(go.Scatter(x=data['Duration'], y=data['TIR'],name="Dollar Linked",legendgroup="Dollar Linked",mode="markers",marker=dict(color="royalblue"),text=data.index.values,hovertemplate = '%{text}: %{y:.2f}%<extra></extra>'))
    fig.update_traces(marker=dict(size=15,line=dict(width=2,color=black)),selector=dict(mode='markers'))

    fig.update_layout(margin=dict(l=1, r=1, t=75, b=1),
            height=450, 
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bordercolor="Black",
                borderwidth=2
            ))
    fig.update_xaxes(showline=True, linewidth=2, linecolor=black,title="Mod. Duration")
    fig.update_yaxes(showline=True, linewidth=2, linecolor=black,title="TIR")
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def curva_CER(data):
    fig=go.Figure()
    #Curva Bopreales
    coefficients = np.polyfit(data['Duration'], data['TIR'], 2)
    polynomial = np.poly1d(coefficients)
    vencimiento_linea = np.linspace(data['Duration'].min(), data['Duration'].max(), 100)
    tir_linea = polynomial(vencimiento_linea)
    fig.add_trace(go.Scatter(x=vencimiento_linea, y=tir_linea, marker_color='darkgreen',line=dict(dash="dash",width=4),name="Ajustados por CER",showlegend=False,legendgroup="Ajustados por CER",hoverinfo='none'))
    fig.add_trace(go.Scatter(x=data['Duration'], y=data['TIR'],name="Ajustados por CER",legendgroup="Ajustados por CER",mode="markers",marker=dict(color="darkgreen"),text=data.index.values,hovertemplate = '%{text}: %{y:.2f}%<extra></extra>'))
    fig.update_traces(marker=dict(size=15,line=dict(width=2,color=black)),selector=dict(mode='markers'))

    fig.update_layout(margin=dict(l=1, r=1, t=75, b=1),
            height=450, 
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bordercolor="Black",
                borderwidth=2
            ))
    fig.update_xaxes(showline=True, linewidth=2, linecolor=black,title="Mod. Duration")
    fig.update_yaxes(showline=True, linewidth=2, linecolor=black,title="TIR")
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def curva_LECAPS(data):
    fig=go.Figure()
    #Curva Bopreales
    coefficients = np.polyfit(data['Duration'], data['TIR'], 2)
    polynomial = np.poly1d(coefficients)
    vencimiento_linea = np.linspace(data['Duration'].min(), data['Duration'].max(), 100)
    tir_linea = polynomial(vencimiento_linea)
    fig.add_trace(go.Scatter(x=vencimiento_linea, y=tir_linea, marker_color='#A04747',line=dict(dash="dash",width=4),name="LECAPS",showlegend=False,legendgroup="LECAPS",hoverinfo='none'))
    fig.add_trace(go.Scatter(x=data['Duration'], y=data['TIR'],name="LECAPS",legendgroup="LECAPS",mode="markers",marker=dict(color="#A04747"),text=data.index.values,hovertemplate = '%{text}: %{y:.2f}%<extra></extra>'))
    fig.update_traces(marker=dict(size=15,line=dict(width=2,color=black)),selector=dict(mode='markers'))

    fig.update_layout(margin=dict(l=1, r=1, t=75, b=1),
            height=450, 
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bordercolor="Black",
                borderwidth=2
            ))
    fig.update_xaxes(showline=True, linewidth=2, linecolor=black,title="Mod. Duration")
    fig.update_yaxes(showline=True, linewidth=2, linecolor=black,title="TIR")
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
   

def make_bonds():
    c1_1,c2_1,c3_1=st.columns(3)
    #Los dataframes deberían tener de index el ticker del bono para hacer el filtrado más simple
    with c1_1:
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Títulos Públicos')
            t_1_nac,sob,bop=st.tabs(['Panel','Curva-Soberanos','Curva-Bopreales'])
            plot_sob,plot_bop=curva_soberanos(S.bonos[S.bonos['Tipo'].isin(['Tasa Fija', 'BOPREAL'])].drop(columns=['Tipo']))
            with t_1_nac: st.table(S.bonos[S.bonos['Tipo'].isin(['Tasa Fija', 'BOPREAL'])].drop(columns=['Tipo']))
            with sob:
                st.plotly_chart(plot_sob,config={'displayModeBar': False},use_container_width=True)
            with bop:
                st.plotly_chart(plot_bop,config={'displayModeBar': False},use_container_width=True)
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    with c2_1:
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Bonos Dollar Linked')
            t_1_ex,t_2_ex=st.tabs(['Panel','Curva'])
            with t_1_ex: st.dataframe(S.bonos[S.bonos['Tipo'].isin(['Dollar Linked'])].drop(columns=['Tipo']))
            with t_2_ex: curva_DL(S.bonos[S.bonos['Tipo'].isin(['Dollar Linked'])])
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    with c3_1:
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Bonos ajustados por CER')
            t_1_c,t_2_c=st.tabs(['Panel','Curva'])
            with t_1_c: st.dataframe(S.bonos[S.bonos['Tipo'].isin(['Ajustable por CER'])].drop(columns=['Tipo']))
            with t_2_c: curva_CER(S.bonos[S.bonos['Tipo'].isin(['Ajustable por CER'])])
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    c1_2,c2_2=st.columns(2)
    with c1_2:
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Lecaps')
            t_1_l,t_2_l=st.tabs(['Panel','Curva'])
            with t_1_l: st.dataframe(S.bonos[S.bonos['Tipo'].isin(['Lecap'])].drop(columns=['Tipo']))
            with t_2_l: curva_LECAPS(S.bonos[S.bonos['Tipo'].isin(['Lecap'])])
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    with c2_2:    
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Obligaciones Negociables')
            t_1_cor,t_2_cor=st.tabs(['Panel','Curva'])
            with t_1_cor: st.dataframe(S.bonos)
            with t_2_cor: st.subheader('Curva')
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    if isinstance(S.bonos,pd.DataFrame):
        c1,c2=st.columns(2,vertical_alignment='bottom')
        c1.subheader('Buscador de Bonos')
        c2.selectbox('Bono a buscar:',options=S.bonos.index.values,key='bono_seleccionado')
        st.write(S.bono_seleccionado)
    st.divider()
    #TEST
    try:
        _=pd.merge(S.df_bonos_gob[['last','change','volume','expiration']],S.df_iamc[['Duración Modificada','Tir Anual']], left_index=True,right_index=True)
        st.dataframe(_)
    except:pass

def make_forex():
    @st.cache_resource(show_spinner=False)
    def iframes():
        tradingview_widget = """
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container" style="width: 100%; height: 100%;">
        <div class="tradingview-widget-container__widget"></div>
        <div class="tradingview-widget-copyright">
        </div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>
        {
        "width": "100%",
        "height": 500,
        "currencies": [
            "EUR",
            "USD",
            "JPY",
            "GBP",
            "HKD",
            "MXN",
            "ARS",
            "CLP",
            "COP",
            "PEN",
            "UYU",
            "BRL"
        ],
        "isTransparent": true,
        "colorTheme": "light",
        "locale": "es",
        "backgroundColor": "#ffffff"
        }
        </script>
        </div>
        <!-- TradingView Widget END -->
        """
        components.html(tradingview_widget, height=550, scrolling=True)
        w_panel_forex_val="""<!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-cross-rates.js" async>
        {
        "width": "100%",
        "height": 500,
        "currencies": [
            "EUR",
            "USD",
            "JPY",
            "GBP",
            "HKD",
            "MXN",
            "ARS",
            "CLP",
            "COP",
            "PEN",
            "UYU",
            "BRL"
        ],
        "isTransparent": true,
        "colorTheme": "light",
        "locale": "es",
        "backgroundColor": "white"
        }
        </script>
        </div>
        <!-- TradingView Widget END -->"""
        components.html(w_panel_forex_val, height=550, scrolling=True)
    iframes()
def make_merv_web():
    try:
        try:
            st.button('Recargar Datos',key='Recarga_datos',type='primary',use_container_width=True)
            if (not 'bonos' in S) or S.Recarga_datos:
                S.bonos=get_ecovalores()
                #S.docta=DoctaCap()
        except Exception as e:
            pass#st.write(e)
        bonos, acciones, cedears, forex= st.tabs(["Bonos", "Acciones",'Cedears','Forex'])
        with forex:
            make_forex()
        with bonos:
            make_bonds()
        with acciones:
            if (S.df_merval is not None):# and (S.df_general is not None):
                fig_merv,fig_gen=make_acciones(S.df_merval,S.df_general)
                container=st.container(border=True)
                if container.radio('¿Que panel desea ver?' , options=['Merval','Panel General'] , horizontal=True, index=0 , key='which_merv') == 'Merval':
                    st.markdown("""<h2 style='text-align: center; color: #404040; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Merval</h2>""", unsafe_allow_html=True)
                    st.plotly_chart(fig_merv,config={'displayModeBar': False},use_container_width=True)
                else:
                    st.markdown("""<h2 style='text-align: center; color: #404040; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Panel General</h2>""", unsafe_allow_html=True)
                    #st.plotly_chart(fig_gen, use_container_width=True)
            else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        with cedears:
            if S.df_cedears is not None:
                make_cedears(S.df_cedears)
                cede=S.df_cedears.copy().set_index('Nombre')
                c1,c2= st.columns((0.6,0.4))
                with c1:
                    st.subheader('Listado de CEDEARS')
                    st.dataframe(cede,use_container_width=True)
                with c2:
                    st.subheader('Buscador de Cedears')
                    st.selectbox('Buscador de cedears',label_visibility='collapsed',options=cede.index.to_list(),key='cedebuscado')
                    st.dataframe(cede.iloc[cede.index==S.cedebuscado].transpose(),use_container_width=True)

            else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    except:
        st.exception(Exception('🤯 Ups... Algo está andando mal. Disculpe las molestias, estamos trabajando para solucionarlo.'))
 