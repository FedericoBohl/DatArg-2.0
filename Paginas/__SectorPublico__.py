from _globals_ import *
import streamlit as st
from streamlit import session_state as S
import pandas as pd
from Paginas.librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import plotly.express as px
import io
from _globals_ import colorscale
@st.cache_resource(show_spinner=False)
def load_data_sectpub(date):
    deficit=pd.read_csv("His Data/his-deficit.csv",delimiter=";")
    deficit['Unnamed: 0'] = pd.to_datetime(deficit.iloc[:, 0].values, format='%d/%m/%Y')
    deficit.set_index('Unnamed: 0', inplace=True)
    ids=["379.9_GTOS_PRIMA017__39_96",
        "379.9_ING_DESPUE017__28_10",
        "379.9_SUPERAVIT_017__23_94",
        "379.9_RESULTADO_017__18_38"
        ]
    cols=["Gastos","Ingresos","Superavit Primario","Superavit Financiero"]
    data=get_data(ids,start_date="2024-01-01",col_list=cols)
    data['Intereses de Deuda']=data['Superavit Primario']-data['Superavit Financiero']
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
    deficit.columns=data.columns
    data.reindex(columns=deficit.columns)
    data=pd.concat([deficit,data],axis=0)
    datagdp=data.copy().iloc[48:]

    datagdp["PBI"]=S.pbi_men[:len(datagdp)]
    for col in data.columns.to_list():
        datagdp[col]=datagdp.rolling(12).sum()[col]*100/(datagdp["PBI"]*4)
    
    datatco=data.copy().iloc[48:]
    datatco['TC']=S.TC
    for col in data.columns.to_list():
        datatco[col]=datatco[col]/datatco["TC"]
    ################## ENDEUDAMIENTO ##############################
    endeudamiento_his=pd.read_csv("His Data/his-endeudamiento.csv",delimiter=";")
    endeudamiento_his['Unnamed: 0'] = pd.to_datetime(endeudamiento_his.iloc[:, 0].values, format='%Y-%m-%d')
    endeudamiento_his.set_index('Unnamed: 0', inplace=True)
    ids=["379.9_FTES_FIN_E017__47_62",
        "379.9_FTES_FIN_E017__49_20",
        "379.9_AP_FIN_AMO017__50_49",
        "379.9_AP_FIN_AMO017__52_70"
        ]
    cols=["Endeudamiento ARS","Endeudamiento USD","Amort ARS","Amort USD"]
    endeudamiento_cur=get_data(ids,start_date="2024-01-01",col_list=cols)
    endeudamiento_cur.index = pd.to_datetime(endeudamiento_cur.index, format='%Y-%m-%d')
    endeudamiento_cur.columns=endeudamiento_his.columns
    endeudamiento_cur.reindex(columns=endeudamiento_his.columns)
    endeudamiento_cur=pd.concat([endeudamiento_his,endeudamiento_cur],axis=0)
    endeudamiento_cur['ARS']=endeudamiento_cur['Endeudamiento ARS']-endeudamiento_cur['Amort ARS']
    endeudamiento_cur['USD']=endeudamiento_cur['Endeudamiento USD']-endeudamiento_cur['Amort USD']
    endeudamiento_cur['Total']=endeudamiento_cur['ARS']+endeudamiento_cur['USD']
    endeudamiento_curgdp=endeudamiento_cur.copy().iloc[48:]

    endeudamiento_curgdp["PBI"]=S.pbi_men[:len(endeudamiento_curgdp)]
    for col in endeudamiento_cur.columns.to_list():
        endeudamiento_curgdp[col]=endeudamiento_curgdp.rolling(12).sum()[col]*100/(endeudamiento_curgdp["PBI"]*4)
    
    endeudamientotco=endeudamiento_cur.copy().iloc[47:]
    endeudamientotco['TC']=S.TC
    for col in endeudamiento_cur.columns.to_list():
        endeudamientotco[col]=endeudamientotco[col]/endeudamientotco["TC"]

    ############################ GASTOS/INGRESOS ###############################################
    corr_his=pd.read_csv("His Data/his-ingresos-gastos.csv",delimiter=";")
    corr_his['Unnamed: 0'] = pd.to_datetime(corr_his.iloc[:, 0].values, format='%Y-%m-%d')
    corr_his.set_index('Unnamed: 0', inplace=True)
    ids=["379.9_GTOS_CORR_017__14_1",
        "379.9_GTOS_CORR_017__49_26",
        "379.9_GTOS_CORR_017__51_65",
        "379.9_GTOS_CORR_017__43_4",
        "379.9_GTOS_CORR_017__35_92",
        "379.9_GTOS_CORR_017_3_0_M_50_79",
        "379.9_GTOS_CORR_017_5_0_M_51_42",
        "379.9_GTOS_CORR_017_7_0_M_38_20",
        "379.9_GTOS_CORR_017_8_0_M_37_3",
        "379.9_GTOS_CORR_017__34_72",
        "379.9_ING_CORR_2017__13_2",
        "379.9_ING_CORR_I017__29_10",
        "379.9_ING_CORR_A017__37_57",
        "379.9_ING_CORR_I017__32_24",
        "379.9_ING_CORR_T017__25_70"
        ]
    cols=['Gastos Corrientes','Remuneraciones','Bienes y Servicios','Otros Gastos de Consumo',"Gasto Seguridad Social",
         "Trans Sect Priv","Trans Provincias y CABA","Trans Universidades","Trans Otras","Trans Sect Ext",
         'Ingresos Corrientes','Ingresos Tributarios','Ingresos Seguridad Social','Ingresos No Tributarios',
         'Ingresos Transferencias Corrientes']
    corr=get_data(ids,start_date="2024-01-01",col_list=cols)
    corr.index = pd.to_datetime(corr.index, format='%Y-%m-%d')
    corr['Gastos en consumo y operación']=corr['Remuneraciones']+corr['Bienes y Servicios']+corr['Otros Gastos de Consumo']
    corr['Gastos Transferencias Corrientes']=corr['Trans Sect Priv']+corr['Trans Provincias y CABA']+corr['Trans Universidades']+corr['Trans Otras']+corr['Trans Sect Ext']
    corr=corr.drop(columns=['Remuneraciones','Bienes y Servicios','Otros Gastos de Consumo',"Trans Sect Priv","Trans Provincias y CABA","Trans Universidades","Trans Otras","Trans Sect Ext"])
    corr['Otros Gastos']=corr['Gastos Corrientes']-corr['Gastos en consumo y operación']-corr['Gastos Transferencias Corrientes']-corr['Gasto Seguridad Social']
    corr['Otros Ingresos']=corr['Ingresos Corrientes']-corr['Ingresos Tributarios']-corr['Ingresos Seguridad Social']-corr['Ingresos No Tributarios']-corr['Ingresos Transferencias Corrientes']
    corr.reindex(columns=corr_his.columns)
    corr=pd.concat([corr_his,corr],axis=0)
    corrgdp=corr.copy().iloc[48:]
    corrgdp["PBI"]=S.pbi_men[:len(corrgdp)]
    for col in corr.columns.to_list():
        corrgdp[col]=corrgdp.rolling(12).sum()[col]*100/(corrgdp["PBI"]*4)
    
    corrtco=corr.copy().iloc[47:]
    corrtco['TC']=S.TC
    for col in corr.columns.to_list():
        corrtco[col]=corrtco[col]/corrtco["TC"]
    
    return data.rolling(12).sum().dropna(), datagdp.dropna(), datatco.rolling(12).sum().dropna(),endeudamiento_cur.rolling(12).sum().dropna(), endeudamiento_curgdp.dropna(), endeudamientotco.rolling(12).sum().dropna(),corr.rolling(12).sum().dropna(),corrgdp.dropna(),corrtco.rolling(12).sum().dropna()

