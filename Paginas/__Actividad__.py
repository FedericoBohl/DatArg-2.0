from _globals_ import *
import streamlit as st
from streamlit import session_state as S
import pandas as pd
from Paginas.librerias import get_data
from plotly import graph_objects as go
from plotly.subplots import make_subplots

st.cache_resource(show_spinner=False)
def load_actividad(end):
    his_data=pd.read_csv("His Data/his-actividad.csv",delimiter=";")
    his_data['Unnamed: 0'] = pd.to_datetime(his_data.iloc[:, 0].values, format='%Y-%m-%d')
    his_data.set_index('Unnamed: 0', inplace=True)
    ids=[
        "143.3_NO_PR_2004_A_31",
        "11.3_ISOM_2004_M_39",
        "11.3_ISD_2004_M_26",
        "11.3_AGCS_2004_M_41",
        "11.3_SEGA_2004_M_48",
        "453.1_SERIE_DESEADA_0_0_24_58",
        "33.2_ISAC_SIN_EDAD_0_M_23_56"
    ]
    cols=["EMAE","Campo","Minas","Comercio","Inmobiliaria","IPI","ISAC"]
    data=get_data(ids,start_date="2024-01-01",col_list=cols)
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
    his_data.columns=data.columns
    data.reindex(columns=his_data.columns)
    data=pd.concat([his_data,data],axis=0)

    ids=['3.2_OGP_D_2004_T_17','9.2_PPCDC_2004_T_33']
    pbi=get_data(ids,start_date='2004-01-01',col_list=['PBI Real','PBI Per Cap'])

    return data, pbi

