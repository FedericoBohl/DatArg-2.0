from _globals_ import *
import streamlit as st
from streamlit import session_state as S
import pandas as pd
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.filters import hp_filter
import statsmodels.api as sm


@st.cache_data(show_spinner=False)
def plot_agregados(escala,bcra: pd.DataFrame, tasas: pd.DataFrame):
    st.subheader("Agregados Monetarios - Tasa de pol. mon. - Inflación interanual")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig.add_trace(go.Bar(x=bcra.index, y=bcra['M1/PBI']*100, name='', marker_color=red,showlegend=False),secondary_y=False)
    fig.add_trace(go.Scatter(x=bcra.index, y=bcra['M1'], name='M1', marker_color="red",showlegend=True, line=dict(width=2.5),fill="tonexty",fillcolor=red),secondary_y=False)
    fig.add_trace(go.Scatter(x=bcra.index, y=bcra['M2'], name='M2', marker_color="green",showlegend=True, line=dict(width=2.5),fill="tonexty",fillcolor=green),secondary_y=False)
    fig.add_trace(go.Scatter(x=bcra.index, y=bcra['M3'], name='M3', marker_color="blue",showlegend=True, line=dict(width=2.5),fill="tonexty",fillcolor=blue),secondary_y=False)
    fig.add_trace(go.Scatter(x=tasas.index,y=tasas["Tasa de Politica Monetaria"],name="Tasa Pol. Mon.",marker_color=black,line=dict(width=3)),secondary_y=True)
    #fig.add_trace(go.Scatter(x=bcra.index,y=infl*100,name="Inflación",marker_color=black,line=dict(width=2.5,dash="dash")),secondary_y=True)
    fig.update_xaxes(type='category',tickmode='array',showticklabels=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0.2,height=450,legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bordercolor='black',
                                    borderwidth=2),
                                    yaxis=dict(showgrid=False, zeroline=True, showline=True),
                                    yaxis2=dict(title='%-Tasas', side='right',showgrid=False, zeroline=True, showline=True)
                                )
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
        fig['layout']['yaxis']['type']='log'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_data(show_spinner=False)