@st.cache_resource(show_spinner=False)
def load_data_map(end):
    provincias={#'Ciudad Autónoma de Buenos Aires':'Capital Federal',
        'Provincia de Buenos Aires':'Buenos Aires',
        'Provincia de Catamarca':'Catamarca',
        'Provincia de Corrientes':'Corrientes',
        'Provincia de Córdoba':'Córdoba',
        'Provincia de Entre Ríos':'Entre Ríos',
        'Provincia de Formosa':'Formosa',
        'Provincia de Jujuy':'Jujuy',
        'Provincia de La Pampa':'La Pampa',
        'Provincia de La Rioja':'La Rioja',
        'Provincia de Mendoza':'Mendoza',
        'Provincia de Misiones':'Misiones',
        'Provincia de Río Negro':'Río Negro',
        'Provincia de Salta':'Salta',
        'Provincia de San Juan':'San Juan',
        'Provincia de San Luis':'San Luis',
        'Provincia de Santa Cruz':'Santa Cruz',
        'Provincia de Santa Fe':'Santa Fe',
        'Provincia de Santiago del Estero':'Santiago del Estero',
        'Provincia de Tierra del Fuego, Antártida e Islas del Atlántico Sur':'Tierra del Fuego, Antártida e Islas del Atlántico Sur',
        'Provincia de Tucumán':'Tucumán',
        'Provincia del Chaco':'Chaco',
        'Provincia del Chubut':'Chubut',
        'Provincia del Neuquén':'Neuquén'}

    df = pd.read_csv('donde-se-gasta.csv')
    df['Ubicacion geografica'] = df['Ubicacion geografica'].replace(provincias)
    df['Presupuestado']=df['Presupuestado'].str.replace(',','').astype(float)
    df['Ejecutado']=df['Ejecutado'].str.replace(',','').astype(float)
    df['% Ejecutado']=df['% Ejecutado'].astype(float)

    df['% Presupuestado']=df['Presupuestado']/sum(df['Presupuestado'])*100
    extras=df.iloc[-4:]
    df=df.iloc[:-4]
    geo=json.load(open('provincias.geojson', encoding='utf-8'))
    provincias_geo_df = pd.json_normalize(geo['features'])
    df=provincias_geo_df.merge(df, left_on='properties.nombre', right_on='Ubicacion geografica')
    return df, geo, extras

