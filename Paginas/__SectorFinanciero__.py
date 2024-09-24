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
import re


@st.cache_data(show_spinner=False)
def plot_acciones(data_now_merv : pd.DataFrame):
    data=pd.read_csv('data_bolsa/bolsa_arg.csv',delimiter=';')
    data=data[data['Lider']=='Si']
    data_merv=pd.merge(data_now_merv,data,on='Nombre').dropna()
    data_merv['Var%']=[float(i.replace(',','.')[:-1]) for i in data_merv["Var%"]]
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
    fig_merv.update_layout(margin=dict(l=1, r=1, t=25, b=25))
    st.plotly_chart(fig_merv,config={'modeBarButtonsToRemove': ['zoom', 'pan','box select', 'lasso select','zoom in','zoom out']},use_container_width=True)

@st.cache_data(show_spinner=False)
def plot_galpones(data_now_gen : pd.DataFrame):
    data=pd.read_csv('data_bolsa/bolsa_arg.csv',delimiter=';')
    data=data[data['Lider']=='No']
    data_merv=pd.merge(data_now_gen,data,on='Nombre').dropna()
    data_merv['Var%']=[float(i.replace(',','.')[:-1]) for i in data_merv["Var%"]]
    #-------------- Fig del General  --------------
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
    fig_merv.update_layout(margin=dict(l=1, r=1, t=25, b=25))
    st.plotly_chart(fig_merv,config={'modeBarButtonsToRemove': ['zoom', 'pan','box select', 'lasso select','zoom in','zoom out']},use_container_width=True)
    
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
                data=data.rename(columns={'VT':'Valor Técnico'})
                break
        except:continue
    return data[['Nombre','Precio','Var %','Valor Técnico','Int. Corrido','TIR','Duration','Paridad','Vol %','Próx. Vto.','Vencimiento','Tipo']]

