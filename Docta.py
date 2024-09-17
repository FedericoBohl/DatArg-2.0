from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import pandas as pd
import time
import streamlit as st

@st.cache_resource
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=chrome_options,
    )
class DoctaCap:
    def __init__(self):

        #driver = get_driver()
        options = Options() 
        options.add_argument("--headless=new")
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=options)
        self.token_info = None
        self.urls={'CER':'https://www.doctacapital.com.ar/dashboard/bonos/general/cer',
                   'DL':'https://www.doctacapital.com.ar/dashboard/bonos/general/dollar-linked',
                   'Soberanos':'https://www.doctacapital.com.ar/dashboard/bonos/general/hard-dollar',
                   'ON':'https://www.doctacapital.com.ar/dashboard/bonos/general/on',
                   'BOP':'https://www.doctacapital.com.ar/dashboard/bonos/general/bopreal',
                   'Acciones':'https://www.doctacapital.com.ar/dashboard/acciones/general',
                   'Cedears':'https://www.doctacapital.com.ar/dashboard/cedears/general',
                   'lecaps':'https://www.doctacapital.com.ar/dashboard/bonos/general/fixed-rate'
                    }
        self.df={'CER':None,
                   'DL':None,
                   'Soberanos':None,
                   'ON':None,
                   'BOP':None,
                   'Acciones':None,
                   'Cedears':None,
                   'lecaps':None
                    }
        for key in self.df:
            try:
                self.df[key]=self.extract_table(self.urls[key],driver)
            except:continue
        try:
            self.df['Soberanos']=self.df['Soberanos'][~self.df['Soberanos'].index.str.endswith('C')]
            self.df['Soberanos']=pd.concat([self.df['Soberanos'],self.df['BOP']])
        except:pass
    def extract_table(self,url,driver)->pd.DataFrame:
        data=[['Sin resultados.']]
        while data[0][0]=='Sin resultados.':
            try:
                driver.get(url=url)
                wait = WebDriverWait(driver, 5)
                button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Limpiar filtros']")))
                button.click()
                time.sleep(2.5)

                wait = WebDriverWait(driver, 5)  # Esperar hasta 30 segundos
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

                # Encuentra la última ngx-datatable
                element=driver.find_element(By.TAG_NAME, 'table')
                head=element.find_element(By.TAG_NAME,'thead')
                body=element.find_element(By.TAG_NAME,'tbody')
                cols= [i.text for i in head.find_elements(By.TAG_NAME,'th')]
                data=[[td.text for td in tr.find_elements(By.TAG_NAME,'td')] for tr in body.find_elements(By.TAG_NAME,'tr')]
            except Exception as e:
                print(e,'\n')
                continue
        data=pd.DataFrame(data,columns=cols)
        data=data[data['Ticker']!='tc-mayorista']
        tickers=[]
        tipo=[]
        for row in data['Ticker']:
            tickers.append(row.split('\n')[0])
            tipo.append(row.split('\n')[1])
        data['Ticker']=tickers
        data['Tipo']=tipo
        data=data[data['Tipo']=='24hs']
        data['Último precio']=[float(i.split(' ')[0].replace('$\n','').replace('.','').replace(',','.')) for i in data['Último precio']]
        data['Variación']=[float(i.replace('+','').replace('\n%','').replace(',','.')) for i in data['Variación']]

        if 'TIR' in cols:
            data['TIR']=[float(i.replace('.','').replace('%','').replace(',','.')) for i in data['TIR']]
            data['MD']=[float(i.replace('.','').replace(',','.')) for i in data['MD']]
            data['Valor técnico']=[float(i.replace('.','').replace(',','.')) for i in data['Valor técnico']]
            data['Paridad']=[float(i.replace('.','').replace('%','').replace(',','.')) for i in data['Paridad']]
            data=data[['Ticker', 'Último precio', 'Variación','TIR', 'MD','Valor técnico', 'Paridad']]
        elif 'TEM' in cols:
            data['TEM']=[float(i.replace('.','').replace('%','').replace(',','.')) for i in data['TEM']]
            data['MD']=[float(i.replace(',','.')) for i in data['MD']]
            data['Valor técnico']=[float(i.replace('.','').replace(',','.')) for i in data['Valor técnico']]
            data['Paridad']=[float(i.replace('.','').replace('%','').replace(',','.')) for i in data['Paridad']]
            data=data[['Ticker', 'Último precio', 'Variación','TEM', 'MD','Valor técnico', 'Paridad']]
        else:
            data['Último precio']=[float(i.split(' ')[0].replace('$\n','').replace('.','').replace(',','.')) for i in data['Último precio']]
            data['Variación']=[float(i.replace('+','').replace('\n%','').replace(',','.')) for i in data['Variación']]
            data=data[['Ticker', 'Último precio', 'Variación']]
        data.set_index('Ticker',inplace=True)
        return data
