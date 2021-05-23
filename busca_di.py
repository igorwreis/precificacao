def busca_di():

    """
    -->> Busca taxa DI anual divulgada pela B3, em formato decimal <<--
    # IMPORTANTE: instalar bibliotecas destacadas abaixo

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
    from selenium.webdriver.chrome.options import Options

    url = "http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-de-derivativos/indicadores/indicadores-financeiros/"

    try:

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # RETIRAR/INCLUIR COMENTARIO ABAIXO PARA ATIVAR/DESATIVAR MODO HEADLESS
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)

        sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='conteudo-principal']/div[4]/div/div/div[2]/div[1]/table/tbody/tr/td")))
        sleep(1)

        di_ano = driver.find_element_by_xpath("//*[@id='conteudo-principal']/div[4]/div/div/div[2]/div[1]/table/tbody/tr/td").get_attribute('textContent')

        di_ano = di_ano.split('%', 1)[0]
        di_ano = di_ano.replace(',', '.')
        di_ano = '{:.4f}'.format((float(di_ano))/100)

        driver.quit()
        return di_ano

    except:
        driver.quit()
        return 'ERRO! VERIFIQUE CONEXAO'

if __name__ == '__main__':
    busca_di()