def load_iol(tipo_,url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    divs = soup.find_all("tr", {"data-cantidad": "1"})
    ticker=[div.find('a').find("b").text.strip() for div in divs]
    val=[float(div.find_all('td')[1].text.strip().replace('.','').replace(',','.')) for div in divs]
    var=[float(div.find('span',{"data-field": "Variacion"}).text.replace('.','').replace(',','.')) for div in divs]
    tipo=[tipo_ for div in divs]
    return pd.DataFrame({'Ticker':ticker,'Precio':val,'Var':var,'Tipo':tipo})
@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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

def get_galpones():
    url='https://iol.invertironline.com/mercado/cotizaciones/argentina/acciones/panel-general'
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    table=soup.find('table')
    cols=[td.text for td in table.find('thead').find_all('td')]
    data=[]
    for tr in table.find('tbody').find_all('tr'):
        row=[]
        first_column = tr.find_all('td')[0].find('b').get_text(strip=True)
        row.append(first_column)
        for td in tr.find_all('td')[1:]:
            row.append(re.sub(r'\s+', ' ', td.get_text(strip=True)))
        data.append(row)
    return pd.DataFrame(data,columns=cols)[cols[:3]].rename(columns={cols[0]:'Nombre',cols[1]:'Precio',cols[2]:'Var%'})

def get_lideres():
    url='https://iol.invertironline.com/mercado/cotizaciones/argentina/acciones/panel-l%C3%ADderes'
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    table=soup.find('table')
    cols=[td.text for td in table.find('thead').find_all('td')]
    data=[]
    for tr in table.find('tbody').find_all('tr'):
        row=[]
        first_column = tr.find_all('td')[0].find('b').get_text(strip=True)
        row.append(first_column)
        for td in tr.find_all('td')[1:]:
            row.append(re.sub(r'\s+', ' ', td.get_text(strip=True)))
        data.append(row)
    return pd.DataFrame(data,columns=cols)[cols[:3]].rename(columns={cols[0]:'Nombre',cols[1]:'Precio',cols[2]:'Var%'})

def make_acciones():
    st.button('Recargar Datos',key='Recarga_datos_acciones',type='primary',use_container_width=True)
    if (not 'lideres' in S) or S.Recarga_datos_acciones:
        S.lideres=get_lideres()
        S.galpones=get_galpones()
    c1,c2=st.columns(2)
    with c1:
        st.subheader('Panel Líderes-ARS')
        try:
            plot_acciones(S.lideres)
        except Exception as e: st.exception(e)
    with c2:
        st.subheader('Panel Galpones-ARS')
        try:
            plot_galpones(S.galpones)
        except Exception as e: st.exception(e)
    st.header('Acciones en USD')
    #@st.cache_resource(show_spinner=False)
    def iframe_acciones():
        tradingview_widget = '''
            <!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
            {
            "symbols": [["NYSE:YPF|3M|USD"],["NYSE:PAM|3M|USD"],["NYSE:BBAR|3M|USD"],["NYSE:TEO|3M|USD"],["NYSE:TGS|3M|USD"],["NASDAQ:GGAL|3M|USD"],["NYSE:BMA|3M|USD"],["NYSE:SUPV|3M|USD"],["NYSE:CEPU|3M|USD"],["NYSE:EDN|3M|USD"],["NASDAQ:CRESY|3M|USD"],["NYSE:VIST|3M|USD"],["NASDAQ:MELI|3M|USD"],["NYSE:GLOB|3M|USD"],["NYSE:DESP|3M|USD"],["NYSE:LOMA|3M|USD"],["NYSE:TS|3M|USD"],["NYSE:TX|3M|USD"]],
            "chartOnly": false,
            "width": "100%",
            "height": "600",
            "locale": "es",
            "colorTheme": "light",
            "autosize": false,
            "showVolume": false,
            "showMA": false,
            "hideDateRanges": false,
            "hideMarketStatus": false,
            "hideSymbolLogo": false,
            "scalePosition": "right",
            "scaleMode": "Normal",
            "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
            "fontSize": "14",
            "noTimeScale": false,
            "valuesTracking": "1",
            "changeMode": "price-and-percent",
            "chartType": "area",
            "headerFontSize": "medium",
            "gridLineColor": "rgba(93, 96, 107, 1)",
            "backgroundColor": "rgba(187, 217, 251, 0)",
            "widgetFontColor": "rgba(0, 0, 0, 1)",
            "lineWidth": 2,
            "lineType": 2,
            "dateRanges": [
                "1d|1",
                "1m|30",
                "3m|60",
                "12m|1D",
                "60m|1W",
                "all|1M"
            ],
            "upColor": "#22ab94",
            "downColor": "#f7525f",
            "borderUpColor": "#22ab94",
            "borderDownColor": "#f7525f",
            "wickUpColor": "#22ab94",
            "wickDownColor": "#f7525f"
            }
            </script>
            </div>
            <!-- TradingView Widget END -->
        '''
        components.html(tradingview_widget,height=600, scrolling=False)
        tradingview_widget = '''
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>
        {
        "width": "100%",
        "height": "800",
        "symbolsGroups": [
            {
            "name": "Indices",
            "originalName": "Indices",
            "symbols": [
                {
                "name": "NYSE:YPF",
                "displayName": "YPF"
                },
                {
                "name": "NYSE:PAM",
                "displayName": "PAM"
                },
                {
                "name": "NYSE:BBAR",
                "displayName": "BBAR"
                },
                {
                "name": "NYSE:TEO",
                "displayName": "TEO"
                },
                {
                "name": "NYSE:TGS",
                "displayName": "TGS"
                },
                {
                "name": "NASDAQ:GGAL",
                "displayName": "GGAL"
                },
                {
                "name": "NYSE:BMA",
                "displayName": "BMA"
                },
                {
                "name": "NYSE:SUPV",
                "displayName": "SUPV"
                },
                {
                "name": "NYSE:CEPU",
                "displayName": "CEPU"
                },
                {
                "name": "NYSE:EDN",
                "displayName": "EDN"
                },
                {
                "name": "NASDAQ:CRESY",
                "displayName": "CRESY"
                },
                {
                "name": "NYSE:VIST",
                "displayName": "VIST"
                },
                {
                "name": "NASDAQ:MELI",
                "displayName": "MELI"
                },
                {
                "name": "NYSE:GLOB",
                "displayName": "GLOB"
                },
                {
                "name": "NYSE:DESP",
                "displayName": "DESP"
                },
                {
                "name": "NYSE:LOMA",
                "displayName": "LOMA"
                },
                {
                "name": "NYSE:TS",
                "displayName": "TS"
                },
                {
                "name": "NYSE:TX",
                "displayName": "TX"
                }
            ]
            }
        ],
        "showSymbolLogo": true,
        "isTransparent": true,
        "colorTheme": "light",
        "locale": "es"
        }
        </script>
        </div>
        <!-- TradingView Widget END -->
        '''
        components.html(tradingview_widget,height=800, scrolling=False)
    iframe_acciones()

def make_panel_bonos(iol):
    data=pd.read_csv("Datos Bonos.csv",encoding='utf-8').set_index('Ticker')
    for i in data.index:
        if i in iol.index.values:
            data.at[i,'Precio']=iol.at[i,'Precio']
            data.at[i,'Var']=iol.at[i,'Var']
    df_grouped = data[data['Monto Residual']>0].reset_index().groupby(["Tipo","Tipo-2","Ticker"])[["Monto Residual","Var","Nombre","Precio",'Moneda']].min().reset_index()
    if not df_grouped.empty:
        fig_usd = px.treemap(df_grouped[df_grouped['Moneda']=='U$S'], 
                    path=[px.Constant("Bonos Argentinos"), 'Tipo',  'Tipo-2','Ticker'],
                    values='Monto Residual',
                    hover_name="Var",
                    custom_data=["Nombre", 'Precio', "Var"],
                    color='Var',
                    range_color =[-6,6],color_continuous_scale=colorscale,
                    labels={'Value': 'Number of Items'},
                    color_continuous_midpoint=0)
        fig_usd.update_traces(marker_line_width=1.5, marker_line_color='black',
                hovertemplate="<br>".join([
                    "<b>Nombre</b>: %{customdata[0]}",
                    "<b>Precio (ARS)</b>: $%{customdata[1]}"
                ])
            )
            
        fig_usd.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[2]}%"
        fig_usd.update_traces(marker=dict(cornerradius=10))
        fig_usd.update_layout(margin=dict(l=1, r=1, t=25, b=25))
        
        fig_ars = px.treemap(df_grouped[df_grouped['Moneda']=='$'], 
                    path=[px.Constant("Bonos Argentinos"), 'Tipo',  'Tipo-2','Ticker'],
                    values='Monto Residual',
                    hover_name="Var",
                    custom_data=["Nombre", 'Precio', "Var"],
                    color='Var',
                    range_color =[-6,6],color_continuous_scale=colorscale,
                    labels={'Value': 'Number of Items'},
                    color_continuous_midpoint=0)
        fig_ars.update_traces(marker_line_width=1.5, marker_line_color='black',
                hovertemplate="<br>".join([
                    "<b>Nombre</b>: %{customdata[0]}",
                    "<b>Precio (ARS)</b>: $%{customdata[1]}"
                ])
            )
            
        fig_ars.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[2]}%"
        fig_ars.update_traces(marker=dict(cornerradius=10))
        fig_ars.update_layout(margin=dict(l=1, r=1, t=25, b=25))
        return fig_usd,fig_ars