@st.cache_resource(show_spinner=False)
def plot_PBI(data:pd.DataFrame,var:pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data['PBI Real'],name='PBI Real',line=dict(width=4.5),marker_color=navy),secondary_y=True)
    fig.add_trace(go.Bar(x=data.index,y=var['PBI Real'],name='Var %',marker_color='royalblue'),secondary_y=False)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='%',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="Millones de ARS del 2004",showgrid=False, zeroline=False, showline=False)
                                )
    fig['layout']['yaxis2']['type']='log'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_percap(data:pd.DataFrame,var:pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data['PBI Per Cap'],name='PBI Per Cápita',line=dict(width=4.5),marker_color=olive),secondary_y=True)
    fig.add_trace(go.Bar(x=data.index,y=var['PBI Per Cap'],name='Var %',marker_color='lime'),secondary_y=False)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='%',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="Millones de USD",showgrid=False, zeroline=False, showline=False)
                                )
    fig['layout']['yaxis2']['type']='log'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_emae(data:pd.DataFrame,var_m:pd.DataFrame,var_a:pd.DataFrame):
    fig_emae = make_subplots(specs=[[{"secondary_y": True}]])
    fig_emae.add_trace(go.Scatter(x=data.index,y=data['EMAE'],name='EMAE',marker_color=blue),secondary_y=False)
    fig_emae.add_trace(go.Bar(x=var_m.index,y=var_m['EMAE'],name='Var. Mensual',marker_color=var_m['EMAE'].apply(lambda x: 'green' if x >= 0 else 'red'),opacity=0.5,marker_line_color=black,marker_line_width=1),secondary_y=True)
    fig_emae.add_trace(go.Scatter(x=var_a.index,y=var_a['EMAE'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
    fig_emae.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='EMAE',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )
    
    fig_campo = make_subplots(specs=[[{"secondary_y": True}]])
    fig_campo.add_trace(go.Scatter(x=data.index,y=data['Campo'],name='EMAE-Sector Agrícola',marker_color=blue),secondary_y=False)
    fig_campo.add_trace(go.Bar(x=var_m.index,y=var_m['Campo'],name='Var. Mensual',marker_color=var_m['Campo'].apply(lambda x: 'green' if x >= 0 else 'red'),opacity=0.5,marker_line_color=black,marker_line_width=1),secondary_y=True)
    fig_campo.add_trace(go.Scatter(x=var_a.index,y=var_a['Campo'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
    fig_campo.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='EMAE',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )

    fig_minas = make_subplots(specs=[[{"secondary_y": True}]])
    fig_minas.add_trace(go.Scatter(x=data.index,y=data['Minas'],name='EMAE-Minas y Canteras',marker_color=blue),secondary_y=False)
    fig_minas.add_trace(go.Bar(x=var_m.index,y=var_m['Minas'],name='Var. Mensual',marker_color=var_m['Minas'].apply(lambda x: 'green' if x >= 0 else 'red'),opacity=0.5,marker_line_color=black,marker_line_width=1),secondary_y=True)
    fig_minas.add_trace(go.Scatter(x=var_a.index,y=var_a['Minas'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
    fig_minas.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='EMAE',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )

    fig_comercio = make_subplots(specs=[[{"secondary_y": True}]])
    fig_comercio.add_trace(go.Scatter(x=data.index,y=data['Comercio'],name='EMAE-Comercio',marker_color=blue),secondary_y=False)
    fig_comercio.add_trace(go.Bar(x=var_m.index,y=var_m['Comercio'],name='Var. Mensual',marker_color=var_m['Comercio'].apply(lambda x: 'green' if x >= 0 else 'red'),opacity=0.5,marker_line_color=black,marker_line_width=1),secondary_y=True)
    fig_comercio.add_trace(go.Scatter(x=var_a.index,y=var_a['Comercio'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
    fig_comercio.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='EMAE',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )
    
    fig_inmob = make_subplots(specs=[[{"secondary_y": True}]])
    fig_inmob.add_trace(go.Scatter(x=data.index,y=data['Inmobiliaria'],name='EMAE-Inmobiliaria',marker_color=blue),secondary_y=False)
    fig_inmob.add_trace(go.Bar(x=var_m.index,y=var_m['Inmobiliaria'],name='Var. Mensual',marker_color=var_m['Inmobiliaria'].apply(lambda x: 'green' if x >= 0 else 'red'),opacity=0.5,marker_line_color=black,marker_line_width=1),secondary_y=True)
    fig_inmob.add_trace(go.Scatter(x=var_a.index,y=var_a['Inmobiliaria'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
    fig_inmob.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='EMAE',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )

    return {'EMAE-Nivel General':fig_emae,'Agricultura, ganadería, caza y silvicultura':fig_campo,'Explotación de minas y canteras':fig_minas,'Comercio mayorista, minorista y reparaciones':fig_comercio,'Actividades inmobiliarias, empresariales y de alquiler':fig_inmob}

@st.cache_resource(show_spinner=False)
def plot_ipi(data:pd.DataFrame,var_m:pd.DataFrame,var_a:pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data,name='IPI',marker_color=blue),secondary_y=False)
    fig.add_trace(go.Bar(x=var_m.index,y=var_m,name='Var. Mensual',marker_color=var_m.apply(lambda x: 'green' if x >= 0 else 'red'),opacity=0.5,marker_line_color=black,marker_line_width=1),secondary_y=True)
    fig.add_trace(go.Scatter(x=var_a.index,y=var_a,name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='IPI',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_isac(data:pd.DataFrame,var_m:pd.DataFrame,var_a:pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data,name='ISAC',marker_color=blue),secondary_y=False)
    fig.add_trace(go.Bar(x=var_m.index,y=var_m,name='Var. Mensual',marker_color=var_m.apply(lambda x: 'green' if x >= 0 else 'red'),opacity=0.5,marker_line_color=black,marker_line_width=1),secondary_y=True)
    fig.add_trace(go.Scatter(x=var_a.index,y=var_a,name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='ISAC',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

def make_actividad_web():
    actividad=S.actividad_.copy()
    pbi=S.pbi_.copy()
    c1,c2=st.columns((0.7,0.3),vertical_alignment='bottom')
    c1.number_input(value=2016,label='Datos desde',min_value=2004,max_value=2024,key="start_actividad")
    c2.link_button(":blue[**Descargar datos:\nActividad**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/QfXi8hfJF_kggFaKFQAAAAAA7qhKZI81Oq7vDg",use_container_width=True)
    var_men_act=actividad.pct_change()*100
    var_an_act=actividad.pct_change(periods=12)*100
    var_pbi=pbi.pct_change()
    actividad=actividad.loc[f"{S.start_actividad}":]
    var_men_act=var_men_act.loc[f"{S.start_actividad}":]
    var_an_act=var_an_act.loc[f"{S.start_actividad}":]
    pbi=pbi.loc[f"{S.start_actividad}":]
    pbi.index=pbi.index.strftime('%b-%Y')
    var_pbi=var_pbi.loc[f"{S.start_actividad}":]
    var_pbi.index=var_pbi.index.strftime('%b-%Y')
    actividad.index=actividad.index.strftime('%b-%Y')
    var_men_act.index=var_men_act.index.strftime('%b-%Y')
    var_an_act.index=var_an_act.index.strftime('%b-%Y')
    with st.container(border=False):
        c1,c2=st.columns([0.3,0.7],vertical_alignment='center')
        c1.radio('¿Qué indicador de actividad desea ver?',options=['EMAE','IPI','ISAC'],horizontal=False,key='indicador_actividad')
        with c2:
            if S.indicador_actividad=='EMAE':
                st.subheader('EMAE')
                st.selectbox('EMAE-elegido',label_visibility='collapsed',options=['EMAE-Nivel General','Agricultura, ganadería, caza y silvicultura','Explotación de minas y canteras','Comercio mayorista, minorista y reparaciones','Actividades inmobiliarias, empresariales y de alquiler'],key='emae_elegido')
                emae_plots=plot_emae(actividad,var_men_act,var_an_act)
                st.plotly_chart(emae_plots[S.emae_elegido],config={'displayModeBar': False},use_container_width=True)
            elif S.indicador_actividad=='IPI':
                st.subheader('Industria')
                plot_ipi(actividad['IPI'].dropna(),var_men_act['IPI'].dropna(),var_an_act['IPI'].dropna())
            else:
                st.subheader('Construcción')
                plot_isac(actividad['ISAC'].dropna(),var_men_act['ISAC'].dropna(),var_an_act['ISAC'].dropna())
        if S.indicador_actividad=='EMAE':
            _={'EMAE-Nivel General':'EMAE',
             'Agricultura, ganadería, caza y silvicultura':'Campo',
             'Explotación de minas y canteras':'Minas',
             'Comercio mayorista, minorista y reparaciones':'Comercio',
             'Actividades inmobiliarias, empresariales y de alquiler':'Inmobiliaria'}
            with c1.container(border=True):
                data=actividad.dropna(subset=[_[S.emae_elegido]])
                var_data=var_men_act.dropna(subset=[_[S.emae_elegido]])
                st.metric(label=f"Último Dato ({data.index[-1]})",value=round(data.iloc[-1][_[S.emae_elegido]],2),delta=f"{round(var_data.iloc[-1][_[S.emae_elegido]],2)}%")
        else:
            with c1.container(border=True):
                data=actividad.dropna(subset=[S.indicador_actividad])
                var_data=var_men_act.dropna(subset=[S.indicador_actividad])
                st.metric(label=f"Último Dato ({data.index[-1]})",value=round(data.iloc[-1][S.indicador_actividad],2),delta=f"{round(var_data.iloc[-1][S.indicador_actividad],2)}%")
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.subheader('PBI Real')
        plot_PBI(pbi,var_pbi)
    with c2.container(border=True):
        st.subheader('PBI per cápita')   
        plot_percap(pbi,var_pbi)
    st.divider()
    st.caption('Datos Desestacionalizados excepto para el PBI Per Cápita')