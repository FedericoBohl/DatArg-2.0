from _globals_ import *
import streamlit as st
from streamlit import session_state as S
import pandas as pd
from librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

@st.cache_resource(show_spinner=False)
def load_sect_ext(end):
    bop=pd.read_csv("His Data/his-BOP.csv",delimiter=";")
    bop['Unnamed: 0'] = pd.to_datetime(bop.iloc[:, 0].values, format='%Y-%m-%d')
    bop.set_index('Unnamed: 0', inplace=True)
    ids=["160.2_TL_CUENNTE_0_T_22",
        "160.2_TL_CUENTAL_0_T_20",
        "160.2_TL_CUENERA_0_T_23",
        "160.2_AVOS_RERVA_0_T_15",
        "160.2_ERES_OMTOS_0_T_23",
        "82.2_ITI_2004_T_27",
        "9.2_PDPC_2004_T_30",
        "74.2_SC_0_T_15"
        ]
    cols=["CC","CK","CF","VarR","Errores","ToT","PBIUSD","XN"]
    data=get_data(ids,start_date="2023-10-01",col_list=cols)
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
    data.reindex(columns=bop.columns)
    data=pd.concat([bop,data],axis=0)
    data['CF(MBP5)']=-(data['CF']-data['VarR'])
    tot=data['ToT']
    
    datagdp=data.rolling(4).sum()
    datagdp['PBIUSD']=data['PBIUSD']
    for col in data.columns.to_list():
        if col=='PBIUSD':pass
        else: datagdp[col]=100*datagdp[col]/(datagdp['PBIUSD']*4)


    ica_his=pd.read_csv("His Data/his-ica.csv",delimiter=";")
    ica_his['Unnamed: 0'] = pd.to_datetime(ica_his.iloc[:, 0].values, format='%Y-%m-%d')
    ica_his.set_index('Unnamed: 0', inplace=True)
    ids=["74.2_IET_0_T_16",
        "74.2_IEPP_0_T_35",
        "74.2_IEMOA_0_T_48",
        "74.2_IEMOI_0_T_46",
        "74.2_IECE_0_T_35",
        "74.2_IIT_0_T_25",
        "74.2_IIBCA_0_T_32",
        "74.2_IIBI_0_T_36",
        "74.2_IICL_0_T_42",
        "74.2_IIPABC_0_T_50",
        "74.2_IIBCO_0_T_32",
        "74.2_IIVAP_0_T_49",
        "74.2_IIR_0_T_23",
        "9.2_PDPC_2004_T_30"
        ]
    cols=["Expo Totales","PP","MOA","MOI","Combustibles y Energía","Impo Totales","Bienes de capital","Bienes intermedios","Combustibles y Lubricantes","Piezas y acces","Bienes de consumo","Vehículos","Resto","PBIUSD"]
    ica=get_data(ids,start_date="2023-10-01",col_list=cols)
    ica.index = pd.to_datetime(ica.index, format='%Y-%m-%d')
    ica.reindex(columns=ica_his.columns)
    ica=pd.concat([ica_his,ica],axis=0)
    
    icagdp=ica.rolling(4).sum()
    icagdp['PBIUSD']=ica['PBIUSD']
    for col in ica.columns.to_list():
        if col=='PBIUSD':pass
        else: icagdp[col]=100*icagdp[col]/(icagdp['PBIUSD']*4)

    return data.rolling(4).sum()[4:],datagdp.dropna(),ica.rolling(4).sum()[4:],icagdp.dropna(),tot

