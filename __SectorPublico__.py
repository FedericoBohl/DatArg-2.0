from librerias import *

def load_sectpub():
    pass

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
            t1,t2,t3=st.tabs(['Gráfico','Títulos Públicos','Datos'])
            t3.dataframe(data)
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
            fig.add_trace(go.Bar(x=data.index,y=data['Titulos Publicos-Moneda Extranjera'],name='Moneda Extranjera',marker_color='#FDFFE2'))




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

def make_sect_pub():
    load_sectpub()
    c1,c2=st.columns((0.8,0.2))
    with c1:
        with st.container():
            st.caption('Aca poner déficit fiscal y financiero y para que el usuario elija el ratio sobre PBI, dólares y pesos')
    with c2:
        with st.container():
            st.caption('Link web')
    c1,c2=st.columns(2)
    with c1:
        with st.container():
            st.subheader('Resultado Fiscal')
    with c2:
        with st.container():
            st.subheader('Resultado Financiero')
    c1,c2=st.columns(2)
    with c1:
        with st.container():
            st.subheader('Deuda Pública')
            deuda,deuda_mon=load_datos_deuda(datetime.now().strftime("%Y%m%d"))
            st.radio('Deuda Pública',options=['Composición de la Deuda Bruta','Pagos de Deuda por Moneda'],horizontal=True,key='plot_deuda')
            plot_deuda(deuda,S.plot_deuda) if S.plot_deuda=='Composición de la Deuda Bruta' else plot_deuda(deuda_mon,S.plot_deuda)
    with c2:
        with st.container():
            st.subheader('Déficit Provincial')
            data,geo,extras=load_data_map(datetime.now().strftime("%Y%m%d"))
            make_map(data,geo,extras)