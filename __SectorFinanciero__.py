from GetBYMA import GetBYMA
from librerias import *

@st.cache_data(show_spinner=False)
def make_cedears(data_now : pd.DataFrame):
    with st.container(border=True):
        c1,c2,c3,c4,c5=st.columns(5)
        with c1:
            st.metric('SPY (ARS)',data_now.loc[data_now['symbol']=='SPY','last'].values[0],f"{data_now.loc[data_now['symbol']=='SPY','change'].values[0]*100:.2f}%")
        with c2:
            st.metric('NASDAQ (ARS)',data_now.loc[data_now['symbol']=='QQQ','last'].values[0],f"{data_now.loc[data_now['symbol']=='QQQ','change'].values[0]*100:.2f}%")
        with c3:
            st.metric('Down Jones (ARS)',data_now.loc[data_now['symbol']=='DIA','last'].values[0],f"{data_now.loc[data_now['symbol']=='DIA','change'].values[0]*100:.2f}%")
        with c4:
            st.metric('Dólar Oficial','-')
        with c5:
            st.metric('Dolar Blue/MEP/CCL','-')
    data=pd.read_csv('data_bolsa/bolsa_cedears.csv',delimiter=';')
    data=pd.merge(data_now,data,on='symbol').dropna()
    data['change']=data["change"]*100
    df_grouped = data.groupby(["Sector","symbol"])[["Weigths","change","Company","last"]].min().reset_index()
    fig = px.treemap(df_grouped, 
                    path=[px.Constant("CEDEARS"), 'Sector',  'symbol'],
                    values='Weigths',
                    hover_name="change",
                    custom_data=["Company",'last',"change"],
                    color='change', 
                    range_color =[-7,7],color_continuous_scale=colorscale,
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
    st.plotly_chart(fig,use_container_width=True)

@st.cache_data(show_spinner=False)
def make_acciones(data_now_merv : pd.DataFrame , data_now_gen : pd.DataFrame):
    data=pd.read_csv('data_bolsa/bolsa_arg.csv',delimiter=';')
    data_merv=pd.merge(data_now_merv,data,on='symbol').dropna()
    data_merv['change']=data_merv["change"]*100
    data_gen=pd.merge(data_now_gen,data,on='symbol').dropna()
    data_gen['change']=data_gen["change"]*100

    #-------------- Fig del Merval  --------------
    df_grouped = data_merv.groupby(["Sector","symbol"])[["CAP (MM)","change","Nombre","last"]].min().reset_index()
    fig_merv = px.treemap(df_grouped, 
                    path=[px.Constant("Bolsa Argentina"), 'Sector',  'symbol'], #Quite 'Industria', en 3
                    values='CAP (MM)',
                    hover_name="change",
                    custom_data=["Nombre",'last',"change"],
                    color='change', 
                    range_color =[-5,5],color_continuous_scale=colorscale,
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
    df_grouped = data_gen.groupby(["Sector","symbol"])[["CAP (MM)","change","Nombre","last"]].min().reset_index()
    fig_gen = px.treemap(df_grouped, 
                    path=[px.Constant("Bolsa Argentina"), 'Sector',  'symbol'], #Quite 'Industria', en 3
                    values='CAP (MM)',
                    hover_name="change",
                    custom_data=["Nombre",'last',"change"],
                    color='change', 
                    range_color =[-5,5],color_continuous_scale=colorscale,
                    labels={'Value': 'Number of Items'},
                    color_continuous_midpoint=0)
    fig_gen.update_traces(marker_line_width = 1.5,marker_line_color=black,
        hovertemplate="<br>".join([
        "<b>Empresa<b>: %{customdata[0]}",
        "<b>Precio (ARS)<b>: %{customdata[1]}"
        ])
        )
    fig_gen.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[2]}%"
    fig_gen.update_traces(marker=dict(cornerradius=10))
    fig_gen.update_layout(margin=dict(l=1, r=1, t=10, b=1))
    return fig_merv,fig_gen


def make_merv():
    df_indice,df_bonos_gob,df_letras,df_bonos_cor,df_merval,df_general,df_cedears, df_iamc=GetBYMA()
    st.metric('Merval',df_indice.loc[1,'last'],f'{round(df_indice.loc[1,"change"]*100,2)}%')
    bonos, acciones, cedears= st.tabs(["Bonos", "Acciones",'Cedears'])
    with bonos:
        st.header("Bonos")
        st.write(df_bonos_gob)
        st.header("Letras de corto plazo")
        st.write(df_letras)
        st.header("Bonos Corporativos")
        st.write(df_bonos_cor)
        st.header("IAMC??")
        st.write(df_iamc)
        st.divider()
        st.subheader("ejemplo de filtrado de bonos")
        st.write(df_iamc['Especie'].to_list())
    with acciones: 
        fig_merv,fig_gen=make_acciones(df_merval,df_general)
        container=st.container(border=True)
        if container.radio('¿Que panel desea ver?' , options=['Merval','Panel General'] , horizontal=True, index=0 , key='which_merv') == 'Merval':
            st.markdown("""<h2 style='text-align: center; color: #404040; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Merval</h2>""", unsafe_allow_html=True)
            st.plotly_chart(fig_merv, use_container_width=True)
        else:
            st.markdown("""<h2 style='text-align: center; color: #404040; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Panel General</h2>""", unsafe_allow_html=True)
            st.plotly_chart(fig_gen, use_container_width=True)
    with cedears:
        make_cedears(df_cedears)