def plot_BM(escala, bcra: pd.DataFrame):
    st.subheader("Base Monetaria")
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=bcra.index,y=(bcra["BM"]),name="BM",marker_color=maroon, line=dict(width=3.5)))
    fig.add_trace(go.Scatter(x=bcra.index,y=(bcra["Circulante"]),name="Circulante",marker_color=navy, line=dict(width=3.5)))
    fig.add_trace(go.Bar(x=bcra.index,y=(bcra["CPP"]),name="CPP",marker_color=teal))
    fig.add_trace(go.Bar(x=bcra.index,y=(bcra["CB"]),name="EB",marker_color="coral"))
    fig.add_trace(go.Bar(x=bcra.index,y=(bcra["BM"]-bcra["Circulante"]),name="CC-BCRA",marker_color=olive))
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
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_data(show_spinner=False)
def plot_pasivos_rem(escala,bcra: pd.DataFrame,tasas: pd.DataFrame): # El botón de BM está andando mal
    st.subheader("Pasivos Remunerados")
    #if not st.checkbox("%BM",value=False,key="BM_bcra"):
    fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": True}], [{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=bcra.index, y=(bcra["LeLiq"]), name='LELIQ', marker_color='navy'), row=1, col=1, secondary_y=False)
    fig.add_trace(go.Bar(x=bcra.index, y=(bcra["LEBAC-NOBAC"]), name='LEBAC', marker_color='gray'), row=1, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=tasas.index, y=tasas["Tasa de Politica Monetaria"], name="Tasa Pol. Mon.", marker_color='red', line=dict(width=3)), row=1, col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=bcra.index, y=bcra["Pases Netos"], name='Pases Netos', marker_color="rgb(139,224,164)", line=dict(width=3), fill='tozeroy'), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=tasas.index, y=tasas["Tasa Pases Pasivos (1 dia)"], name="Tasa Pasiva", marker_color="orange", line=dict(width=3)), row=2, col=1, secondary_y=True)                
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),height=600, barmode="relative", legend=dict(
        orientation="h",
        yanchor="top",  # Cambiado a 'top'
        y=1.2,          # Cambiado a 1.0
        xanchor="center",
        x=0.5,
        bordercolor='black',
        borderwidth=2
    ))
    fig.update_yaxes( row=1, col=1, showgrid=False, zeroline=True, showline=True)
    fig.update_yaxes( row=2, col=1, showgrid=False, zeroline=True, showline=True)
    # Configurar el primer subgráfico para ocultar el eje x
    fig.update_xaxes(
        title_text='',
        visible=False,
        row=1,
        col=1
    )
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
        fig['layout']['yaxis']['type']='log'
        fig['layout']['yaxis3']['title']='Millones de ARS'
        fig['layout']['yaxis3']['type']='log'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
        fig['layout']['yaxis3']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
        fig['layout']['yaxis3']['title']='PP del PBI'
    fig['layout']['yaxis2']['title']='%-Tasa'
    fig['layout']['yaxis4']['title']='%-Tasa'
    #else: 
    #    fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": True}], [{"secondary_y": True}]])
    #    fig.add_trace(go.Bar(x=bcra.index, y=(bcra["LeLiq"]/bcra["BM"]), name='LELIQ', marker_color='navy'), row=1, col=1, secondary_y=False)
    #    fig.add_trace(go.Bar(x=bcra.index, y=(bcra["LEBAC-NOBAC"]/bcra["BM"]), name='LEBAC', marker_color='gray'), row=1, col=1, secondary_y=False)
    #    fig.add_trace(go.Scatter(x=tasas.index, y=tasas["Tasa de Politica Monetaria"], name="Tasa Pol. Mon.", marker_color='red', line=dict(width=3)), row=1, col=1, secondary_y=True)
    #    fig.add_trace(go.Scatter(x=bcra.index, y=(bcra["Pases Netos"]/bcra["BM"]), name='Pases Netos', marker_color="rgb(139,224,164)", line=dict(width=3), fill='tozeroy'), row=2, col=1, secondary_y=False)
    #    fig.add_trace(go.Scatter(x=tasas.index, y=tasas["Tasa Pases Pasivos (1 dia)"], name="Tasa Pasiva", marker_color="orange", line=dict(width=3)), row=2, col=1, secondary_y=True)                

    #    fig.update_layout(margin=dict(l=1, r=1, t=75, b=1),height=600, barmode="relative", legend=dict(
    #        orientation="h",
    #        yanchor="top",  # Cambiado a 'top'
    #        y=1.2,          # Cambiado a 1.0
    #        xanchor="center",
    #        x=0.5,
    #        bordercolor='black',
    #        borderwidth=2
    #    ))
    #    fig.update_yaxes(row=1, col=1, showgrid=False, zeroline=True, showline=True)
    #    fig.update_yaxes(row=2, col=1, showgrid=False, zeroline=True, showline=True)

    #    # Configurar el primer subgráfico para ocultar el eje x
    #    fig.update_xaxes(
    #        title_text='',
    #        visible=False,
    #        row=1,
    #        col=1
    #    )
    #    fig['layout']['yaxis']['title']='Puntos de la BM'
    #    fig['layout']['yaxis2']['title']='%-Tasa'
    #    fig['layout']['yaxis3']['title']='Puntos de la BM'
    #    fig['layout']['yaxis4']['title']='%-Tasa'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
        
@st.cache_data(show_spinner=False)
def plot_fin_mon(escala,bcra: pd.DataFrame):
    st.subheader("Financiamiento monetario del Tesoro")
    fig=go.Figure()
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["Tit Publicos"],name="Títulos Públicos",marker_color=lavender))
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["Adeltantos Transitorios"],name="Adeltantos Transitorios",marker_color=teal))
    fig.add_trace(go.Scatter(x=bcra.index,y=bcra["Adeltantos Transitorios"]+bcra["Tit Publicos"],name="Total",showlegend=False,marker_color=brown,line=dict(width=3.5)))
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="relative",bargap=0.2,height=450,legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(showgrid=False, zeroline=True, showline=True),
                                )
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
        fig['layout']['yaxis']['type']='log'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_data(show_spinner=False)
