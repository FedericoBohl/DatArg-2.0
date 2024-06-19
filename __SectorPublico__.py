from librerias import *

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
    cols['Gastos Corrientes','Remuneraciones','Bienes y Servicios','Otros Gastos de Consumo',"Gasto Seguridad Social",
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
    #load new data
    try:
        # URL del endpoint de la API
        url = "https://www.presupuestoabierto.gob.ar/api/v1/credito?format=csv"

        # Cabeceras de la solicitud
        headers = {
            'Authorization': 'ee7f6d62-90ad-4a31-8db0-844acf12ee27',  # Reemplaza con tu token
            'Content-Type': 'application/json'
        }

        # Datos de la solicitud
        data = {
            "title": "Credito vigente por jurisdiccion",
            "columns": [
                "impacto_presupuestario_mes",
                "jurisdiccion_desc",
                "finalidad_desc",
                "fuente_financiamiento_desc",
                "ubicacion_geografica_desc",
                "credito_vigente"
            ]
        }

        # Realizar la solicitud POST a la API
        response = requests.post(url, headers=headers, data=json.dumps(data))


        with open('presupuestos.csv', 'w', encoding='utf-8') as file:
            file.write(response.text)
    except: pass
    provincias={'Ciudad Autónoma de Buenos Aires':'Capital Federal',
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
    'Provincia de Tierra del Fuego, Antártida e Islas del Atlántico Sur':'Tierra del Fuego',
    'Provincia de Tucumán':'Tucumán',
    'Provincia del Chaco':'Chaco',
    'Provincia del Chubut':'Chubut',
    'Provincia del Neuquén':'Neuquén'}
    df=pd.read_csv('presupuestos.csv',encoding='utf-8')

    df1=df.groupby(by=['ubicacion_geografica_desc']).sum()#.reset_index()
    df1['%']=100*df1['credito_vigente']/df1['credito_vigente'].sum()
    extras=df1.iloc[0:4]
    df1=df1.drop(index=['Binacional','No Clasificado','Interprovincial','Nacional'],)
    df1=df1.reset_index()
    df1['ubicacion_geografica_desc'] = df1['ubicacion_geografica_desc'].replace(provincias)


    geo=json.load(open('ProvinciasArgentina.geojson', encoding='utf-8'))
    provincias_geo_df = pd.json_normalize(geo['features'])
    #provincias_geo_df['properties.nombre'] = 'Provincia de ' + provincias_geo_df['properties.nombre']

    merged_df = provincias_geo_df.merge(df1, left_on='properties.nombre', right_on='ubicacion_geografica_desc')
    return merged_df, geo, extras

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
    t1.plotly_chart(fig,use_container_width=True)

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
    t2.plotly_chart(fig,use_container_width=True)

@st.cache_data(show_spinner=False)
def make_map(data,geo,extras):
    fig = px.choropleth_mapbox(
        data,
        geojson=geo,
        locations='ubicacion_geografica_desc',
        featureidkey='properties.nombre',
        color='%', # Asegúrate de que esta columna contiene el gasto fiscal
        hover_name='properties.nombre',
        custom_data=['properties.nombre','credito_vigente','%'],
        color_continuous_scale='magma',
                            mapbox_style= "carto-positron" , # formatos de diseño del mapa : "carto-positron", "carto-positron",   "white-bg",
                            zoom=2.6, center = {"lat": -38.40, "lon": -63.60},
                            opacity=1,
                            labels={'promedio acessos por cada 100 hogares':'acceso a internet'},
                            color_discrete_sequence=["blue"],
                            )
    fig.update_traces(
        marker_line_width=1.5,
        marker_line_color='black',
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",  # Asegúrate de cerrar la etiqueta <b> correctamente aquí
            "Presupuesto Brindado: %{customdata[1]}",
            "Proporción en relación al presupuesto total: %{customdata[2]:.2f}%"
        ])
    )
    # Actualizar el layout del mapa
    #fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
        mapbox=dict(
            center={"lat": -38.4161, "lon": -63.6167},
            style="white-bg",
            zoom=2.65,
            layers=[
                dict(
                    below='traces',
                    type='fill',
                    source=geo,
                    color="lightblue"
                )
            ]
        ),
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        geo=dict(
            showland=False,  # No mostrar etiquetas de países
            showcountries=False,  # No mostrar bordes de países
        )
    )

    st.plotly_chart(fig,use_container_width=True)

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
            t1.plotly_chart(fig,use_container_width=True)
            
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
            t2.plotly_chart(fig,use_container_width=True)

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
            t3.plotly_chart(fig,use_container_width=True)


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
            t1.plotly_chart(fig,use_container_width=True)

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
    st.plotly_chart(fig,use_container_width=True)


    st.caption('Los datos corresponden al endeudamiento en cada moneda neto de lo amortizado en el mes en cuestión. Se ignora el incremento de otros pasivos.')

@st.cache_data(show_spinner=False)
def plot_ingresos_gastos(data,escala):
    t1,t2=st.tabs(['Ingresos','Gastos'])
    st.caption('Los datos son el resultado anual acumulado de cada mes.')

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['Ingresos Corrientes'],name='Total',line=dict(width=4)))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos Tributarios'],name='Ingresos Tributarios'))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos Seguridad Social'],name='Aport. a la Seg. Social'))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos No Tributarios'],name='Ingresos No Tributarios'))
    fig.add_trace(go.Bar(x=data.index,y=data['Ingresos Transferencias Corrientes'],name='Trans. Corrientes'))
    fig.add_trace(go.Bar(x=data.index,y=data['Otros Ingresos'],name='Otros'))
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
    t1.plotly_chart(fig,use_container_width=True)


def make_sect_pub():
    deficit,datagdp,datatco,endeudamiento,endeudamientogdp,endeudamientotco=load_data_sectpub(datetime.now().strftime("%Y%m%d"))
    c1,c2=st.columns((0.8,0.2))
    with c1:
        with st.container(border=True):
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

    if S.escala_sectpub=="***Millones de ARS***":
        S.data_sectpub=deficit
        S.endeudamiento=endeudamiento
    elif S.escala_sectpub=="***Millones de USD-Oficial***":
        S.data_sectpub=datatco
        S.endeudamiento=endeudamientotco
    else:
        S.data_sectpub=datagdp
        S.endeudamiento=endeudamientogdp
    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader('Resultado Fiscal y Financiero')
            plot_deficit(S.escala_sectpub,S.data_sectpub)
    with c2:
        with st.container(border=True):
            st.subheader('Gastos/Ingresos Corrientes')
    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader('Deuda Pública')
            deuda,deuda_mon=load_datos_deuda(2)
            st.radio('Deuda Pública',options=['Endeudamiento Anual Acumulado','Composición de la Deuda Bruta','Pagos de Deuda por Moneda'],label_visibility='collapsed',horizontal=False,key='plot_deuda')
            plot_deuda(deuda,S.plot_deuda) if S.plot_deuda=='Composición de la Deuda Bruta' else (plot_deuda(deuda_mon,S.plot_deuda) if S.plot_deuda=='Pagos de Deuda por Moneda' else plot_endeudamiento(S.endeudamiento,S.escala_sectpub))
    with c2:
        with st.container(border=True):
            st.subheader('Déficit Provincial')
            data,geo,extras=load_data_map(datetime.now().strftime("%Y%m%d"))
            make_map(data,geo,extras)