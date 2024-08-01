from Paginas.__BCRA__ import load_bcra
from Paginas.__SectorExterno__ import load_sect_ext
from Paginas.__SectorPublico__ import load_data_map,load_data_sectpub,load_datos_deuda
from Paginas.__Actividad__ import load_actividad
from Paginas.librerias import get_pbi
from streamlit_lottie import st_lottie_spinner # type: ignore
import streamlit as st
from streamlit import session_state as S
from datetime import datetime
import requests


st.set_page_config(
    page_title="DatArg",
    page_icon="🧉",
    layout="centered",
    initial_sidebar_state="collapsed")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
#local_css('styles.css')

def load_ALL(today):
    S.pbi_men=get_pbi()
    S.actividad_,S.pbi_=load_actividad(today)
    S.reservas_,S.bcra_,S.bcragdp_,S.datatco_,S.tasas_,S.TCR,S.TC=load_bcra(today)
    S.bop_,S.bopgdp_,S.ica_,S.icagdp_,S.tot=load_sect_ext(today)
    S.deficit_,S.datagdp_,S.datatco_,S.endeudamiento_,S.endeudamientogdp_,S.endeudamientotco_,S.corr_,S.corrgdp_,S.corrtco_=load_data_sectpub(today)
    S.deuda,S.deuda_mon=load_datos_deuda(today)
    S.data_map,S.geo_map,S.extras_map=load_data_map(today)

today=datetime.now().strftime("%Y%m%d")

with st.container(border=False,height=550):
    lottie_progress_url = "https://lottie.host/61385cf3-564b-41cb-a243-3ce5c25c4134/uIUPGURgQ9.json"
    lottie_progress = load_lottieurl(lottie_progress_url)
    #with st_lottie_spinner(lottie_progress, loop=True, key="progress",height=490):
    load_ALL(today)
S.__loaded__=0
st.switch_page('main.py')