@st.cache_resource(show_spinner=False)
def load_datos_deuda(end) -> pd.DataFrame|None:
    # URL del archivo de Excel
    url = "https://www.argentina.gob.ar/sites/default/files/boletin_mensual_30_04_2024_0.xlsx"

    # Descargar el archivo
    response = requests.get(url)
    if response.status_code == 200:
        # Leer el archivo de Excel en un DataFrame sin guardarlo
        excel_data = io.BytesIO(response.content)
        xls = pd.ExcelFile(excel_data)
        
        # Cargar las hojas 'A.1' y 'A.5'
        sheet_A1 = pd.read_excel(xls, sheet_name='A.1')
        sheet_A5 = pd.read_excel(xls, sheet_name='A.5')

        _=sheet_A1.iloc[15:45].transpose()
        cols=['TÍTULOS PÚBLICOS',' - Moneda nacional','Deuda no ajustable por CER','Deuda ajustable por CER',' - Moneda extranjera ']
        _.columns=_.iloc[1]
        _=_.iloc[2:-1]
        date_list = pd.date_range(start='2019-01-01 00:00:00', periods=len(_), freq='M').tolist()
        tp=pd.DataFrame(index=date_list)
        for i in cols:
            tp[i]=_[i].tolist()

        _=sheet_A1.iloc[80:87].transpose()
        cols=['LETRAS DEL TESORO',' - Moneda nacional',' - Moneda extranjera ']
        _.columns=_.iloc[1]
        _=_.iloc[2:-1]
        __=sheet_A1.iloc[134:148].transpose()
        __.columns=__.iloc[1]
        __=__.iloc[2:-1]
        letras:pd.DataFrame=pd.DataFrame(index=date_list)
        for i in cols:
            letras[i]=[_[i][k]+__[i][k] for k in range(len(_))]

        df=pd.merge(tp,letras,left_index=True,right_index=True)
        df.columns=['Titulos Publicos', 'Titulos Publicos-Moneda Nacional',
            'Deuda no ajustable por CER', 'Deuda ajustable por CER',
            'Titulos Publicos-Moneda Extranjera', 'Letras', 'Letras-Moneda Nacional',
            'Letras-Moneda Extranjera']

        _=sheet_A1.iloc[85:95].transpose()
        _.columns=_.iloc[1]
        _=_.iloc[2:-1]
        df['Prestamos']=_['PRÉSTAMOS'].tolist()
        _=sheet_A1.iloc[7:9].transpose()
        _.columns=_.iloc[1]
        _=_.iloc[2:-1]
        df['Total Deuda Bruta']=_['A- DEUDA BRUTA ( I + II  + III)'].tolist()
        df['Otros']=df['Total Deuda Bruta']-df['Titulos Publicos']-df['Letras']-df['Prestamos']

        deuda_mon=sheet_A5.iloc[12:21].transpose().iloc[2:-1]
        deuda_mon.index=date_list
        deuda_mon=deuda_mon.rename(columns={12:'Total Pagado',14:'Total-Moneda Nacional',15:'Capital-Moneda Nacional',16:'Intereses-Moneda Nacional',18:'Total-Moneda Extranjera',19:'Capital-Moneda Extranjera',20:'Intereses-Moneda Extranjera'})
        deuda_mon=deuda_mon.drop(columns=[13,17],axis=0)
        del tp,letras,_,__,excel_data,xls,sheet_A1,sheet_A5
        return df,deuda_mon