def plot_varBM(escala,bcra:pd.DataFrame,roll:int):
    bcra=bcra.rolling(roll).sum()[roll:]#.dropna()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bcra.index,y=bcra["Var. BM"],name="Var. BM Total",line=dict(width=3.5),marker_color="#0B1623"))
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["Neto compra divisas"],name="Neto-Compra de divisas",marker_color=cyan))
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["Oper con el Tesoro"],name="Operaciones con el tesoro",marker_color=orange))
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["Pases y Redescuentos"],name="Pases y Redescuentos",marker_color=pink))
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["LEBAC-NOBAC"],name="LEBAC-NOBAC",marker_color=brown))
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["Rescate Cuasimonedas"],name="Rescate Cuasimonedas",marker_color=yellow))
    fig.add_trace(go.Bar(x=bcra.index,y=bcra["Otros-Var.BM"],name="Otros",marker_color=gray))
    fig.update_layout(margin=dict(l=1, r=1, t=75, b=1),barmode="relative",bargap=0.5,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=-1.05,
                                        xanchor="center",
                                        x=0.5,
                                    bordercolor=black,
                                    borderwidth=2
                                ),yaxis=dict(showgrid=False, zeroline=True, showline=True))
    fig.update_xaxes(rangeslider_visible=True)
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
    elif escala=="***Millones de USD-Oficial***":
        pass
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)


@st.cache_data(show_spinner=False)
def plot_depositos(escala, bcra:pd.DataFrame, tasas: pd.DataFrame)->None:
    st.subheader("Depósitos & Rendimiento de los Plazos Fijos")
    fig=make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=bcra.index,y=bcra["Depositos"],name="Depósitos",marker_color=purple,line=dict(width=3),fill='tozeroy'),secondary_y=False)
    fig.add_trace(go.Scatter(x=bcra.index,y=tasas["Badlar"],name="Tasa Badlar",marker_color="yellow",line=dict(width=4)),secondary_y=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),height=450, legend=dict(
                                            orientation="h",
                                            entrywidth=70,
                                            yanchor="bottom",
                                            y=1.02,
                                            xanchor="right",
                                            x=1,
                                            bordercolor=black,
                                            borderwidth=2
                                        ),
                                yaxis=dict(showgrid=False, zeroline=True, showline=True),
                                yaxis2=dict(showgrid=False, zeroline=True, showline=True,title="%-Tasa")
                                )
    if escala=="***Millones de ARS***":
        fig['layout']['yaxis']['title']='Millones de ARS'
        fig['layout']['yaxis']['type']='log'
    elif escala=="***Millones de USD-Oficial***":
        fig['layout']['yaxis']['title']='Millones de USD-TC Oficial'
    else:
        fig['layout']['yaxis']['title']='PP del PBI'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_data(show_spinner=False)
def plot_reservas(reservas): # Está andando medio mal, no reacciona bien con el botón
    st.subheader("Reservas Internacionales & Tipo de Cambio Real Multilateral")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #if st.checkbox("Post Convertibilidad",value=True,key='reservas_post'):
    _,tcreq=sm.tsa.filters.hpfilter(reservas["TCR"],129600)
    st.write(reservas["TCR"]) 
    st.write(tcreq)
    fig.add_trace(go.Scatter(x=reservas.index, y=reservas["TCR"], name="TCR", marker_color="#EF5A6F", line=dict(width=2)), secondary_y=True)
    fig.add_trace(go.Scatter(x=reservas.index, y=tcreq, name="TCR de equilibrio", marker_color="#D4BDAC", line=dict(width=2,dash="dash")), secondary_y=True)
    fig.add_trace(go.Scatter(x=reservas.index, y=reservas["Res Int"], name="Reservas", marker_color="#536493", line=dict(width=3),fill="tozeroy"), secondary_y=False)

    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),
        height=450, 
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bordercolor="Black",
            borderwidth=2
        ),
        yaxis=dict(showgrid=False, zeroline=True, showline=True, title="Millones de USD-Oficial"),
        yaxis2=dict(showgrid=False, zeroline=True, showline=True, title="ITCRM"),
        xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1,
                                label="1y",
                                step="year",
                                stepmode="backward"),
                            dict(count=5,
                                label="5y",
                                step="year",
                                stepmode="backward"),
                            dict(count=10,
                                label="10y",
                                step="year",
                                stepmode="backward"),
                                dict(step="all")
                        ])
                    ),
                    rangeslider=dict(
                        visible=False
                    )
                )
    )
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)
    st.caption("El TCR es una elaboración propia en base el IPC de EEUU, el IPC ajustado de la sección Precios y el Tipo de cambio nominal oficial")




