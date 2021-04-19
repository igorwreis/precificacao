def busca_dados():

    """
    -->> Captura volatilidade de ativos de acordo com informacoes divulgadas pela B3 <<--

    # IMPORTANTE: instalar bibliotecas e informar dentro do programa o local a ser salvo

    Retorna arquivo txt com Desvio e Volatilidade de 1, 3, 6 e 12 meses.
    
    Erros sao comuns devido a instabilidades no portal da B3. Caso o programa
    nao conclua a captura, basta roda-lo novamente apos alguns instantes.
    """

    # INSTALAR BIBLIOTECAS ABAIXO NO AMBIENTE A SER UTILIZADO !
    # pip install getpass
    # pip install pandas
    # pip install beautifulsoup4
    # pip install selenium
    # pip install webdriver-manager

    from getpass import getuser
    from time import sleep
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    # SE DESEJAR, ALTERAR ABAIXO O DIRETORIO ONDE O ARQUIVO SERA SALVO, INFORMANDO -USUARIO-
    diretorio = r'C:\\Users\\' + getuser() + '\\Downloads\\vol_ativos_b3.txt'
    # diretorio = r'C:/Users/ -USUARIO- /Downloads/vol_ativos_b3.txt'

    url = "https://sistemaswebb3-listados.b3.com.br/securitiesVolatilityPage/standard-deviation/false?language=pt-br"

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # ESTE PROGRAMA NAO FUNCIONA NO MODO HEADLESS
    #options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((
        By.XPATH, "//*[@id='listing_pagination']/pagination-template/ul/li[9]/a/span[2]")))
    
    ultima_pagina = driver.find_element_by_xpath("//*[@id='listing_pagination']/pagination-template/ul/li[9]/a/span[2]").get_attribute('textContent')
    ultima_pagina = int(ultima_pagina)
    c = 0
    d = 0

    sleep(1)
    df_geral = pd.DataFrame(columns=[])

    try:
        while d < 5:
        # O PROGRAMA EXECUTA A MESMA RASPAGEM 5 VEZES PARA GARANTIR
        # QUE TODAS AS TABELAS DE TODAS AS PAGINAS SEJAM CAPTURADAS
            while c < ultima_pagina:
                
                element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((
                    By.XPATH, "//*[@id='divContainerIframeB3']")))

                html_content = element.get_attribute('outerHTML')
                soup = bs(html_content, 'html.parser')
                table = soup.find(name='table')

                df = pd.read_html(str(table), encoding = 'utf-8', decimal=",", thousands='.')[0]

                df_geral = df_geral.append(df).reset_index(drop=True)

                WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                    By.XPATH, "//*[@id='listing_pagination']/pagination-template/ul/li[10]")))
                driver.find_element_by_xpath("//*[@id='listing_pagination']/pagination-template/ul/li[10]").click()

                c += 1

            WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                By.XPATH, "//*[@id='listing_pagination']/pagination-template/ul/li[3]/a/span[2]")))
            driver.find_element_by_xpath("//*[@id='listing_pagination']/pagination-template/ul/li[3]/a/span[2]").click()

            c = 0
            d += 1
            sleep(1)

        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='divContainerIframeB3']")))

        sleep(1)

        html_content = element.get_attribute('outerHTML')
        soup = bs(html_content, 'html.parser')
        table = soup.find(name='table')

        df = pd.read_html(str(table), encoding = 'utf-8', decimal=",", thousands='.')[0]

        df_geral = df_geral.append(df).reset_index(drop=True)            

        df_geral.drop_duplicates(keep='first', inplace=True)

        df_geral.columns = ['Codigo', 'Nome', 'Espec', 'Desvpad1', 'Vol1',
                        'Desvpad3', 'Vol3', 'Desvpad6', 'Vol6', 'Desvpad12', 'Vol12']

        df_geral = df_geral.sort_values('Codigo', ascending=True)

        df_geral.reset_index(drop=True, inplace=True)

        df_geral.to_csv(diretorio, index=False, encoding='cp1252', decimal=',', sep=';')
        
        driver.quit()

        return df_geral
        
    except:
        driver.quit()
        return f'Erro na página {c}. Verifique conexão e tente novamente.'

if __name__ == '__main__':
    busca_dados()