@st.cache_resource(show_spinner=False)
def plot_bop(data,escala,errores):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['CC'],name='CC',marker_color=maroon,line=dict(width=5)))
    fig.add_trace(go.Scatter(x=data.index,y=data['CK']+data['CF(MBP5)'],name='CF+CK',marker_color=navy,line=dict(width=5)))
    fig.add_trace(go.Bar(x=data.index,y=data['VarR'],name='Var. R',marker_color=data["VarR"].apply(lambda x: green if x >= 0 else red),
                                    showlegend=True, opacity=1, marker_line_color=black,marker_line_width=1))
    if errores==True:fig.add_trace(go.Bar(x=data.index,y=data['Errores'],name='Errores y Omisiones',marker_color=gray))
    fig.update_xaxes(type='category',tickmode='array',showticklabels=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bordercolor='black',
                                    borderwidth=2),
                                    yaxis=dict(showgrid=False, zeroline=True, showline=True)
                                )
    if escala=="***Millones de USD***":
        fig['layout']['yaxis']['title']='Millones de USD'
        #fig['layout']['yaxis']['type']='log'   #Dado a que hay valores negativos no sirve
    else:
        fig['layout']['yaxis']['title']='PP del PBI en USD'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_balcom(data,escala):
    fig = make_subplots(specs=[[{"secondary_y": True}]])    
    fig.add_trace(go.Scatter(x=data.index,y=data["XN"],fill="tozeroy",marker_color="#3A4D39",fillcolor="#739072",name="Balance Comercial"))
    _=S.tot.rolling(4).mean().dropna()
    _=_.loc[f"{S.start_sectext}":]
    _.index=_.index.strftime('%b-%Y')
    fig.add_trace(go.Scatter(x=data.index,y=_.values.tolist(),name="ToT",line=dict(width=3),marker_color='#FF7F3E'),secondary_y=True)
    _=S.TCR.resample('Q').mean().rolling(4).mean().dropna()
    _=_.iloc[4:]*100/69.82120981
    _=_.loc[f"{S.start_sectext}":]
    _.index=_.index.strftime('%b-%Y')
    fig.add_trace(go.Scatter(x=data.index,y=_.values.tolist(),name="TCR",line=dict(width=4,dash="dot"),marker_color="#F19ED2"),secondary_y=True)
    fig.add_hline(y=0)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="ToT - TCR (Ene-2004=100)",showgrid=True, zeroline=True, showline=True)
                                )
    if escala=="***Millones de USD***":
        fig['layout']['yaxis']['title']='Millones de USD'
        #fig['layout']['yaxis']['type']='log'   #Dado a que hay valores negativos no sirve
    else:
        fig['layout']['yaxis']['title']='PP del PBI en USD'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    del _,fig

@st.cache_resource(show_spinner=False)
def plot_destXM(escala,año):
    destX=pd.read_excel('His Data/Data SectExt.xlsx',sheet_name=f"Dest X")
    destX["Share"]=round(destX[año]*100/sum(destX[año]),2)
    destX["rounded"]=round(destX[año],2)
    destM=pd.read_excel('His Data/Data SectExt.xlsx',sheet_name=f"Dest M")
    destM["Share"]=round(destM[año]*100/sum(destM[año]),2)
    destM["rounded"]=round(destM[año],2)

    color_map = {
        'América Latina y el Caribe': 'rgb(255, 179, 186)',  # Rosa pastel
        'Canadá': 'rgb(255, 223, 186)',                      # Naranja pastel
        'Estados Unidos': 'rgb(186, 255, 239)',              # Verde agua pastel 
        'Unión Europea': 'rgb(186, 255, 201)',               # Verde pastel
        'Reino Unido': 'rgb(186, 255, 255)',                 # Azul pastel
        'Suiza': 'rgb(186, 225, 255)',                       # Azul claro pastel
        'India': 'rgb(255, 205, 186)',                       # Durazno pastel
        'Rusia': 'rgb(255, 186, 255)',                       # Rosa claro pastel
        'Asia Pacífico': 'rgb(186, 186, 255)',               # Morado pastel
        'Israel': 'rgb(210, 255, 173)',                      # Verde claro pastel
        'Australia': 'rgb(255, 248, 201)',                   # Beige pastel
        'Nueva Zelanda': 'rgb(220, 220, 220)',               # Gris claro pastel
        'Africa':'rgb(255, 255, 186)',                       # Amarillo pastel
        'Otros': 'rgb(255, 214, 214)'                        # Rosa medio pastel
    }


    figX = px.sunburst(destX, path=['Continente', 'Alianza-Pais', 'Pais'],
                       values=destX['rounded' if escala=='Valor (USD)' else  'Share'],
                       color='Continente',color_discrete_map=color_map)
    if escala=="Porcentaje del Total":    
        figX.update_traces(
            hovertemplate="<br>".join([
            "<b><b>%{label}",
            "<b>Proporción del Total<b>: %{value}%"
            ])
            )

    else:
        figX.update_traces(
            hovertemplate="<br>".join([
            "<b><b>%{label}",
            "<b>Valor<b>: %{value} MM USD"
            ])
            )   
    figX.update_layout(margin=dict(l=1, r=1, t=75, b=1),height=600)

    figM = px.sunburst(destM, path=['Continente', 'Alianza-Pais', 'Pais'],
                       values=destM['rounded' if escala=='Valor (USD)' else  'Share'],
                       color='Continente',color_discrete_map=color_map)
    if escala=="Porcentaje del Total":    
        figM.update_traces(
            hovertemplate="<br>".join([
            "<b><b>%{label}",
            "<b>Proporción del Total<b>: %{value}%"
            ])
            )
        
    else:
        figM.update_traces(
            hovertemplate="<br>".join([
            "<b><b>%{label}",
            "<b>Valor<b>: %{value} MM USD"
            ])
            )   
    figM.update_layout(margin=dict(l=1, r=1, t=75, b=1),height=600)

    return figX,figM

