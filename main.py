from _globals_ import w_barra_stocks
import streamlit as st
from streamlit import session_state as S
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
import pytz
import requests
import time
from streamlit_lottie import st_lottie_spinner
from st_social_media_links import SocialMediaIcons
from Paginas.__BCRA__ import make_BCRA_web,load_bcra
from Paginas.__SectorExterno__ import make_sect_ext_web,load_sect_ext
from Paginas.__SectorPublico__ import make_sect_pub_web,load_data_map,load_data_sectpub,load_datos_deuda
from Paginas.__SectorInternacional__ import make_internacional_web
from Paginas.__SectorFinanciero__ import make_merv_web
from Paginas.__Actividad__ import make_actividad_web,load_actividad
from Paginas.__Pobreza__ import make_pobreza_web,load_pobreza
from Paginas.__Precios__ import make_precios_web,load_precios
from Paginas.librerias import get_pbi
from Calendar.calendar import create_calendar
import csv
import base64

st.set_page_config(
    page_title="DatArg",
    page_icon="🧉",
    layout="wide",
    initial_sidebar_state="collapsed")

#st.switch_page('pages/login_animation.py')

#***************************************    ARMADO DE LA PÁGINA     ****************************************************************

#@st.cache_resource(show_spinner=False)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css('styles.css')
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.cache_resource(show_spinner=False)
def make_info():
    st.header("¿Quienes somos?")
    st.caption(":blue[:blue-background[DatArg]] es una aplicación sin fines de lucro que busca promover la transparencia de los datos económicos oficiales mediante un entorno que presente en **tiempo real** las principales variables de los distintos sectores económicos que involucran la coyuntura económica de un país, permitiendo su analisis y fácil comprensión, **todo en un solo lugar**. Su uso es tan extenso que preferimos que lo compruebes por vos mismo/a: analistas, consultores, profesores, periodistas y mucho más.")
    st.caption("Esta aplicación surge como una iniciativa para democratizar el acceso a datos económicos en tiempo real sobre Argentina. Nuestro objetivo es ofrecer una herramienta gratuita que permita a cualquier persona, sin importar su nivel de conocimientos en economía, acceder a información clara y transparente.La creación de esta plataforma responde a nuestra convicción de que el acceso a la información es un derecho fundamental. Al ofrecer esta aplicación de manera gratuita, buscamos contribuir al desarrollo de una sociedad más informada y, en última instancia, más justa.")
    st.caption("Somos un equipo pequeño, pero estamos comprometidos con la idea de que el conocimiento es poder, y el acceso al conocimiento debe ser universal. Esperamos que esta herramienta te sea útil y te invitamos a explorarla todo con libertad.")
    st.header("Nuestro Equipo")
    col1,col2=st.columns((1,1))
    with col1:
        with st.container(border=True):
            c1,c2=st.columns((0.2,0.8)) 
            with c1:st.image("fede.jpeg")
            with c2:
                st.subheader("Federico Bohl")
                st.write("**Rol:** Creador y desarrollador")
                social_media_links = [
                        "https://www.linkedin.com/in/federico-bohl/",
                        "https://x.com/BohlFede"
                        ]
                SocialMediaIcons(social_media_links).render(sidebar=False, justify_content="left")
    with col2:
        with st.container(border=True):
            c1,c2=st.columns((0.2,0.8)) 
            with c1:st.image("valen.jpeg")
            with c2:
                st.subheader("Valentín Vedda")
                st.write("**Rol:** Calendario económico y bot de Telegram")
                social_media_links = [
                        "https://www.linkedin.com/in/valentin-vedda-35024720a/",
                        "valenvedda@gmail.com"#"https://github.com/valenvedda"
                        ]
                SocialMediaIcons(social_media_links).render(sidebar=False, justify_content="left")

