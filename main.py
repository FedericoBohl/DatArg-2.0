from librerias import *
from Paginas.__BCRA__ import make_BCRA_web
from Paginas.__SectorExterno__ import make_sect_ext_web
from Paginas.__SectorPublico__ import make_sect_pub_web
from Paginas.__SectorInternacional__ import make_internacional_web
from Paginas.__SectorFinanciero__ import make_merv_web
from Paginas.__Actividad__ import make_actividad_web
from Paginas.__Pobreza__ import make_pobreza_web
from Paginas.__Precios__ import make_precios_web



st.set_page_config(
    page_title="DatArg",
    page_icon="🧉",
    layout="wide",
    initial_sidebar_state="expanded")

#@st.cache_resource(show_spinner=False)

st.markdown('''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>''', unsafe_allow_html=True)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css('styles.css')

try:
    S.page_width,S.is_session_pc=page_info()
except:
    S.page_width=2000
    S.is_session_pc=True
if S.is_session_pc:  #Fix momentaneo
    try:
        components.html(w_barra_stocks,height=80)
    except:pass
    col1,col2=st.columns((0.1,0.9))
    with col1:st.image("Icono.jpeg",caption="🐐")
    with col2:

        #x=f"""<div data-stale="false" width="{page_width}"""+"""class="element-container st-emotion-cache-u4g42f e1f1d6gn4" data-testid="element-container"><div class="stHeadingContainer" data-testid="stHeading"><div class="stMarkdown" style="width: 524.8px;"><div data-testid="stMarkdownContainer" class="st-emotion-cache-w3enc8 e1nzilvr5" style="width: 524.8px;"><div class="st-emotion-cache-1629p8f e1nzilvr2"><h2 id="61901152"><div data-testid="StyledLinkIconContainer" class="st-emotion-cache-zt5igj e1nzilvr4"><a href="#61901152" class="st-emotion-cache-p2doo6 e1nzilvr3"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a><span class="st-emotion-cache-10trblm e1nzilvr1"><span style='text-align: center; color: #6CACE4; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Datos Argentina 🧉</span></span></div></h2></div></div></div><hr data-testid="stHeadingDivider" color="#FFB81C" class="st-emotion-cache-h8phe6 e1nzilvr0"></div></div>"""
        #st.markdown(x,unsafe_allow_html=True)
        #st.markdown("""<h2 style='text-align: center; color: #6CACE4; font-family: "Source Serif Pro", serif; font-weight: 600; letter-spacing: -0.005em; padding: 1rem 0px; margin: 0px; line-height: 1.2;'>Datos Argentina 🧉</h2>""", unsafe_allow_html=True)
        #st.markdown("""<hr data-testid="stHeadingDivider" color="#3d9df3" class="st-emotion-cache-h8phe6 e1nzilvr0">""",unsafe_allow_html=True)
        #st.markdown("""<hr data-testid="stHeadingDivider" color="#6cace4" class="st-emotion-cache-h8phe6 e1nzilvr0">""", unsafe_allow_html=True)
        st.header('Datos Argentina 🧉',divider='blue')
        #st.caption(" ")
        with st.popover("Calendario Económico",use_container_width=True,help="Los datos muy recientes pueden tardar unos pocos dias en ser agregados a las series oficiales. Aquí puede ver los últimos datos anunciados y las fechas de proximos anuncios."):
            #c1,c2=st.columns(2)
            #with c1:
            #    components.html(w_calendar_investing, height=350,width=int(page_width*0.9*0.45))
            #with c2:
            create_widget(w_calendar_tv,height=350,width=int(S.page_width*0.85))
    
    st.write(st.context.cookies)
    
    t_info, t_actividad, t_PI, t_precios, t_bcra, t_SecExt, t_SecPub, t_Intl, t_Merv= st.tabs(["Info","Actividad","Pobreza y Empleo", "Precios", "BCRA", "Sector Externo","Sector Público","Internacional","Bolsa Argentina"])

    S.pbi_men=get_pbi()

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



