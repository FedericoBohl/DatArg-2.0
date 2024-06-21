from librerias import *
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

    return data.rolling(4).sum(),datagdp.dropna(),ica.rolling(4).sum(),icagdp.dropna() 

@st.cache_resource(show_spinner=False)
def plot_bop(data,escala,errores):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['CC'],name='CC',marker_color=maroon,line=dict(width=5)))
    fig.add_trace(go.Scatter(x=data.index,y=data['CK']+data['CF(MBP5)'],name='CF+CK',marker_color=navy,line=dict(width=5)))
    fig.add_trace(go.Bar(x=data.index,y=data['VarR'],name='Var. R',marker_color=data["VarR"].apply(lambda x: green if x >= 0 else red),
                                    showlegend=True, opacity=1, marker_line_color=black,
                                    marker_line_width=1))
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
    st.plotly_chart(fig,use_container_width=True)
def make_sect_ext_web():
    bop,bopgdp,ica,icagdp=load_sect_ext(datetime.now().strftime("%Y%m%d"))
    c1,c2=st.columns((0.8,0.2))
    with c1:
        with st.container(border=True):
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
        _=S.TCR.resample('Q').mean()
        st.write(_.iloc[8:]*100/69.82120981)
        
        st.caption('El Tipo de Cambio es re-escalado por conveniencia visual con base Enero 2004 = 100.')
    c1,c2=st.columns(2)
    with c1.container(border=True):
        st.subheader('Destino de las Expo/Importaciones')
        c11,c12=st.columns(2)
        c11.number_input('Año',2004,2023,step=1)
        c12.radio('Destino expo/impo',label_visibility='collapsed',options=['Valor (USD)','Porcentaje del Total'])
        ex,im=st.tabs(['Exportaciones','Importaciones'])
    with c2.container(border=True):
        st.subheader('Intercambio Comercial Argentino')
        ex,im=st.tabs(['Exportaciones','Importaciones'])