@st.cache_resource(show_spinner=False)
def plot_ica(data,escala):
    figX=go.Figure()
    figX.add_trace(go.Bar(x=data.index,y=data["PP"],name="Productos Primarios",marker_color=red))
    figX.add_trace(go.Bar(x=data.index,y=data["MOA"],name="Manufacturas de Origen Agropecuario",marker_color=green))
    figX.add_trace(go.Bar(x=data.index,y=data["MOI"],name="Manufacturas de Origen Industrial",marker_color=blue))
    figX.add_trace(go.Bar(x=data.index,y=data["Combustibles y Energía"],name="Combustibles y Energía",marker_color=yellow))
    figX.add_trace(go.Scatter(x=data.index,y=data["Expo Totales"],name="Total",line=dict(width=4),marker_color=black))
    figX.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),
        barmode="stack",height=450, 
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.75,
            xanchor="right",
            x=0.95,
            bordercolor=black,
            borderwidth=2
        ),
        yaxis=dict(showgrid=False, zeroline=True, showline=True)
    )

    figM=go.Figure()
    figM.add_trace(go.Bar(x=data.index,y=data["Bienes de capital"],name="Bienes de Capital",marker_color=red))
    figM.add_trace(go.Bar(x=data.index,y=data["Piezas y acces"],name="Piezas y Acc. para bienes de capital",marker_color=teal))
    figM.add_trace(go.Bar(x=data.index,y=data["Bienes intermedios"],name="Bienes Intermedios",marker_color=green))
    figM.add_trace(go.Bar(x=data.index,y=data["Bienes de consumo"],name="Bienes de Consumo",marker_color=blue))
    figM.add_trace(go.Bar(x=data.index,y=data["Vehículos"],name="Vehículos",marker_color=yellow))
    figM.add_trace(go.Bar(x=data.index,y=data["Combustibles y Lubricantes"],name="Combustibles y Lubricantes",marker_color=purple))            
    figM.add_trace(go.Bar(x=data.index,y=data["Resto"],name="Otros",marker_color=gray))
    figM.add_trace(go.Scatter(x=data.index,y=data["Impo Totales"],name="Total",line=dict(width=4),marker_color=black))
    figM.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),
        barmode="stack",height=450, 
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.75,
            xanchor="right",
            x=0.95,
            bordercolor=black,
            borderwidth=2
        ),
        yaxis=dict(showgrid=False, zeroline=True, showline=True)
    )
    if escala=="***Millones de USD***":
        figX['layout']['yaxis']['title']='Millones de USD'
        figX['layout']['yaxis']['type']='log'
        figM['layout']['yaxis']['title']='Millones de USD'
        figM['layout']['yaxis']['type']='log'

    else:
        figX['layout']['yaxis']['title']='PP del PBI en USD'
        figM['layout']['yaxis']['title']='PP del PBI en USD'
    return figX,figM