def plot_datos(data):
    data=data[['Nombre','Precio','Var %','Valor Técnico','Int. Corrido', 'TIR','Duration','Paridad']].reset_index()
    var=data['Var %']
    data['Var %']=[str(i)+'%' for i in data['Var %']]
    data['Precio']=['$'+str(i) for i in data['Precio']]
    fig = go.Figure(data=go.Table(
        columnwidth = [7,25,10,7,10,10,10,10,10],
        header=dict(values=data.columns,
                    fill = dict(color='#accbeb'),
                    line_color='#8baed5',
                    font=dict(color='white', size=14),
                    ),
        cells=dict(values=[data[col] for col in data.columns],
                fill = dict(color=['#f0f7ff', 
                                    ["white" if i % 2 == 0 else "lightgrey" for i in range(len(data))],
                                    ['#ff2d5d' if c>0 else '#04b29b' for c in var],
                                    ['#ff2d5d' if c>0 else '#04b29b' for c in var],
                                    ["white" if i % 2 == 0 else "lightgrey" for i in range(len(data))]]),
                line_color=['#8baed5','darkslategray'],
                align = ['left','center'])))
    return fig

def make_bonds():
    st.button('Recargar Datos',key='Recarga_datos_bonos',type='primary',use_container_width=True)
    if (not 'bonos' in S) or S.Recarga_datos_bonos:
        S.bonos=get_ecovalores()
        datasets={
                'Bonos':'https://iol.invertironline.com/mercado/cotizaciones/argentina/bonos/todos',
                'Letras':'https://iol.invertironline.com/mercado/cotizaciones/argentina/letras/todas',
                #'Obligaciones Negociables':'https://iol.invertironline.com/mercado/cotizaciones/argentina/obligaciones-negociables/todos'
                }
        iol=pd.DataFrame(columns=['Ticker','Precio','Var','Tipo'])
        for k in datasets:
            iol=pd.concat([iol,load_iol(k,datasets[k])],ignore_index=True)
        iol.set_index('Ticker',inplace=True)
        for i in S.bonos.index:
            if i in iol.index.values:
                S.bonos.at[i,'Precio']=iol.at[i,'Precio']
                S.bonos.at[i,'Var']=iol.at[i,'Var']

        S.iol_bonos=iol

    c1_1,c2_1=st.columns(2)
    #Los dataframes deberían tener de index el ticker del bono para hacer el filtrado más simple
    fig_usd,fig_ars=make_panel_bonos(S.iol_bonos.copy())
    with c1_1:
        st.subheader('Bonos en USD')
        st.plotly_chart(fig_usd,config={'modeBarButtonsToRemove': ['zoom', 'pan','box select', 'lasso select','zoom in','zoom out']},use_container_width=True)
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Títulos Públicos')
            t_1_nac,sob,bop=st.tabs(['Panel','Curva-Soberanos','Curva-Bopreales'])
            plot_sob,plot_bop=curva_soberanos(S.bonos[S.bonos['Tipo'].isin(['Tasa Fija', 'BOPREAL'])].drop(columns=['Tipo']))
            with t_1_nac:
                st.plotly_chart(plot_datos(S.bonos[S.bonos['Tipo'].isin(['Tasa Fija', 'BOPREAL'])]),use_container_width=True)
            with sob:
                st.plotly_chart(plot_sob,config={'displayModeBar': False},use_container_width=True)
            with bop:
                st.plotly_chart(plot_bop,config={'displayModeBar': False},use_container_width=True)
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    with c2_1:
        st.subheader('Bonos en ARS')
        st.plotly_chart(fig_ars,config={'modeBarButtonsToRemove': ['zoom', 'pan','box select', 'lasso select','zoom in','zoom out']},use_container_width=True)
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Bonos Dollar Linked')
            t_1_ex,t_2_ex=st.tabs(['Panel','Curva'])
            with t_1_ex: st.dataframe(S.bonos[S.bonos['Tipo'].isin(['Dollar Linked'])].drop(columns=['Tipo']))
            with t_2_ex: curva_DL(S.bonos[S.bonos['Tipo'].isin(['Dollar Linked'])])
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    c1_2,c2_2=st.columns(2)
    with c1_2:
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Bonos ajustados por CER')
            t_1_c,t_2_c=st.tabs(['Panel','Curva'])
            with t_1_c: st.dataframe(S.bonos[S.bonos['Tipo'].isin(['Ajustable por CER'])].drop(columns=['Tipo']))
            with t_2_c: curva_CER(S.bonos[S.bonos['Tipo'].isin(['Ajustable por CER'])])
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    with c2_2:
        if isinstance(S.bonos,pd.DataFrame):
            st.subheader('Lecaps')
            t_1_l,t_2_l=st.tabs(['Panel','Curva'])
            with t_1_l: st.dataframe(S.bonos[S.bonos['Tipo'].isin(['Lecap'])].drop(columns=['Tipo']))
            with t_2_l: curva_LECAPS(S.bonos[S.bonos['Tipo'].isin(['Lecap'])])
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    #with c2_2:    
    #    if isinstance(S.bonos,pd.DataFrame):
    #        st.subheader('Obligaciones Negociables')
    #        t_1_cor,t_2_cor=st.tabs(['Panel','Curva'])
    #        with t_1_cor: st.dataframe(S.bonos)
    #        with t_2_cor: st.subheader('Curva')
    #    else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    #if isinstance(S.bonos,pd.DataFrame):
    #    c1,c2=st.columns(2,vertical_alignment='bottom')
    #    c1.subheader('Buscador de Bonos')
    #    c2.selectbox('Bono a buscar:',options=S.bonos.index.values,key='bono_seleccionado')
    #    st.write(S.bono_seleccionado)

