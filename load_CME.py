from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
# Navega al sitio web
url='https://www.presupuestoabierto.gob.ar/sici/destacado-donde-se-gasta#'
try:
    driver.get(url)
    time.sleep(5)
    table_tab=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "tab-tabla"))
    )
    #table_tab=driver.find_element(By.ID, "tab-tabla")
    table_tab.click()
    # Esperar a que aparezca el span con la clase 'page-list'
    page_list_span = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "page-list"))
    )

    # Dentro del span, encontrar el botón con la clase 'dropdown-toggle' y hacer clic
    dropdown_button = page_list_span.find_element(By.CLASS_NAME, "dropdown-toggle")
    dropdown_button.click()
    time.sleep(1)
    # Esperar a que el menú desplegable esté visible y seleccionar la opción '50'
    #dropdown_menu = WebDriverWait(driver, 10).until(
    #    EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu"))
    #)

    # Encontrar la opción '50' dentro del menú desplegable y hacer clic en ella
    option_50 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//li/a[text()='50']"))
    )
    option_50.click()
    html = driver.page_source
finally:
    # Cerrar el driver
    driver.quit()

# Parsear el contenido HTML con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')


# Buscar la tabla por su ID
tabla = soup.find('table', {'id': 'tabla-programa'})

# Inicializar una lista para almacenar los datos
datos = []

# Verificar si existe tbody, si no, buscar directamente en la tabla
if tabla.find('tbody'):
    filas = tabla.find('tbody').find_all('tr')
else:
    filas = tabla.find_all('tr')

# Recorrer todas las filas
for fila in filas:
    # Extraer todas las celdas de la fila
    celdas = fila.find_all('td')
    # Extraer el texto de cada celda y almacenarlo en una lista
    fila_datos = [celda.text.strip() for celda in celdas]
    # Añadir la fila de datos a la lista principal
    datos.append(fila_datos)

# Crear un DataFrame con los datos extraídos
columnas = ['Ejercicio', 'Ubicación Geográfica', 'Presupuestado', 'Ejecutado', '% Ejecutado']
df = pd.DataFrame(datos, columns=columnas)
df['Presupuestado']=[float(i.replace('.','').replace(',','.')) for i in df['Presupuestado']]
df['Ejecutado']=[float(i.replace('.','').replace(',','.')) for i in df['Ejecutado']]
df['% Ejecutado']=[float(i.replace('.','').replace(',','.')) for i in df['% Ejecutado']]
# Mostrar el DataFrame
df.to_csv("donde-se-gasta.csv")

#############################################################################
def load_iol(tipo_,url):
    url=datasets[k]
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    divs = soup.find_all("tr", {"data-cantidad": "1"})
    ticker=[div.find('a').find("b").text.strip() for div in divs]
    val=[float(div.find_all('td')[1].text.strip().replace('.','').replace(',','.')) for div in divs]
    var=[float(div.find('span',{"data-field": "Variacion"}).text.replace('.','').replace(',','.')) for div in divs]
    tipo=[tipo_ for div in divs]
    return pd.DataFrame({'Ticker':ticker,'Precio':val,'Var':var,'Tipo':tipo})
def get_ecovalores():
    url='https://bonos.ecovalores.com.ar/eco/listado.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup=BeautifulSoup(response.text,'html.parser')
    tables=soup.find_all('table')
    data=None
    for i in range(len(tables)):
        try:
            table=tables[i]
            headers = table.find_all('th')
            header_texts = [header.get_text(strip=True) for header in headers]
            if 'TIR' in header_texts:
                data=[[td.text for td in tr.find_all('td')] for tr in table.find_all('tr')]
                data=pd.DataFrame(data,columns=header_texts).dropna()
                data.set_index('Título',inplace=True)
                data['TIR']=[float(i.replace('.','').replace('%','').replace(',','.')) for i in data['TIR']]
                data['Duration']=[float(i.replace(',','.')) for i in data['Duration']]
                data['Var %']=[float(i.replace('+','').replace(',','').replace('%','')) for i in data['Var %']]#[float(i.replace('.','').replace('%','').replace(',','.').replace('+','')) for i in data['Var %']]
                data['Int. Corrido']=[float(i.replace('.','').replace(',','.')) for i in data['Int. Corrido']]
                data['VT']=[float(i.replace('.','').replace(',','.')) for i in data['VT']]
                data['Precio']=[float(i.replace('.','').replace(',','.')) for i in data['Precio']]
                data['Vencimiento']=pd.to_datetime(data['Vencimiento'],format='%d/%m/%Y')
                data['Próx. Vto.']=pd.to_datetime(data['Próx. Vto.'],format='%d/%m/%Y')
                data.rename(columns={'VT':'Valor Técnico'},inplace=True)
                break
        except:continue
    return data[['Nombre','Precio','Var %','Valor Técnico','Int. Corrido','TIR','Duration','Paridad','Vol %','Próx. Vto.','Vencimiento','Tipo']]