@st.cache_data(show_spinner=False)
def plot_deficit(escala,data:pd.DataFrame):
    t1,t2=st.tabs(['Superavit Financiero','Superavit Fiscal'])
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data["Superavit Financiero"],name="Resultado Financiero",line=dict(width=3),marker_color=black))
    fig.add_trace(go.Bar(x=data.index,y=data["Superavit Primario"],name="Superavit Primario",marker_color=olive))
    fig.add_trace(go.Bar(x=data.index,y=-data["Intereses de Deuda"],name="Intereses de deuda",marker_color=teal))
    fig.add_hline(y=0,line_dash="dot",secondary_y=True)
    fig.add_annotation(text="Déficit 0",
                    xref="paper", yref="paper",
                    x=0.9, y=0.98, showarrow=False,
                        font=dict(size=12,color=black),
                        align="center",
                        bordercolor=black,
                        borderwidth=1,
                        borderpad=2,
                        bgcolor=white,
                        opacity=0.8
                        )
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),
        barmode="relative",height=450, 
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bordercolor="Black",
            borderwidth=2
        ),
        yaxis=dict(showgrid=False, zeroline=True, showline=True)
    )
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    t1.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index, y=data["Superavit Primario"], name="Resultado Primario", marker_color=black,line=dict(width=3)), secondary_y=True)
    fig.add_trace(go.Bar(x=data.index, y=data["Ingresos"], name="Ingresos", marker_color=green), secondary_y=False)
    fig.add_trace(go.Bar(x=data.index, y=-data["Gastos"], name="Gastos", marker_color=red), secondary_y=False)
    fig.add_hline(y=0,line_dash="dot",secondary_y=True)
    fig.add_annotation(text="Déficit 0",
            xref="paper", yref="paper",
            x=0.9, y=0.98, showarrow=False,
            font=dict(size=12,color=black),
            align="center",
            bordercolor=black,
            borderwidth=1,
            borderpad=2,
            bgcolor=white,
            opacity=0.8
            )
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Gasto/Ingresos-Millones de ARS'
        fig['layout']['yaxis2']['title']='Superávit/Déficit-Millones de ARS'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Gasto/Ingresos-Millones de USD-TC Oficial'
        fig['layout']['yaxis2']['title']='Superávit/Déficit-Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='Gasto/Ingresos-PP del PBI'
        fig['layout']['yaxis2']['title']='Superávit/Déficit-PP del PBI'
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="overlay",bargap=0.2,height=450,legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bordercolor='black',
                                    borderwidth=2),
                                    yaxis=dict(showgrid=False, zeroline=True, showline=True),
                                    yaxis2=dict(showgrid=False, zeroline=True, showline=True)
                                )
    t2.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