def load_ALL(today):
    S.pbi_men=get_pbi()
    S.actividad_,S.pbi_=load_actividad(today)
    S.precios,S.rem=load_precios(today)
    S.IPC=S.precios.loc['2004':,'IPC']
    S.reservas_,S.bcra_,S.bcragdp_,S.bcratco_,S.tasas_,S.TCR,S.TC=load_bcra(today)
    S.salarios,S.empleo,S.pobind=load_pobreza(today)
    S.bop_,S.bopgdp_,S.ica_,S.icagdp_,S.tot=load_sect_ext(today)
    S.deficit_,S.deficitgdp_,S.deficittco_,S.endeudamiento_,S.endeudamientogdp_,S.endeudamientotco_,S.corr_,S.corrgdp_,S.corrtco_=load_data_sectpub(today)
    S.deuda,S.deuda_mon=load_datos_deuda(today)
    S.data_map,S.geo_map,S.extras_map=load_data_map(today)

if not '__loaded__' in S:
    today=datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).strftime("%Y-%m-%d")
    cont=st.container(border=False,height=550)
    with cont:
        st.markdown("""<h1 style='text-align: center; color: #000000; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Cargando tu Economía...</h1>""", unsafe_allow_html=True)
        lottie_progress_url = "https://lottie.host/61385cf3-564b-41cb-a243-3ce5c25c4134/uIUPGURgQ9.json"
        lottie_progress = load_lottieurl(lottie_progress_url)
        with st_lottie_spinner(lottie_progress, loop=True, key="progress",height=490):
            load_ALL(today)
    del cont
    S.__loaded__=0
    st.rerun()

components.html(w_barra_stocks,height=80)
st.header('Datos Argentina 🧉')
c1,c2=st.columns((0.8,0.2))
with c1.popover("Calendario Económico",use_container_width=True,help="Los datos muy recientes pueden tardar unos pocos dias en ser agregados a las series oficiales. Aquí puede ver los últimos datos anunciados y las fechas de proximos anuncios."):
#with st.expander(label='Calendario económico',icon=":material/settings:"):
    #create_widget(w_calendar_tv,height=350,width=int(S.page_width*0.85))
    df = pd.read_csv('Calendar/calendar_events.csv')
    calendario=create_calendar(df)
with c2.popover('Bot de Telegram',use_container_width=True,help='Agradecimientos a Valentín Vedda por su gran aporte con este bot.'):
    st.caption('¿Queres enterarte cuando sale un nuevo dato? Subscribite al bot de Telegram para que te avisemos cuando salgan.')
    st.page_link(page='https://t.me/calendario_economico_argentino',label='Calendario Económico Argentino',icon='🗓️')



t_info, t_actividad, t_PI, t_precios, t_bcra, t_SecExt, t_SecPub, t_Intl, t_Merv= st.tabs(["Info","Actividad","Pobreza y Empleo", "Precios", "BCRA", "Sector Externo","Sector Público","Internacional","Mercado de Capitales"])

with t_info:
    make_info()
with t_actividad:
    make_actividad_web()
with t_PI:
    make_pobreza_web()
with t_precios:
    make_precios_web()
with t_bcra:
    make_BCRA_web()
with t_SecExt:
    make_sect_ext_web()
with t_SecPub:
    make_sect_pub_web()
with t_Intl:
    make_internacional_web()
with t_Merv:
    make_merv_web()

with st.container():
    image_path = "cafe.png"
    with open(image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode()

    # HTML para el botón
    html_code = f"""
    <div class="button-container">
        <a href="https://cafecito.app/datarg" target="_blank" style="text-decoration: none;">
            <button class="custom-button">
                <img src="data:image/jpeg;base64,{image_data}" alt="Café" />
                Invitame un cafecito
            </button>
        </a>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True) 
    if 0==1:    #Desactivado hasta que encuentre la manera de que la sugerencia sea recibida
        suggestion = st.text_input(
            label="Déjanos tus sugerencias o comentarios:", 
            placeholder="Escribe aquí tus sugerencias o comentarios...",
            label_visibility='collapsed'
        )
        if suggestion:
            with open('sugerencias.csv', mode='a',newline='',encoding='utf-8') as file:
                writer=csv.writer(file)
                writer.writerow([suggestion])
            st.toast('Muchas gracias por tu comentiario y por ayudarnos a mejorar la página!')
            st.rerun()