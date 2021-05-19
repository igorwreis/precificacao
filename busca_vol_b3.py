def busca_vol(a):

    """
    -->> Captura volatilidade do ativo informado de acordo com informacoes divulgadas pela B3 <<--

    # IMPORTANTE: instalar bibliotecas destacadas abaixo

    Arg:
        a (str): Obrigatorio - Codigo do ativo a ser pesquisado

    Retorna dicionario com Desvio e Volatilidade de 1, 3, 6 e 12 meses.
    
    Erros sao comuns devido a instabilidades no portal da B3. Caso o programa
    nao conclua a captura, basta roda-lo novamente apos alguns instantes.
    """

    # INSTALAR BIBLIOTECAS ABAIXO NO AMBIENTE A SER UTILIZADO !
    # pip install selenium
    # pip install webdriver-manager

    from time import sleep
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options

    try:

        ativo = str(a).strip().upper().replace(" ", "")

        url = "https://sistemaswebb3-listados.b3.com.br/securitiesVolatilityPage/standard-deviation/false?language=pt-br"

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # ESTE PROGRAMA NAO FUNCIONA NO MODO HEADLESS
        #options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)

        sleep(1)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table")))

        sleep(1)

        codigo = driver.find_element_by_xpath("//*[@id='nameOrCode']")
        codigo.send_keys(ativo)

        sleep(1)

        driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[1]/div[3]/button").click()

        sleep(1)

        WebDriverWait(driver, 3).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table")))

        dic = {"Codigo": [],
                "Nome": [],
                "Especif": [],
                "DesvPad_1_mes": [],
                "VolAnual_1_mes": [],
                "DesvPad_3_meses": [],
                "VolAnual_3_meses": [],
                "DesvPad_6_meses": [],
                "VolAnual_6_meses": [],
                "DesvPad_12_meses": [],
                "VolAnual_12_meses": [], 
                }

        codigo = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[1]").get_attribute('textContent')
        nome = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[2]").get_attribute('textContent')
        espec = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[3]").get_attribute('textContent')

        desv1 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[4]").get_attribute('textContent')
        desv1 = desv1.replace(',', '.')
        desv1 = round(float(desv1), 4)

        vol1 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[5]").get_attribute('textContent')
        vol1 = vol1.replace(',', '.')
        vol1 = round(float(vol1), 2)

        desv3 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[6]").get_attribute('textContent')
        desv3 = desv3.replace(',', '.')
        desv3 = round(float(desv3), 4)

        vol3 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[7]").get_attribute('textContent')
        vol3 = vol3.replace(',', '.')
        vol3 = round(float(vol3), 2)

        desv6 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[8]").get_attribute('textContent')
        desv6 = desv6.replace(',', '.')
        desv6 = round(float(desv6), 4)

        vol6 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[9]").get_attribute('textContent')
        vol6 = vol6.replace(',', '.')
        vol6 = round(float(vol6), 2)

        desv12 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[10]").get_attribute('textContent')
        desv12 = desv12.replace(',', '.')
        desv12 = round(float(desv12), 4)

        vol12 = driver.find_element_by_xpath("//*[@id='divContainerIframeB3']/standard-deviation/form/div/div/div[2]/table/tbody/tr[1]/td[11]").get_attribute('textContent')
        vol12 = vol12.replace(',', '.')
        vol12 = round(float(vol12), 2)

        dic["Codigo"].append(codigo)
        dic["Nome"].append(nome)
        dic["Especif"].append(espec)
        dic["DesvPad_1_mes"].append(desv1)
        dic["VolAnual_1_mes"].append(vol1)
        dic["DesvPad_3_meses"].append(desv3)
        dic["VolAnual_3_meses"].append(vol3)
        dic["DesvPad_6_meses"].append(desv6)
        dic["VolAnual_6_meses"].append(vol6)
        dic["DesvPad_12_meses"].append(desv12)
        dic["VolAnual_12_meses"].append(vol12)

        driver.quit()
        return dic

    except:

        driver.quit()
        return 'ERRO! Verifique a conexao, o codigo do ativo e tente novamente.'
