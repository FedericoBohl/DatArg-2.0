from librerias import *
from plots_bcra import *
#from get_data import *





#___________________________CARGA DE DATOS____________________________________________________________
@st.cache_resource(show_spinner=False)
def load_bcra_his(date): 
    ## Agregados Monetarios
    bcra=pd.read_csv("His Data/his-agregados.csv",delimiter=";")
    bcra['Unnamed: 0'] = pd.to_datetime(bcra.iloc[:, 0].values, format='%Y-%m-%d')
    bcra.set_index('Unnamed: 0', inplace=True)
    ids=["300.1_AP_ACT_TITPUB_0_M_14",
        "300.1_AP_ACT_ADENAC_0_M_37",
        "90.1_BMT_0_0_20",
        "90.1_BMCMT_0_0_42",
        "90.1_BMCMP_0_0_44",
        "90.1_BMCMEF_0_0_52",
        "90.1_BMCCB_0_0_36",
        "90.1_DTPPUB_0_0_31",
        "90.1_DCCPUB_0_0_34",
        "90.1_AMTM2_0_0_31",
        "90.1_AMTM3_0_0_31",
        "92.1_PMLD_0_0_27_100",
        "92.1_PNP_0_0_19",
        "331.1_TOTAL_VARIION__27",
        "331.1_COMPRAS_NETAL__45",
        "331.1_OTRAS_OPERTAL__56",
        "331.1_PASES_REDETAL__24",
        "331.1_TITULOS_DECRA__20",
        "331.1_RESCATE_CUDAS__5"
        ]
    cols=["Tit Publicos","Adeltantos Transitorios","BM","Circulante","CPP","CB","R","Depositos","Cta Corriente","M2","M3","LeLiq","Pases Netos","Var. BM","Neto compra divisas","Oper con el Tesoro","Pases y Redescuentos","LEBAC-NOBAC","Rescate de Cuasimonedas"]
    data=get_data(ids,start_date="2024-01-01",col_list=cols)
    data["Cuasimonedas"]=None
    data["M1"]=data["Circulante"]+data["Cta Corriente"]
    data["Cta Ahorro"]=data["M2"]-data["M1"]
    data["Deposito plazo"]=data["M3"]-data["M2"]
    data["Lebac"]=None
    data["Tit Publicos"]=data["Tit Publicos"]/1000
    data["Adeltantos Transitorios"]=data["Adeltantos Transitorios"]/1000
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
    data.reindex(columns=bcra.columns)
    data=pd.concat([bcra,data],axis=0)
    datagdp=data.copy()
    datagdp=add_gdp(datagdp)
    for col in data.columns.to_list():
        datagdp[col]=datagdp[col]*100/(datagdp["PBI"]*4)

    ## Reservas
    his_data=pd.read_csv('His Data/his-reservas.csv',delimiter=';')
    his_data['Unnamed: 0'] = pd.to_datetime(his_data.iloc[:, 0].values, format='%Y-%m-%d')
    his_data.set_index('Unnamed: 0', inplace=True)
    ids=['92.1_RID_0_0_32','92.1_TCV_0_0_21','145.3_INGNACNAL_DICI_M_15']
    cols=["Res Int",'TC','IPC']
    cur_data=get_data(ids,start_date="2024-01-01",col_list=cols)
    _ = fred.get_series('CPIAUCNS').loc[f'{2024}':]
    cur_data=pd.concat([cur_data,_],axis=1)
    cur_data=cur_data.rename(columns={0:'IPC*'})
    cur_data['TCR']=cur_data['TC']*cur_data['IPC*']/cur_data['IPC']
    cur_data=cur_data.reindex(columns=his_data.columns)
    reservas=pd.concat([his_data,cur_data],axis=0)

    datatco=data.copy()
    TCR=reservas.loc["2004":f"{data.index.values[len(data)-1]}","TCR"]
    TC=reservas.loc["2004":f"{data.index.values[len(data)-1]}","TC"]
    datatco['TC']=TC
    for col in data.columns.to_list():
        datatco[col]=datatco[col]/datatco["TC"]

    ## Tasas de interés
    his_data=pd.read_csv('His Data/his-tasas.csv',delimiter=';')
    his_data['Unnamed: 0'] = pd.to_datetime(his_data.iloc[:, 0].values, format='%Y-%m-%d')
    his_data.set_index('Unnamed: 0', inplace=True)
    ids=['89.1_TIB_0_0_20','89.1_IR_BCRADIA_0_M_36','89.1_IR_BCRARIA_0_M_34']
    cols=["Badlar","Tasa Pases Pasivos (1 dia)","Tasa de Politica Monetaria"]
    cur_data=get_data(ids,start_date="2024-01-01",col_list=cols)
    cur_data=cur_data.reindex(columns=his_data.columns)
    tasas=pd.concat([his_data,cur_data],axis=0)

    return reservas, data, datagdp, datatco, tasas,TCR,TC