datasets={
        'Bonos':'https://iol.invertironline.com/mercado/cotizaciones/argentina/bonos/todos',
        'Letras':'https://iol.invertironline.com/mercado/cotizaciones/argentina/letras/todas',
        #'Obligaciones Negociables':'https://iol.invertironline.com/mercado/cotizaciones/argentina/obligaciones-negociables/todos'
        }
data=pd.DataFrame(columns=['Ticker','Precio','Var','Tipo'])
for k in datasets:
    data=pd.concat([data,load_iol(k,datasets[k])],ignore_index=True)
data.set_index('Ticker',inplace=True)

ecovalores=get_ecovalores()
for i in ecovalores.index:
    if i in data.index.values:
        ecovalores.at[i,'Precio']=data.at[i,'Precio']
        ecovalores.at[i,'Var %']=data.at[i,'Var']

tipo2=[]
for i in data.index:
    try:
        t=ecovalores.loc[i]['Tipo']
    except:
        if i=='BPOD7':
            t='BOPREAL'
        else:
            t=None
    tipo2.append(t)
data['Tipo-2']=tipo2

driver=webdriver.Chrome()

nombre_=[]
descripcion_=[]
ley_=[]
isin_=[]
moneda_=[]
amortizacion_=[]
intereses_=[]
residual_=[]

for ticker in data.index:
    try:
        driver.get(f'https://www.cohen.com.ar/Bursatil/Especie/{ticker}/MERVAL/24hs.')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(("id", "tablaDatosPerfil")))
        #time.sleep(5)
        df=[[td.text for td in tr.find_elements(By.TAG_NAME,'td')] for tr in driver.find_element("id", "tablaDatosPerfil").find_elements(By.TAG_NAME,'tr')[1:]]
        df=pd.DataFrame(df,columns=['Dato','Val']).set_index('Dato')
        #print(df)
        nombre=df.loc['Denominación']['Val'] if 'Denominación' in df.index else ''
        descripcion=df.loc['Descripción']['Val'] if 'Descripción' in df.index else ''
        ley=df.loc['Ley']['Val'] if 'Ley' in df.index else ''
        isin=df.loc['Código ISIN']['Val'] if 'Código ISIN' in df.index else ''
        moneda=df.loc['Moneda de Emisión']['Val'] if 'Moneda de Emisión' in df.index else ''
        amortizacion=df.loc['Forma Amortización']['Val'] if 'Forma Amortización' in df.index else ''
        intereses=df.loc['Interés']['Val'] if 'Interés' in df.index else ''
        residual=float(df.loc['Monto Residual']['Val'].replace('.','').replace(',','.')) if 'Monto Residual' in df.index else 0
        if residual ==0:
            residual=float(df.loc['Monto de Emisión']['Val'].replace('.','').replace(',','.')) if 'Monto de Emisión' in df.index else 0
    except:
        nombre=''
        descripcion= ''
        ley=''
        isin=''
        moneda=''
        amortizacion=''
        intereses=''
        residual=0
    nombre_.append(nombre)
    descripcion_.append(descripcion)
    ley_.append(ley)
    isin_.append(isin)
    moneda_.append(moneda)
    amortizacion_.append(amortizacion)
    intereses_.append(intereses)
    residual_.append(residual)
    time.sleep(3.5)
data['Nombre']=nombre_
data['Descripción']=descripcion_
data['Ley']=ley_
data['ISIN']=isin_
data['Moneda']=moneda_
data['Amortización']=amortizacion_
data['Intereses']=intereses_
data['Monto Residual']=residual_
data.to_csv("Datos Bonos.csv")