#@st.cache_data(show_spinner=False)
def make_map(data,geo,extras:pd.DataFrame,eleccion):
    extras=extras.to_dict()
    st.write(extras)
    fig = make_subplots(
        rows=4, cols=2,
        specs=[[{"type": "domain"}, {"rowspan": 4,"type": "choroplethmapbox"}],
            [{"type": "domain"}, None],
            [{"type": "domain"}, None],
            [{"type": "domain"}, None]],
        print_grid=True)
    mapa = px.choropleth_mapbox(
        data,
        geojson=geo,
        locations='Ubicacion geografica',
        featureidkey='properties.nombre',
        color=f'% {eleccion}',
        hover_name='properties.nombre',
        custom_data=['properties.nombre',f'{eleccion}',f'% {eleccion}'],
        color_continuous_scale='Picnic',
        mapbox_style="carto-positron",
        zoom=2.6, center={"lat": -38.40, "lon": -63.60},
        opacity=1,
        color_discrete_sequence=["blue"],
    )

    # Actualizar las trazas del mapa
    mapa.update_traces(
        marker_line_width=1.5,
        marker_line_color='black',
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",
            "Presupuesto Brindado: $%{customdata[1]:.2f}" if eleccion == 'Presupuesado' else "Presupuesto Ejecutado: $%{customdata[1]:.2f}",
            "Proporción del total: %{customdata[2]:.2f}%" if eleccion == 'Presupuesado' else "Presupuesto Ejecutado: %{customdata[2]:.2f}%"
        ])
    )

    # Añadir la figura del mapa al subplot
    fig.add_traces(mapa.data, rows=1, cols=2)
    picnic_colors = [
                    [0.0, '#ff0000'],  # Rojo
                    [0.25, '#ff99cc'], # Rosa
                    [0.5, '#ffff00'],  # Amarillo
                    [0.75, '#66ff66'], # Verde
                    [1.0, '#00ccff']   # Azul
                    ]
    # Añadir los indicadores (métricas) como gráficos individuales
    fig.add_trace(go.Indicator(
                                mode="number+gauge",  # Modo del indicador que incluye el número y el gauge
                                value=extras[eleccion][25] / 1000,  # Valor que se muestra en el número (dividido por 1000 para mostrar en 'k')
                                number={"prefix": "$", "suffix": "k"},  # Prefijo y sufijo del número
                                gauge={
                                        'axis': {'range': [0, 100]},  # Rango del gauge de 0 a 100%
                                        'bar': {'color': "rgba(0, 0, 0, 0)"},  # Hacer la barra central completamente transparente
                                        'steps': [
                                            {'range': [0, 100], 'color': 'lightblue'}  # Color celeste uniforme en todo el rango
                                        ],
                                        'threshold': {
                                            'thickness': 0.75,  # Grosor de la línea de umbral
                                            'value': extras[f'% {eleccion}'][25]  # Valor del umbral que indica la posición en el gauge
                                        }
                                     },
                                title={"text": f"{extras['Ubicacion geografica'][25]}"}  # Título con el nombre de la ubicación geográfica
                            ), row=1, col=1)
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=450,
        delta={'reference': 400},
        title={"text": "Métrica 1"},
    ), row=2, col=1)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=300,
        delta={'reference': 250},
        title={"text": "Métrica 2"},
    ), row=3, col=1)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=200,
        delta={'reference': 180},
        title={"text": "Métrica 3"},
    ), row=4, col=1)

    # Actualizar el layout de la figura
    fig.update_layout(
        mapbox=dict(
            center={"lat": -38.4161, "lon": -63.6167},
            style="white-bg",
            zoom=2.65,
            layers=[dict(below='traces', type='fill', source=geo, color="lightblue")]
        ),
        showlegend=False,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    # Añadir la figura del mapa al subplot

    # Añadir las tres métricas como gráficos individuales (ejemplo de pie charts)
    #fig.add_trace(go.Indicator(
    #mode="gauge+number",  # Modo del indicador que incluye el gauge y el número
    #value=extras[f'% {eleccion}'][23],  # Valor para el gauge (68%)
    #title={'text':23},
    #domain={'x': [0, 1], 'y': [0, 1]}  # Dominios para el tamaño y posición del gauge
    #),row=1, col=1)
    #fig.add_trace(go.Pie(labels=["Métrica 2"], values=[20], name="Métrica 2"), row=2, col=1)
    #fig.add_trace(go.Pie(labels=["Métrica 3"], values=[30], name="Métrica 3"), row=2, col=1)
    # Actualizar el layout de la figura
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_data(show_spinner=False)
def plot_deuda(data,type_plot):
    if not isinstance(data,pd.DataFrame):st.error('Error Extrayendo los Datos de la Deuda Bruta')
    else:
        if type_plot=='Composición de la Deuda Bruta':
            t1,t2,t3,t4=st.tabs(['Gráfico','Títulos Públicos','Letras','Datos'])
            t4.dataframe(data)
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data['Total Deuda Bruta'],name='Total',line=dict(width=5),marker_color=black))
            fig.add_trace(go.Bar(x=data.index,y=data['Titulos Publicos'],name='Títulos Públicos',marker_color='#1679AB'))
            fig.add_trace(go.Bar(x=data.index,y=data['Letras'],name='Letras',marker_color='#C80036'))
            fig.add_trace(go.Bar(x=data.index,y=data['Prestamos'],name='Préstamos',marker_color='#FFF5E1'))
            fig.add_trace(go.Bar(x=data.index,y=data['Otros'],name='Otros',marker_color=gray))
            fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1,
                                            bordercolor=black,
                                            borderwidth=2
                                        ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
            fig['layout']['yaxis']['title']='Millones de USD (Fecha de Pago Efectivo)'
            t1.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
            
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data['Titulos Publicos'],name='Total',line=dict(width=3.5),marker_color=black))
            fig.add_trace(go.Scatter(x=data.index,y=data['Titulos Publicos-Moneda Nacional'],name='Moneda Nacional',line=dict(width=2),marker_color='#254336',legendgroup='Moneda Nacional'))
            fig.add_trace(go.Bar(x=data.index,y=data['Deuda ajustable por CER'],name='Ajustable por CER',marker_color='#6B8A7A',legendgroup='Moneda Nacional'))
            fig.add_trace(go.Bar(x=data.index,y=data['Deuda no ajustable por CER'],name='No Ajustable por CER',marker_color='#B7B597',legendgroup='Moneda Nacional'))
            fig.add_trace(go.Bar(x=data.index,y=data['Titulos Publicos-Moneda Extranjera'],name='Moneda Extranjera',marker_color='#D1D8C5'))
            fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1,
                                            bordercolor=black,
                                            borderwidth=2
                                        ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
            fig['layout']['yaxis']['title']='Millones de USD (Fecha de Pago Efectivo)'
            t2.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data['Letras'],name='Total',line=dict(width=3.5),marker_color=black))
            fig.add_trace(go.Bar(x=data.index,y=data['Letras-Moneda Nacional'],name='Moneda Nacional',marker_color='#40A578',legendgroup='Moneda Nacional'))
            fig.add_trace(go.Bar(x=data.index,y=data['Letras-Moneda Extranjera'],name='Moneda Extranjera',marker_color='#006769'))
            fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1,
                                            bordercolor=black,
                                            borderwidth=2
                                        ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
            fig['layout']['yaxis']['title']='Millones de USD (Fecha de Pago Efectivo)'
            t3.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)


        else:
            t1,t2=st.tabs(['Gráfico','Datos'])
            t2.dataframe(data)
            data=data.rolling(12).sum().dropna()
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=data.index,y=data['Total Pagado'],name='Total',line=dict(width=5),marker_color=black))
            fig.add_trace(go.Scatter(x=data.index,y=data['Total-Moneda Nacional'],name='Moneda Nacional',line=dict(width=2,dash='dashdot'),marker_color='red',legendgroup='Moneda Nacional'))
            fig.add_trace(go.Scatter(x=data.index,y=data['Total-Moneda Extranjera'],name='Moneda Extranjera',line=dict(width=2,dash='dashdot'),marker_color='royalblue',legendgroup='Moneda Extranjera'))
            fig.add_trace(go.Bar(x=data.index,y=data['Capital-Moneda Nacional'],name='Capital-Moneda Nacional',marker_color=red,legendgroup='Moneda Nacional',showlegend=False))
            fig.add_trace(go.Bar(x=data.index,y=data['Intereses-Moneda Nacional'],name='Capital-Moneda Nacional',marker_color=orange,legendgroup='Moneda Nacional',showlegend=False))
            fig.add_trace(go.Bar(x=data.index,y=data['Capital-Moneda Extranjera'],name='Capital-Moneda Extranjera',marker_color=blue,legendgroup='Moneda Extranjera',showlegend=False))
            fig.add_trace(go.Bar(x=data.index,y=data['Intereses-Moneda Extranjera'],name='Capital-Moneda Extranjera',marker_color='cyan',legendgroup='Moneda Extranjera',showlegend=False))
            fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1,
                                            bordercolor=black,
                                            borderwidth=2
                                        ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
            fig['layout']['yaxis']['title']='Millones de USD (Fecha de Pago Efectivo)'
            t1.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_data(show_spinner=False)