#@st.cache_data(show_spinner=False,experimental_allow_widgets=True)
def make_BCRA_web():
    reservas,bcra,bcragdp,datatco,tasas,S.TCR,S.TC=load_bcra_his(datetime.now().strftime("%Y%m%d"))
    c1,c2=st.columns((0.7,0.3),vertical_alignment='center')
    with c1:
        with st.expander(label='Ajustar Gráficas',icon=":material/settings:"):
            c11,c12=st.columns((0.3,0.7))
            with c11: st.radio("Escala de los datos",options=["***Millones de ARS***","***Millones de USD-Oficial***","***Millones de USD-Blue***","***% del PBI***"],key="escala_bcra")
            with c12: st.number_input(value=2016,label='Datos desde',min_value=2004,max_value=2024,key="start_bcra")
    with c2:
        st.link_button(":blue[**Descargar datos:\nBCRA**]",url="https://1drv.ms/x/c/56f917c917f2e2f5/EfXi8hfJF_kggFZ9FQAAAAABTxlMFKgDUN6_w9BtQ4q1xA?e=PeQb0M",use_container_width=True)
    bcra=bcra.loc[f"{S.start_bcra}":]
    bcra.index=bcra.index.strftime('%b-%Y')
    bcragdp=bcragdp.loc[f"{S.start_bcra}":]
    tasas=tasas.loc[f"{S.start_bcra}":]
    tasas.index=tasas.index.strftime('%b-%Y')
    bcragdp.index=bcragdp.index.strftime('%b-%Y')
    datatco=datatco.loc[f"{S.start_bcra}":]
    datatco.index=datatco.index.strftime('%b-%Y')
    if S.escala_bcra=="***Millones de ARS***":
        S.data_bcra=bcra
    elif S.escala_bcra=="***Millones de USD-Oficial***":
        S.data_bcra=datatco
    else:
        S.data_bcra=bcragdp

    c1,c2=st.columns(2)
    with c1:
        #with st.container(border=True,height=143):
        #    st.subheader("Datos Spot a Agregar")
        with st.container(border=True):
            plot_agregados(S.escala_bcra,S.data_bcra,tasas)
        with st.container(border=True):
            plot_BM(S.escala_bcra,S.data_bcra)
        st.text(" ")
        with st.container(border=True):
            plot_reservas(reservas)
    with c2:
        with st.container(border=True):
            plot_pasivos_rem(S.escala_bcra,S.data_bcra,tasas)
        with st.container(border=True):
            plot_fin_mon(S.escala_bcra,S.data_bcra)
        with st.container(border=True):
            plot_depositos(S.escala_bcra,S.data_bcra,tasas)
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center;'>Factores de variación de la Base Monetaria</h3>", unsafe_allow_html=True)
        st.number_input("¿Suma Móvil de cuantos meses?",min_value=1,max_value=24,value=12,key="roll_bcra_bm")
        plot_varBM(S.escala_bcra,S.data_bcra,S.roll_bcra_bm)
