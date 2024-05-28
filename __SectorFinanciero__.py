from GetBYMA import GetBYMA
from librerias import *

@st.cache_data(show_spinner=False, experimental_allow_widgets=True)
def make_cedears(data_now : pd.DataFrame):
    with st.container(border=True):
        c1,c2,c3,c4,c5=st.columns(5)
        with c1:
            st.metric('SPY (ARS)',data_now.loc[data_now['symbol']=='SPY','close'].values[0],f"{data_now.loc[data_now['symbol']=='SPY','change'].values[0]*100:.2f}%")
        with c2:
            st.metric('NASDAQ (ARS)',data_now.loc[data_now['symbol']=='QQQ','close'].values[0],f"{data_now.loc[data_now['symbol']=='QQQ','change'].values[0]*100:.2f}%")
        with c3:
            st.metric('Down Jones (ARS)',data_now.loc[data_now['symbol']=='DIA','close'].values[0],f"{data_now.loc[data_now['symbol']=='DIA','change'].values[0]*100:.2f}%")
        with c4:
            st.metric('Dólar Oficial','-')
        with c5:
            st.metric('Dolar Blue/MEP/CCL','-')
    data=pd.read_csv('data_bolsa/bolsa_cedears.csv',delimiter=';')
    data_now=data_now.drop_duplicates(subset='symbol', keep='first')
    data=pd.merge(data_now,data,on='symbol').dropna()
    data['change']=data["change"]*100
    df_grouped = data.groupby(["Sector","symbol"])[["Weigths","change","Company","close"]].min().reset_index()
    fig = px.treemap(df_grouped, 
                    path=[px.Constant("CEDEARS"), 'Sector',  'symbol'],
                    values='Weigths',
                    hover_name="change",
                    custom_data=["Company",'close',"change"],
                    color='change', 
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
    st.plotly_chart(fig,use_container_width=True)
    data.set_index('symbol', inplace=True)
    data=data.drop(columns=['Name','Weigths'])
    c1,c2= st.columns((0.6,0.4))
    with c1:
        st.subheader('Listado de CEDEARS')
        st.dataframe(data)
    with c2:
        st.subheader('Buscador de Cedears')
        st.selectbox('Buscador de cedears',label_visibility='collapsed',options=data.index.to_list(),key='cedebuscado')
        st.dataframe(data.loc[data.index==S.cedebuscado].transpose())



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


def make_merv():
    st.header('Mercado de Capitales')
    st.button('🔄️Recargar Datos',key='Reload')
    if (not 'df_indice' in S) or S.Reload:
        S.df_indice,S.df_bonos_gob,S.df_letras,S.df_bonos_cor,S.df_merval,S.df_general,S.df_cedears, S.df_iamc=GetBYMA()
    st.metric('Merval',S.df_indice.loc[1,'last'],f'{round(S.df_indice.loc[1,"change"]*100,2)}%')
    bonos, acciones, cedears= st.tabs(["Bonos", "Acciones",'Cedears'])
    with bonos:
        c1_1,c2_1,c3_1=st.columns(3)
        #Los dataframes deberían tener de index el ticker del bono para hacer el filtrado más simple
        with c1_1:
            if S.df_bonos_gob is not None:
                st.subheader('Bonos Ley Nacional')
                t_1_nac,t_2_nac,t_3_nac=st.tabs(['Panel','Curva','Buscador'])
                with t_1_nac: st.subheader('Panel')
                with t_2_nac: st.subheader('Curva')
                with t_3_nac: st.dataframe(S.df_bonos_gob[['last','change','volume','expiration']])#Filtrar por rango
            else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        with c2_1:
            if S.df_bonos_gob is not None:
                st.subheader('Bonos Ley Extrangera')
                t_1_ex,t_2_ex,t_3_ex=st.tabs(['Panel','Curva','Buscador'])
                with t_1_ex: st.subheader('Panel')
                with t_2_ex: st.subheader('Curva')
                with t_3_ex: st.dataframe(S.df_bonos_gob[['last','change','volume','expiration']])#Idem
            else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        with c3_1:
            if S.df_bonos_gob is not None:
                st.subheader('Bonos ajustados por CER')
                t_1_c,t_2_c,t_3_c=st.tabs(['Panel','Curva','Buscador'])
                with t_1_c: st.subheader('Panel')
                with t_2_c: st.subheader('Curva')
                with t_3_c: st.dataframe(S.df_bonos_gob[['last','change','volume','expiration']])#Idem
            else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        c1_2,c2_2=st.columns(2)
        with c1_2:
            if S.df_letras is not None:
                st.subheader('Letras')
                t_1_l,t_2_l,t_3_l=st.tabs(['Panel','Curva','Buscador'])
                with t_1_l: st.subheader('Panel')
                with t_2_l: st.subheader('Curva')
                with t_3_l: st.dataframe(S.df_letras[['last','change','volume','expiration']])
            else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        with c2_2:    
            if S.df_bonos_cor.all() is not None:
                st.subheader('Bonos Corporativos')
                t_1_cor,t_2_cor,t_3_cor=st.tabs(['Panel','Curva','Buscador'])
                with t_1_cor: st.subheader('Panel')
                with t_2_cor: st.subheader('Curva')
                with t_3_cor: st.dataframe(S.df_bonos_cor[['last','change','volume','expiration']])
            else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        if S.df_iamc is not None:
            c1_3,c2_3=st.columns((0.7,0.3))
            with c1_3:
                st.subheader('Información de los bonos')
                st.dataframe(S.df_iamc)
            with c2_3:
                st.subheader('Filtado de bono')
                st.selectbox('Buscador de Bonos',options=S.df_iamc.index.to_list(),key='bonobuscado')
                st.write(S.df_iamc.loc[S.df_iamc.index==S.bonobuscado].transpose())
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
        st.divider()
        #TEST
        try:
            _=pd.merge(S.df_bonos_gob[['last','change','volume','expiration']],S.df_iamc[['Duración Modificada','Tir Anual']], left_index=True,right_index=True)
            st.dataframe(_)
        except:pass
    with acciones:
        if (S.df_merval is not None):# and (S.df_general is not None):
            fig_merv,fig_gen=make_acciones(S.df_merval,S.df_general)
            container=st.container(border=True)
            if container.radio('¿Que panel desea ver?' , options=['Merval','Panel General'] , horizontal=True, index=0 , key='which_merv') == 'Merval':
                st.markdown("""<h2 style='text-align: center; color: #404040; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Merval</h2>""", unsafe_allow_html=True)
                st.plotly_chart(fig_merv, use_container_width=True)
            else:
                st.markdown("""<h2 style='text-align: center; color: #404040; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Panel General</h2>""", unsafe_allow_html=True)
                #st.plotly_chart(fig_gen, use_container_width=True)
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
    with cedears:
        if S.df_cedears is not None:
            make_cedears(S.df_cedears)
        else: st.exception(Exception('Error en la carga de datos desde ByMA. Disculpe las molestias, estamos trabajando para solucionarlo.'))