def make_forex():
    #@st.cache_resource(show_spinner=False)
    def iframes():
        tradingview_widget = '''
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
            "GBP",
            "JPY",
            "HKD",
            "MXN",
            "USD",
            "ARS",
            "BRL",
            "CLP",
            "COP",
            "PEN",
            "UYU"
        ],
        "isTransparent": true,
        "colorTheme": "light",
        "locale": "es",
        "backgroundColor": "#ffffff"
        }
        </script>
        </div>
        <!-- TradingView Widget END -->
        '''
        components.html(tradingview_widget, height=550, scrolling=True)
        w_panel_forex_val='''<!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-cross-rates.js" async>
        {
        "width": "100%",
        "height": 500,
        "currencies": [
            "EUR",
            "GBP",
            "JPY",
            "HKD",
            "MXN",
            "USD",
            "ARS",
            "BRL",
            "CLP",
            "COP",
            "PEN",
            "UYU"
        ],
        "isTransparent": true,
        "colorTheme": "light",
        "locale": "es",
        "backgroundColor": "white"
        }
        </script>
        </div>
        <!-- TradingView Widget END -->'''
        components.html(w_panel_forex_val, height=550, scrolling=True)
    iframes()


def make_metrics():
    @st.cache_data(show_spinner=False)
    def get_dolar():
        url='https://dolarhoy.com/'
        response=requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')
        data=[]
        for i in soup.find('div', class_='tile is-parent is-9 cotizacion is-vertical').find_all('div',class_='tile is-child'):
            try:
                ind=i.find('a',class_='title').text
                precio=i.find('div',class_='venta').find('div',class_='val').text.replace('$','').replace('','').replace(',','.')
                var=i.find('div',class_='venta').find('div',class_='var-porcentaje').text.replace('%','').replace('','').replace(',','.')
                data.append([ind,precio,var])
            except: continue
        return data[:4]
    data=get_dolar()
    
    if isinstance(data,list):
        cols=st.columns(len(data),vertical_alignment='bottom')
        for i in range(len(data)):
            cols[i].metric(data[i][0],f'${data[i][1]}',f'{data[i][2]}%')

