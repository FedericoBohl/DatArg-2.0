from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configuración del webdriver (asegúrate de tener el webdriver correcto instalado)
url = "https://cmegroup-tools.quikstrike.net/User/QuikStrikeView.aspx?viewitemid=IntegratedFedWatchTool&userId=lwolf&jobRole=&company=&companyType=&userId=lwolf&jobRole=&company=&companyType=&insid=134330738&qsid=cd7c9839-5cb4-4b1e-884c-2e559f28b43d"

def extract_data():
    driver = webdriver.Chrome()
    # Navega al sitio web
    driver.get(url)
    time.sleep(5)
    # Haz clic en la pestaña "Probabilities"
    probabilities_tab = driver.find_element(By.ID, "ctl00_MainContent_ucViewControl_IntegratedFedWatchTool_lbPTree")
    probabilities_tab.click()
    time.sleep(5)
    table = driver.find_elements(By.TAG_NAME, "table")[2]
    rows = table.find_elements(By.TAG_NAME, "tr")
    columns=[col.text for col in rows[1].find_elements(By.TAG_NAME, "th")]
    data = []
    for row in rows[2:]:
        data.append(row.text.split(' '))
    count=len(columns)
    data2=[]
    for i in range(len(data)):
        if len(data[i])<count:
            remplazar=[data[i][0]]
            for j in range(count-len(data[i])):
                remplazar.append('0.0%')
            for j in data[i][1:]:
                remplazar.append(j)
            data2.append(remplazar)
        else: data2.append(data[i])
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('fed_rate_data.csv',index=False)

    time.sleep(5)
    # Haz clic en la pestaña "Probabilities"
    dotplot_tab = driver.find_element(By.ID, "ctl00_MainContent_ucViewControl_IntegratedFedWatchTool_lbDotPlotTable")
    dotplot_tab.click()
    time.sleep(5)
    table=driver.find_elements(By.TAG_NAME, "table")[1]
    rows = table.find_elements(By.TAG_NAME, "tr")
    column=rows[0].text.split(' ')
    column.remove('RUN')
    column[-1]='Largo Plazo'
    column[0]=column[0].replace('\n',' ')
    data=[]
    time.sleep(1)
    for row in rows[1:]:
        row_data=[]
        attempts = 0
        success = False
        while attempts<3:
            try:
                cols=row.find_elements(By.TAG_NAME, "td")
                for i in cols:
                    row_data.append(float(i.text) if i.text!='' else None)
                success = True
                break
            except:
                attempts += 1
        data.append(row_data)
    df=pd.DataFrame(data=data,columns=column)
    df.to_csv('dotplot.csv',index=False)
    driver.quit()


strikes=0
while strikes!=3:
    try:
        extract_data()
        print('Datos Obtenidos')
        break
    except:
        time.sleep(5)
        strikes+=1
        pass