def plot_endeudamiento(data,escala):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['Total'],name='Endeudamiento Total',marker_color=black,line=dict(width=4)))
    fig.add_trace(go.Bar(x=data.index,y=data['ARS'],name='Moneda Local',marker_color='#C80036'))
    fig.add_trace(go.Bar(x=data.index,y=data['USD'],name='Moneda Extranjera',marker_color='#AF47D2'))
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)


    st.caption('Los datos corresponden al endeudamiento en cada moneda neto de lo amortizado en el mes en cuestión. Se ignora el incremento de otros pasivos.')

@st.cache_data(show_spinner=False)
def plot_ingresos_gastos(data,escala):
    t1,t2=st.tabs(['Ingresos','Gastos'])
    st.caption('Los datos son el resultado anual acumulado de cada mes.')

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['Ingresos Corrientes'],name='Total',line=dict(width=5),marker_color=black))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos Tributarios'],name='Ing. Tributarios',marker_color='#059212'))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos Seguridad Social'],name='Aport. a la Seg. Social',marker_color='#9BEC00'))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos No Tributarios'],name='Ing. No Tributarios',marker_color='#006769'))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos Transferencias Corrientes'],name='Trans. Corrientes',marker_color='#F3FF90'))
    fig.add_trace(go.Bar(x=data.index,y=data['Otros Ingresos'],name='Otros',marker_color='#059212'))
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
        fig['layout']['yaxis']['type']='log'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    t1.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['Gastos Corrientes'],name='Total',line=dict(width=5),marker_color=black))
    fig.add_trace(go.Bar(x=data.index,y=data['Gastos en consumo y operación'],name='Gtos. Consumo/Operación',marker_color='#FFC100'))
    fig.add_trace(go.Bar(x=data.index,y=data['Gasto Seguridad Social'],name='Prestaciones Seg. Social',marker_color='#FF6500'))
    fig.add_trace(go.Bar(x=data.index,y=data['Gastos Transferencias Corrientes'],name='Trans. Corrientes',marker_color='#C40C0C'))
    fig.add_trace(go.Bar(x=data.index,y=data['Otros Gastos'],name='Otros',marker_color='#FFF5E1'))
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
        fig['layout']['yaxis']['type']='log'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    t2.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