def make_cedears():
    #@st.cache_resource(show_spinner=False)
    def plot_spy():
        widget='''
                <!-- TradingView Widget BEGIN -->
                <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
                {
                "exchanges": [],
                "dataSource": "SPX500",
                "grouping": "sector",
                "blockSize": "market_cap_basic",
                "blockColor": "change",
                "locale": "es",
                "symbolUrl": "",
                "colorTheme": "light",
                "hasTopBar": false,
                "isDataSetEnabled": false,
                "isZoomEnabled": false,
                "hasSymbolTooltip": false,
                "isMonoSize": false,
                "width": "100%",
                "height": "490"
                }
                </script>
                </div>
                <!-- TradingView Widget END -->
        '''
        components.html(widget, height=500, scrolling=False)
    plot_spy()

    #@st.cache_data(show_spinner=False)
    def analisis_spy(ticker):
        widget='''
                <!-- TradingView Widget BEGIN -->
                <div class="tradingview-widget-container">
                <div class="tradingview-widget-container__widget"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
                {
                "symbol": "'''+ticker+'''",
                "width": "100%",
                "locale": "es",
                "colorTheme": "light",
                "isTransparent": true
                }
                </script>
                </div>
                <!-- TradingView Widget END -->
                '''
        components.html(widget, height=200, scrolling=False)
        widget='''
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container">
                    <div class="tradingview-widget-container__widget"></div>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
                    {
                    "width": "100%",
                    "height": "390",
                    "symbol": "'''+ticker+'''",
                    "interval": "D",
                    "timezone": "America/Argentina/Buenos_Aires",
                    "theme": "light",
                    "style": "3",
                    "locale": "es",
                    "backgroundColor": "rgba(255, 255, 255, 1)",
                    "gridColor": "rgba(42, 46, 57, 0)",
                    "hide_legend": true,
                    "withdateranges": true,
                    "allow_symbol_change": false,
                    "calendar": false,
                    "hide_volume": true,
                    "support_host": "https://www.tradingview.com"
                    }
                    </script>
                    </div>
                    <!-- TradingView Widget END -->
                '''
        components.html(widget, height=400, scrolling=False)
        c1,c2=st.columns((0.4,0.6))
        with c1:
            widget='''
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container">
                    <div class="tradingview-widget-container__widget"></div>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {
                    "interval": "1m",
                    "width": "100%",
                    "isTransparent": true,
                    "height": "900",
                    "symbol": "'''+ticker+'''",
                    "showIntervalTabs": true,
                    "displayMode": "multiple",
                    "locale": "es",
                    "colorTheme": "light"
                    }
                    </script>
                    </div>
                    <!-- TradingView Widget END -->
                    '''
            components.html(widget, height=900, scrolling=False)
        with c2:
            widget='''
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container">
                    <div class="tradingview-widget-container__widget"></div>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-financials.js" async>
                    {
                    "isTransparent": true,
                    "largeChartUrl": "",
                    "displayMode": "adaptive",
                    "width": "100%",
                    "height": "450",
                    "colorTheme": "light",
                    "symbol": "'''+ticker+'''",
                    "locale": "es"
                    }
                    </script>
                    </div>
                    <!-- TradingView Widget END -->
                    '''
            components.html(widget, height=450, scrolling=False)
            widget='''
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container">
                    <div class="tradingview-widget-container__widget"></div>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
                    {
                    "width": "100%",
                    "height": "450",
                    "isTransparent": true,
                    "colorTheme": "light",
                    "symbol": "'''+ticker+'''",
                    "locale": "es"
                    }
                    </script>
                    </div>
                    <!-- TradingView Widget END -->
                    '''
            components.html(widget, height=450, scrolling=False)
            
    st.text_input('Buscador de equity -- Pruebe "NYSE:VIST" o "NASDAQ:GOOG"', value="NASDAQ:AAPL", key='cedear',help='Debe poner primero el exchange (ej. NYSE o NASDAQ), luego de dos puntos (":") y finalmente el activo a buscar.', placeholder='Ticker')
    if isinstance(S.cedear,str):
        analisis_spy(S.cedear.capitalize())

def make_merv_web():
    try:
        make_metrics()
        bonos, acciones, cedears, forex= st.tabs(["Bonos", "Acciones Argentinas",'Acciones Extranjeras','Forex'])
        with bonos:
            try:
                make_bonds()
            except: st.exception(Exception('🤯 Ups... Algo está andando mal. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        with acciones:
            try:
                make_acciones()
            except: st.exception(Exception('🤯 Ups... Algo está andando mal. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        with cedears:
            try:
                make_cedears()
            except: st.exception(Exception('🤯 Ups... Algo está andando mal. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        with forex:
            make_forex()
    except Exception as e:
        st.exception(e)#Exception('🤯 Ups... Algo está andando mal. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    st.divider()
    st.caption('Ninguna de la información provista debe ser utilizada como recomendación financiera de ningún tipo. Invertir es riesgoso, actúe bajo su propia discreción.')
 