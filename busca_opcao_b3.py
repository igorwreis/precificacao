def busca_codigo(a):

    """
    -->> Captura informacoes da opcao divulgadas pela B3, em forma de dicionario python <<--

    # IMPORTANTE: instalar bibliotecas destacadas abaixo

    Arg:
        a (str): Obrigatorio - Codigo da opcao de compra/venda a ser pesquisada

    Retorna dicionario com informacoes de codigo, vencimento, preco de exercicio e outros.

    No caso de existir mais de um registro com o codigo pesquisado,
    o programa retornara as informacoes da primeira linha da tabela encontrada.
    
    Retorna mensagem de erro caso o ativo informado nao seja uma opcao de compra/venda, 
    ou se nao for encontrado nenhum registro no portal da B3.

    Falhas sao comuns devido a instabilidades no portal da B3. Caso o programa
    nao conclua a captura, basta roda-lo novamente apos alguns instantes.
    """

    # INSTALAR BIBLIOTECAS ABAIXO NO AMBIENTE A SER UTILIZADO !
    # pip install bs4
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
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options

    try:

        ativo = str(a).upper().upper().replace(" ", "")

        url = "http://bvmf.bmfbovespa.com.br/cias-listadas/Titulos-Negociaveis/BuscaTitulosNegociaveis.aspx?idioma=pt-br"

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # RETIRAR/INCLUIR COMENTARIO ABAIXO PARA DESATIVAR/ATIVAR MODO HEADLESS
        #options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)

        sleep(1)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='ctl00_contentPlaceHolderConteudo_Menu_tabItem2']/span/span")))

        driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_Menu_tabItem2']/span/span").click()

        sleep(1)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='ctl00_contentPlaceHolderConteudo_txtCodigo_txtCodigo_text']")))

        codigo = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_txtCodigo_txtCodigo_text']")
        codigo.send_keys(ativo)

        sleep(1)

        driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_btnBuscarCodigo']").click()

        sleep(1)

        try:
            sleep(3)
            erro = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_lblTexto3']").get_attribute('textContent')
            if erro == 'Empresa/Código não encontrado.':
                driver.quit()
                return f'O código --{ativo.upper()}-- não foi encontrado. Verifique e tente novamente.'

        except:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((
                By.XPATH, "//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados']")))

                sleep(1)

                confirma_opc = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_lblDescricao']").get_attribute('textContent')

                if confirma_opc[:6] != 'Opções':
                    driver.quit()
                    return f'O código --{ativo.upper()}-- não é uma opção válida. Verifique e tente novamente.'

                else:
                    dic = {"ISIN": [],
                            "Especif": [],
                            "Objeto": [],
                            "Vencimento": [],
                            "Strike": [],
                            "Moeda": [],
                            "Protegida": [],
                            "Estilo": [], 
                            }

                    # Busca informacoes do ativo informado
                    ISIN = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[1]").get_attribute('textContent').strip()
                    Especif = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[2]").get_attribute('textContent').strip()
                    Objeto = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[3]").get_attribute('textContent').strip()
                    Vencimento = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[4]").get_attribute('textContent').strip()

                    Strike = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[5]").get_attribute('textContent').strip()
                    Strike = Strike.replace(',', '.')
                    Strike = round(float(Strike), 2)

                    Moeda = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[6]").get_attribute('textContent').strip()
                    Protegida = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[7]").get_attribute('textContent').strip()
                    Estilo = driver.find_element_by_xpath("//*[@id='ctl00_contentPlaceHolderConteudo_ctl00_grdDados_ctl01']/tbody/tr/td[8]").get_attribute('textContent').strip()

                    dic["ISIN"].append(ISIN)
                    dic["Especif"].append(Especif)
                    dic["Objeto"].append(Objeto)
                    dic["Vencimento"].append(Vencimento)
                    dic["Strike"].append(Strike)
                    dic["Moeda"].append(Moeda)
                    dic["Protegida"].append(Protegida)
                    dic["Estilo"].append(Estilo)

                    driver.quit()
                    return dic

            except:
                driver.quit()
                return f'Informações de --{ativo.upper()}-- não encontradas. Verifique e tente novamente.'

    except:
        driver.quit()
        return 'ERRO! Verifique a conexao, o codigo do ativo e tente novamente.'