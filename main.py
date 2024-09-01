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
    col1,col2=st.columns((1,1))
    with col1:
        with st.container(height=500,border=False):
            st.header('¿Cómo utilizar la aplicación?')
            st.video("https://www.youtube.com/watch?v=hn2WqRX75DI")
            st.caption("Este video es puramente demostración, cuando se finalize la aplicación mostrara como esta se usa")
    with col2:
        st.header("Nuestro Equipo")
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
col1,col2=st.columns((0.1,0.9))
with col1:st.image("Icono.jpeg",caption="🐐")
with col2:
    #x=f"""<div data-stale="false" width="{page_width}"""+"""class="element-container st-emotion-cache-u4g42f e1f1d6gn4" data-testid="element-container"><div class="stHeadingContainer" data-testid="stHeading"><div class="stMarkdown" style="width: 524.8px;"><div data-testid="stMarkdownContainer" class="st-emotion-cache-w3enc8 e1nzilvr5" style="width: 524.8px;"><div class="st-emotion-cache-1629p8f e1nzilvr2"><h2 id="61901152"><div data-testid="StyledLinkIconContainer" class="st-emotion-cache-zt5igj e1nzilvr4"><a href="#61901152" class="st-emotion-cache-p2doo6 e1nzilvr3"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a><span class="st-emotion-cache-10trblm e1nzilvr1"><span style='text-align: center; color: #6CACE4; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Datos Argentina 🧉</span></span></div></h2></div></div></div><hr data-testid="stHeadingDivider" color="#FFB81C" class="st-emotion-cache-h8phe6 e1nzilvr0"></div></div>"""
    #st.markdown(x,unsafe_allow_html=True)
    #st.markdown("""<h2 style='text-align: center; color: #6CACE4; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Datos Argentina 🧉</h2>""", unsafe_allow_html=True)
    #st.markdown("""<hr data-testid="stHeadingDivider" color="#3d9df3" class="st-emotion-cache-h8phe6 e1nzilvr0">""",unsafe_allow_html=True)
    #st.markdown("""<hr data-testid="stHeadingDivider" color="#6cace4" class="st-emotion-cache-h8phe6 e1nzilvr0">""", unsafe_allow_html=True)
    st.header('Datos Argentina 🧉',divider='blue')
    c1,c2=st.columns((0.8,0.2))
    with c1.popover("Calendario Económico",use_container_width=True,help="Los datos muy recientes pueden tardar unos pocos dias en ser agregados a las series oficiales. Aquí puede ver los últimos datos anunciados y las fechas de proximos anuncios."):
    #with st.expander(label='Calendario económico',icon=":material/settings:"):
        #create_widget(w_calendar_tv,height=350,width=int(S.page_width*0.85))
        df = pd.read_csv('Calendar/calendar_events.csv')
        calendario=create_calendar(df)
    with c2.popover('Bot de Telegram',use_container_width=True,help='Agradecimientos a Valentín Vedda por su gran aporte con este bot.'):
        st.caption('¿Queres enterarte cuando sale un nuevo dato? Subscribite al bot de Telegram para que te avisemos cuando salgan.')
        st.page_link(page='https://t.me/calendario_economico_argentino',label='Calendario Económico Argentino',icon='🗓️')


t_info, t_actividad, t_PI, t_precios, t_bcra, t_SecExt, t_SecPub, t_Intl, t_Merv= st.tabs(["Info","Actividad","Pobreza y Empleo", "Precios", "BCRA", "Sector Externo","Sector Público","Internacional","Bolsa Argentina"])

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
    # Incrustar contenido en el container
    cafecito = '''
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <a href='https://cafecito.app/datarg' rel='noopener' target='_blank'>
            <img srcset='https://cdn.cafecito.app/imgs/buttons/button_6.png 1x, 
                            https://cdn.cafecito.app/imgs/buttons/button_6_2x.png 2x, 
                            https://cdn.cafecito.app/imgs/buttons/button_6_3.75x.png 3.75x' 
                    src='https://cdn.cafecito.app/imgs/buttons/button_6.png' 
                    alt='Invitame un café en cafecito.app' />
        </a>
    </div>
    '''
    st.markdown(cafecito, unsafe_allow_html=True)
    
    # Campo de texto para sugerencias
    suggestion = st.text_input(
        label="Déjanos tus sugerencias o comentarios:", 
        placeholder="Escribe aquí tus sugerencias o comentarios..."
    )
    
    # Lógica para manejar las sugerencias (opcional)
    if suggestion:
        st.write(f"Gracias por tus sugerencias: {suggestion}")