def make_sect_pub_web():
    deficit=S.deficit_.copy()
    datagdp=S.deficitgdp_.copy()
    datatco=S.deficittco_.copy()
    endeudamiento=S.endeudamiento_.copy()
    endeudamientogdp=S.endeudamientogdp_.copy()
    endeudamientotco=S.endeudamientotco_.copy()
    corr=S.corr_.copy()
    corrgdp=S.corrgdp_.copy()
    corrtco=S.corrtco_.copy()
    c1,c2=st.columns((0.7,0.3),vertical_alignment='center')
    with c1:
        with st.expander(label='Ajustar Gráficas',icon=":material/settings:"):
            c11,c12=st.columns((0.3,0.7))
            with c11: st.radio("Escala de los datos",options=["***Millones de ARS***","***Millones de USD-Oficial***","***Millones de USD-Blue***","***% del PBI***"],key="escala_sectpub")
            with c12: st.number_input(value=2016,label='Datos desde',min_value=2000,max_value=2024,key="start_sectpub")
    with c2:
        st.link_button(":blue[**Descargar datos:\nSector Público**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/QfXi8hfJF_kggFaNFQAAAAAAHinUdp-mVHJoLA",use_container_width=True)
    deficit=deficit.loc[f"{S.start_sectpub}":]
    deficit.index=deficit.index.strftime('%b-%Y')
    datagdp=datagdp.loc[f"{S.start_sectpub}":]
    datagdp.index=datagdp.index.strftime('%b-%Y')
    datatco=datatco.loc[f"{S.start_sectpub}":]
    datatco.index=datatco.index.strftime('%b-%Y')
    endeudamiento=endeudamiento.loc[f"{S.start_sectpub}":]
    endeudamiento.index=endeudamiento.index.strftime('%b-%Y')
    endeudamientogdp=endeudamientogdp.loc[f"{S.start_sectpub}":]
    endeudamientogdp.index=endeudamientogdp.index.strftime('%b-%Y')
    endeudamientotco=endeudamientotco.loc[f"{S.start_sectpub}":]
    endeudamientotco.index=endeudamientotco.index.strftime('%b-%Y')
    corr=corr.loc[f"{S.start_sectpub}":]
    corr.index=corr.index.strftime('%b-%Y')
    corrgdp=corrgdp.loc[f"{S.start_sectpub}":]
    corrgdp.index=corrgdp.index.strftime('%b-%Y')
    corrtco=corrtco.loc[f"{S.start_sectpub}":]
    corrtco.index=corrtco.index.strftime('%b-%Y')

    if S.escala_sectpub=="***Millones de ARS***":
        S.data_sectpub=deficit
        S.endeudamiento=endeudamiento
        S.corr=corr
    elif S.escala_sectpub=="***Millones de USD-Oficial***":
        S.data_sectpub=datatco
        S.endeudamiento=endeudamientotco
        S.corr=corrtco
    else:
        S.data_sectpub=datagdp
        S.endeudamiento=endeudamientogdp
        S.corr=corrgdp
    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader('Resultado Fiscal y Financiero')
            plot_deficit(S.escala_sectpub,S.data_sectpub)
    with c2:
        with st.container(border=True):
            st.subheader('Gastos/Ingresos Corrientes')
            plot_ingresos_gastos(S.corr,S.escala_sectpub)
    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader('Deuda Pública')
            #deuda,deuda_mon=load_datos_deuda(2)
            st.radio('Deuda Pública',options=['Endeudamiento Anual Acumulado','Composición de la Deuda Bruta','Pagos de Deuda por Moneda'],label_visibility='collapsed',horizontal=False,key='plot_deuda')
            plot_deuda(S.deuda,S.plot_deuda) if S.plot_deuda=='Composición de la Deuda Bruta' else (plot_deuda(S.deuda_mon,S.plot_deuda) if S.plot_deuda=='Pagos de Deuda por Moneda' else plot_endeudamiento(S.endeudamiento,S.escala_sectpub))
    with c2:
        with st.container(border=True):
            c1,c2=st.columns((0.4,0.6))
            c1.subheader('Gasto Provincial')
            c2.radio('deficit_proc',label_visibility='collapsed',options=['Presupuestado','Ejecutado'],key='deficit_elegido',horizontal=False)
            #data,geo,extras=load_data_map(datetime.now().strftime("%Y%m%d"))
            try:
                make_map(S.data_map,S.geo_map,S.extras_map,S.deficit_elegido)
            except Exception as e:
                st.write(e)