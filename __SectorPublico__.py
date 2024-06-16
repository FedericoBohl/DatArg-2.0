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
def make_map(data,geo):
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
    with c2:
        with st.container():
            st.subheader('Mapa Fiscal Argentino')
            make_map(load_data_map(datetime.now().strftime("%Y%m%d")))