def make_sect_ext_web():
    bop=S.bop
    bopgdp=S.bopgdp
    ica=S.ica
    icagdp=S.icagdp
    c1,c2=st.columns((0.7,0.3),vertical_alignment='center')
    with c1:
        with st.expander(label='Ajustar Gráficas',icon=":material/settings:"):
            c11,c12=st.columns((0.3,0.7))
            with c11: st.radio("Escala de los datos",options=["***Millones de USD***","***% del PBI***"],key="escala_sectext")
            with c12: st.number_input(value=2016,label='Datos desde',min_value=2006,max_value=2024,key="start_sectext")
    with c2:
        st.link_button(":blue[**Descargar datos:\nSector Externo**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/QfXi8hfJF_kggFaKFQAAAAAA7qhKZI81Oq7vDg",use_container_width=True)
    bop=bop.loc[f"{S.start_sectext}":]
    bop.index=bop.index.strftime('%b-%Y')
    bopgdp=bopgdp.loc[f"{S.start_sectext}":]
    bopgdp.index=bopgdp.index.strftime('%b-%Y')
    ica=ica.loc[f"{S.start_sectext}":]
    ica.index=ica.index.strftime('%b-%Y')
    icagdp=icagdp.loc[f"{S.start_sectext}":]
    icagdp.index=icagdp.index.strftime('%b-%Y')
    if S.escala_sectext=='***Millones de USD***':
        S.bop=bop
        S.ica=ica
    else:
        S.bop=bopgdp
        S.ica=icagdp
    c1,c2=st.columns(2)
    with c1.container(border=True):
        c11,c12=st.columns((0.7,0.3))
        c11.subheader('Balance de Pagos')
        c11.latex(r'''CC+CF+CK=\Delta R''')
        c12.checkbox('Agregar Errores y Omisiones',value=True,key='erroresyomisiones')
        plot_bop(S.bop,S.escala_sectext,S.erroresyomisiones)
        st.caption('Suma Interanual')
    with c2.container(border=True):
        st.subheader('Balance Comercial - ToT + TCR')
        plot_balcom(S.bop,S.escala_sectext)
        st.caption('El Tipo de Cambio es re-escalado por conveniencia visual con base Enero 2004 = 100.')
        st.caption('El Balance Comercial viene dado como suma interanual, por lo que el tipo de cambio y los terminos de intercambio son los promedios anuales móviles.')
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.subheader('Destino de las Expo/Importaciones')
        c11,c12=st.columns(2)
        c11.number_input('Año',2004,2023,value=2023,step=1,key='year_destXM')
        c12.radio('Destino expo/impo',label_visibility='collapsed',options=['Valor (USD)','Porcentaje del Total'],key='escalaXM')
        ex_plot,im_plot=plot_destXM(S.escalaXM,S.year_destXM)
        ex,im=st.tabs(['Exportaciones','Importaciones'])
        ex.plotly_chart(ex_plot,config={'displayModeBar': False},use_container_width=True)
        im.plotly_chart(im_plot,config={'displayModeBar': False},use_container_width=True)
    with c2.container(border=True):
        st.subheader('Intercambio Comercial Argentino')
        ex_plot,im_plot=plot_ica(S.ica,S.escala_sectext)
        ex,im=st.tabs(['Exportaciones','Importaciones'])
        ex.plotly_chart(ex_plot,config={'displayModeBar': False},use_container_width=True)
        im.plotly_chart(im_plot,config={'displayModeBar': False},use_container_width=True)
