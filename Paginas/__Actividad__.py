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
def plot_PBI(data:pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data['PBI Real'],name='PBI Real',line=dict(width=3.5),marker_color=navy),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=data['PBI Real'].pct_change(),name='Var %',marker_color='royalblue'),secondary_y=True)
    fig.update_layout(hovermode="x unified",margin=dict(l=1, r=1, t=75, b=1),barmode="stack",bargap=0,height=450,legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="right",
                                        x=1,
                                    bordercolor=black,
                                    borderwidth=2
                                ),
                                yaxis=dict(title='Millones de ARS del 2004',showgrid=True, zeroline=True, showline=True),
                                yaxis2=dict(title="%",showgrid=True, zeroline=True, showline=True)
                                )
    fig['layout']['yaxis']['type']='log'
    st.plotly_chart(fig,use_container_width=True)

@st.cache_resource(show_spinner=False)
def plot_percap(data:pd.DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index,y=data['PBI Per Cap'],name='PBI Per Cápita',line=dict(width=3.5),marker_color=olive),secondary_y=False)
    fig.add_trace(go.Bar(x=data.index,y=data['PBI Per Cap'].pct_change(),name='Var %',marker_color='lime'),secondary_y=True)
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
                                yaxis2=dict(title="%",showgrid=True, zeroline=True, showline=True)
                                )
    fig['layout']['yaxis']['type']='log'
    st.plotly_chart(fig,use_container_width=True)


def make_actividad_web():
    actividad,pbi=load_actividad(datetime.now().strftime("%Y%m%d"))
    c1,c2=st.columns((0.7,0.3))
    c1.number_input(value=2016,label='Datos desde',min_value=2004,max_value=2024,key="start_actividad")
    c2.link_button(":blue[**Descargar datos:\nActividad**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/QfXi8hfJF_kggFaKFQAAAAAA7qhKZI81Oq7vDg",use_container_width=True)
    actividad=actividad.loc[f"{S.start_actividad}":]
    actividad.index=actividad.index.strftime('%b-%Y')
    pbi=pbi.loc[f"{S.start_actividad}":]
    pbi.index=pbi.index.strftime('%b-%Y')

    c1,c2,c3=st.columns(3)
    with c1.container(border=False):
        st.header('EMAE')
    with c2.container(border=False):
        st.header('Industria')
    with c3.container(border=True):
        st.header('Construcción')
    c1,c2=st.columns(2)
    with c1.container(border=False):
        st.subheader('PBI Real')
        plot_PBI(pbi)
    with c2.container(border=False):
        st.subheader('PBI per cápita')   
        plot_percap(pbi)
    st.divider()
    st.caption('Datos Desestacionalizados excepto para el PBI Per Cápita')