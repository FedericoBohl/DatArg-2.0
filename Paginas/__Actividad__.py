from librerias import *

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
    fig.add_trace(go.Scatter(x=data.index,y=data['PBI Real'],name='PBI Real',line=dict(width=4.5),marker_color=navy),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=var['PBI Real'],name='Var %',marker_color='royalblue'),secondary_y=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='Millones de ARS del 2004',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False)
                                )
    fig['layout']['yaxis']['type']='log'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_percap(data:pd.DataFrame,var:pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data['PBI Per Cap'],name='PBI Per Cápita',line=dict(width=4.5),marker_color=olive),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=var['PBI Per Cap'],name='Var %',marker_color='lime'),secondary_y=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='Millones de USD',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=False, zeroline=False, showline=False,overlaying='y')
                                )
    fig['layout']['yaxis']['type']='log'
    st.plotly_chart(fig,config={'displayModeBar': False},use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_emae(data:pd.DataFrame,var_m:pd.DataFrame,var_a:pd.DataFrame):
    fig_emae = make_subplots(specs=[[{"secondary_y": True}]])
    fig_emae.add_trace(go.Scatter(x=data.index,y=data['EMAE'],name='EMAE',marker_color=blue),secondary_y=False)
    fig_emae.add_trace(go.Bar(x=data.index,y=var_m['EMAE'],name='Var. Mensual',marker_color=green),secondary_y=True)
    fig_emae.add_trace(go.Scatter(x=data.index,y=var_a['EMAE'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
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
    fig_campo.add_trace(go.Bar(x=data.index,y=var_m['Campo'],name='Var. Mensual',marker_color=green),secondary_y=True)
    fig_campo.add_trace(go.Scatter(x=data.index,y=var_a['Campo'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
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
    fig_minas.add_trace(go.Bar(x=data.index,y=var_m['Minas'],name='Var. Mensual',marker_color=green),secondary_y=True)
    fig_minas.add_trace(go.Scatter(x=data.index,y=var_a['Minas'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
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
    fig_comercio.add_trace(go.Bar(x=data.index,y=var_m['Comercio'],name='Var. Mensual',marker_color=green),secondary_y=True)
    fig_comercio.add_trace(go.Scatter(x=data.index,y=var_a['Comercio'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
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
    fig_inmob.add_trace(go.Bar(x=data.index,y=var_m['Inmobiliaria'],name='Var. Mensual',marker_color=green),secondary_y=True)
    fig_inmob.add_trace(go.Scatter(x=data.index,y=var_a['Inmobiliaria'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
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
    fig.add_trace(go.Scatter(x=data.index,y=data['IPI'],name='IPI',marker_color=blue),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=var_m['IPI'],name='Var. Mensual',marker_color=green),secondary_y=True)
    fig.add_trace(go.Scatter(x=data.index,y=var_a['IPI'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
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
    fig.add_trace(go.Scatter(x=data.index,y=data['ISAC'],name='ISAC',marker_color=blue),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=var_m['ISAC'],name='Var. Mensual',marker_color=green),secondary_y=True)
    fig.add_trace(go.Scatter(x=data.index,y=var_a['ISAC'],name='Var. Interanual',line=dict(dash='dashdot',width=1.5),marker_color=lavender),secondary_y=True)
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
    actividad,pbi=load_actividad(datetime.now().strftime("%Y%m%d"))
    c1,c2=st.columns((0.7,0.3))
    c1.number_input(value=2016,label='Datos desde',min_value=2004,max_value=2024,key="start_actividad")
    c2.link_button(":blue[**Descargar datos:\nActividad**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/QfXi8hfJF_kggFaKFQAAAAAA7qhKZI81Oq7vDg",use_container_width=True)
    var_men_act=actividad.pct_change()
    var_an_act=actividad.pct_change(periods=12)
    var_pbi=pbi.pct_change()
    if S.start_actividad>2016:
        actividad=actividad.loc[f"{S.start_actividad}":]
        actividad.index=actividad.index.strftime('%b-%Y')
        var_men_act=var_men_act.loc[f"{S.start_actividad}":]
        var_men_act.index=var_men_act.index.strftime('%b-%Y')
        var_an_act=var_an_act.loc[f"{S.start_actividad}":]
        var_an_act.index=var_an_act.index.strftime('%b-%Y')
    pbi=pbi.loc[f"{S.start_actividad}":]
    pbi.index=pbi.index.strftime('%b-%Y')
    var_pbi=var_pbi.loc[f"{S.start_actividad}":]
    var_pbi.index=var_pbi.index.strftime('%b-%Y')

    c1,c2,c3=st.columns(3)
    with c1.container(border=True):
        c11,c12=st.columns((0.3,0.7))
        c11.subheader('EMAE')
        c12.selectbox('EMAE-elegido',label_visibility='collapsed',options=['EMAE-Nivel General','Agricultura, ganadería, caza y silvicultura','Explotación de minas y canteras','Comercio mayorista, minorista y reparaciones','Actividades inmobiliarias, empresariales y de alquiler'],key='emae_elegido')
        emae_plots=plot_emae(actividad,var_men_act,var_an_act)
        st.plotly_chart(emae_plots[S.emae_elegido],config={'displayModeBar': False},use_container_width=True)
    with c2.container(border=True):
        st.subheader('Industria')
        plot_ipi(actividad,var_men_act,var_an_act)
    with c3.container(border=True):
        st.subheader('Construcción')
        plot_isac(actividad,var_men_act,var_an_act)
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.subheader('PBI Real')
        plot_PBI(pbi,var_pbi)
    with c2.container(border=True):
        st.subheader('PBI per cápita')   
        plot_percap(pbi,var_pbi)
    st.divider()
    st.caption('Datos Desestacionalizados excepto para el PBI Per Cápita')