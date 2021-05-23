def ultimo_preco(a, d=0, p=0):

    """
    -->> Coleta preco da ultima negociacao da acao desejada conforme
    data informada e de acordo com informacoes divulgadas pela B3 <<--

    # IMPORTANTE: instalar bibliotecas abaixo

    a (str): Obrigatorio - Codigo do ativo a ser pesquisado
    d (str): Opcional - data a ser pesquisada, em formato string DD/MM/AAAA.
    Manter nulo ou 0 para data atual ou ultima data util.
    p (int): Opcional - dias uteis anteriores a data-base.
    Manter nulo ou 0 para data atual ou ultima data util.

    Retorna dicionario com informacoes do ultimo negocio realizado na data informada.
    Delay de aprox 15 minutos quando o mercado estiver aberto.
    
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
    from selenium.webdriver.common.action_chains import ActionChains

    try:

        ativo = str(a).strip().upper().replace(" ", "")

        if p > 0: p = p * -1
        data_preco = diatrabalho(p, d)

        url = "https://arquivos.b3.com.br/negocios/?lang=pt"

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # RETIRAR/INCLUIR COMENTARIO ABAIXO PARA ATIVAR/DESATIVAR MODO HEADLESS
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)

        sleep(1)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/div[1]")))

        sleep(1)

        codigo = driver.find_element_by_xpath("//*[@id='root']/div/div/div[1]/div/div/div[1]")

        ActionChains(driver).move_to_element(codigo).click().send_keys(ativo).perform()

        sleep(1)

        driver.find_element_by_xpath("//*[@id='root']/div/div/div[1]/div/div/div[2]/div").click()
        dia = driver.find_element_by_xpath("//*[@id='root']/div/div/div[1]/div/div/div[2]/div")

        ActionChains(driver).move_to_element(dia).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        sleep(1)
        ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
        sleep(1)
        ActionChains(driver).send_keys(data_preco).perform()
        sleep(1)

        driver.find_element_by_xpath("//*[@id='root']/div/div/div[1]/div/div/div[3]").click()

        sleep(1)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='root']/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]")))

        dic = {
        "Papel": [],
        "Quantidade": [],
        "Preco": [],
        "Num Neg": [],
        "Data Ref": [],
        "Hora": [],
        }

        Papel = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]").get_attribute('textContent').strip()
        Quantidade = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]").get_attribute('textContent').strip()
        Quantidade = str(Quantidade)
        Quantidade = Quantidade.replace('.', '')
        Quantidade = round(float(Quantidade), 0)

        Preco = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[1]/table/tbody/tr[1]/td[3]").get_attribute('textContent').strip()
        Preco = Preco.replace(',', '.')
        Preco = round(float(Preco), 2)

        Num_Neg = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[1]/table/tbody/tr[1]/td[4]").get_attribute('textContent').strip()
        Num_Neg = Num_Neg.replace('.', '')
        Num_Neg = str(Num_Neg)

        Data_Ref = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[1]/table/tbody/tr[1]/td[5]").get_attribute('textContent').strip()
        Hora = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div[1]/table/tbody/tr[1]/td[6]").get_attribute('textContent').strip()

        dic["Papel"].append(Papel)
        dic["Quantidade"].append(Quantidade)
        dic["Preco"].append(Preco)
        dic["Num Neg"].append(Num_Neg)
        dic["Data Ref"].append(Data_Ref)
        dic["Hora"].append(Hora)

        driver.quit()
        return dic

    except:
        driver.quit()
        return 'ERRO! Verifique conexao, data e codigo do ativo.'

def diatrabalho(p=0, d=0):

    """
    -->> Retorna data util de acordo com relacao de feriados ANBIMA (ja disponibilizada pela
         funcao feriados_lista), periodo e data-base informados pelo usuario (opcionais);
         A relacao de feriados utilizada por essa funcao pode ser
         encontrada em: https://www.anbima.com.br/feriados/feriados.asp 
         Qualquer edicao dessas datas devera ser realizada dentro da funcao feriados_lista() <<--

    Args:
        p (int, optional): Intervalo desejado em DIAS UTEIS (numero inteiro)
        d (int, optional): Data-Base desejada; Manter nulo para data atual

    # IMPORTANTE: se a data-base (seja a informada ou a atual) for um dia nao-util,
        a funcao iniciara a contagem a partir do primeiro dia util anterior a esta

    Returns:
        [date]
    """

    from datetime import datetime, date, timedelta
    
    try:
        if d == 0:
            d = datetime.now().date()
            
        if type(d) == str:
            d = datetime.strptime(d, '%d/%m/%Y').date()
            
        if type(d) == datetime:
            d = d.date()
            
        if type(p) != int or p % 1 != 0:
            print('[ERRO!] Informe um período em número INTEIRO. Mantenha os campos nulos para\n'
            'data atual e período = 0. Variáveis são aceitas desde que no formato adequado.')
            return False
    
        feriados = feriados_lista()

        while d.strftime('%d/%m/%Y') in feriados or datetime.weekday(d) > 4:
            d = d + timedelta(days=-1)
        
        while p != 0:
            a = p/abs(p)
            d = d + timedelta(days=a)
    
            if d.strftime('%d/%m/%Y') in feriados or datetime.weekday(d) > 4:
                p += 0
            else:
                p -= a
                
    except (ValueError, TypeError, AttributeError):
        print('[ERRO!] Insira uma data no formato DD/MM/AAAA (com barras e entre aspas) e um período em número INTEIRO.\n'
            'Mantenha os campos nulos para data atual e período = 0. Variáveis são aceitas desde que no formato adequado.')
    
    return d.strftime('%d/%m/%Y')


def feriados_lista():

    """
    -->> Retorna lista com feriados no formato dd/mm/aaaa (string);
         A relacao de feriados utilizada por essa funcao pode ser
         encontrada em: https://www.anbima.com.br/feriados/feriados.asp 
         Qualquer edicao dessas datas devera ser realizada dentro da funcao <<--
    """

    feriados = [
         '01/01/2001', '26/02/2001', '27/02/2001', '13/04/2001', '21/04/2001', '01/05/2001', '14/06/2001', '07/09/2001',
         '12/10/2001', '02/11/2001', '15/11/2001', '25/12/2001', '01/01/2002', '11/02/2002', '12/02/2002', '29/03/2002',
         '21/04/2002', '01/05/2002', '30/05/2002', '07/09/2002', '12/10/2002', '02/11/2002', '15/11/2002', '25/12/2002',
         '01/01/2003', '03/03/2003', '04/03/2003', '18/04/2003', '21/04/2003', '01/05/2003', '19/06/2003', '07/09/2003',
         '12/10/2003', '02/11/2003', '15/11/2003', '25/12/2003', '01/01/2004', '23/02/2004', '24/02/2004', '09/04/2004',
         '21/04/2004', '01/05/2004', '10/06/2004', '07/09/2004', '12/10/2004', '02/11/2004', '15/11/2004', '25/12/2004',
         '01/01/2005', '07/02/2005', '08/02/2005', '25/03/2005', '21/04/2005', '01/05/2005', '26/05/2005', '07/09/2005',
         '12/10/2005', '02/11/2005', '15/11/2005', '25/12/2005', '01/01/2006', '27/02/2006', '28/02/2006', '14/04/2006',
         '21/04/2006', '01/05/2006', '15/06/2006', '07/09/2006', '12/10/2006', '02/11/2006', '15/11/2006', '25/12/2006',
         '01/01/2007', '19/02/2007', '20/02/2007', '06/04/2007', '21/04/2007', '01/05/2007', '07/06/2007', '07/09/2007',
         '12/10/2007', '02/11/2007', '15/11/2007', '25/12/2007', '01/01/2008', '04/02/2008', '05/02/2008', '21/03/2008',
         '21/04/2008', '01/05/2008', '22/05/2008', '07/09/2008', '12/10/2008', '02/11/2008', '15/11/2008', '25/12/2008',
         '01/01/2009', '23/02/2009', '24/02/2009', '10/04/2009', '21/04/2009', '01/05/2009', '11/06/2009', '07/09/2009',
         '12/10/2009', '02/11/2009', '15/11/2009', '25/12/2009', '01/01/2010', '15/02/2010', '16/02/2010', '02/04/2010',
         '21/04/2010', '01/05/2010', '03/06/2010', '07/09/2010', '12/10/2010', '02/11/2010', '15/11/2010', '25/12/2010',
         '01/01/2011', '07/03/2011', '08/03/2011', '21/04/2011', '22/04/2011', '01/05/2011', '23/06/2011', '07/09/2011',
         '12/10/2011', '02/11/2011', '15/11/2011', '25/12/2011', '01/01/2012', '20/02/2012', '21/02/2012', '06/04/2012',
         '21/04/2012', '01/05/2012', '07/06/2012', '07/09/2012', '12/10/2012', '02/11/2012', '15/11/2012', '25/12/2012',
         '01/01/2013', '11/02/2013', '12/02/2013', '29/03/2013', '21/04/2013', '01/05/2013', '30/05/2013', '07/09/2013',
         '12/10/2013', '02/11/2013', '15/11/2013', '25/12/2013', '01/01/2014', '03/03/2014', '04/03/2014', '18/04/2014',
         '21/04/2014', '01/05/2014', '19/06/2014', '07/09/2014', '12/10/2014', '02/11/2014', '15/11/2014', '25/12/2014',
         '01/01/2015', '16/02/2015', '17/02/2015', '03/04/2015', '21/04/2015', '01/05/2015', '04/06/2015', '07/09/2015',
         '12/10/2015', '02/11/2015', '15/11/2015', '25/12/2015', '01/01/2016', '08/02/2016', '09/02/2016', '25/03/2016',
         '21/04/2016', '01/05/2016', '26/05/2016', '07/09/2016', '12/10/2016', '02/11/2016', '15/11/2016', '25/12/2016',
         '01/01/2017', '27/02/2017', '28/02/2017', '14/04/2017', '21/04/2017', '01/05/2017', '15/06/2017', '07/09/2017',
         '12/10/2017', '02/11/2017', '15/11/2017', '25/12/2017', '01/01/2018', '12/02/2018', '13/02/2018', '30/03/2018',
         '21/04/2018', '01/05/2018', '31/05/2018', '07/09/2018', '12/10/2018', '02/11/2018', '15/11/2018', '25/12/2018',
         '01/01/2019', '04/03/2019', '05/03/2019', '19/04/2019', '21/04/2019', '01/05/2019', '20/06/2019', '07/09/2019',
         '12/10/2019', '02/11/2019', '15/11/2019', '25/12/2019', '01/01/2020', '24/02/2020', '25/02/2020', '10/04/2020',
         '21/04/2020', '01/05/2020', '11/06/2020', '07/09/2020', '12/10/2020', '02/11/2020', '15/11/2020', '25/12/2020',
         '01/01/2021', '15/02/2021', '16/02/2021', '02/04/2021', '21/04/2021', '01/05/2021', '03/06/2021', '07/09/2021',
         '12/10/2021', '02/11/2021', '15/11/2021', '25/12/2021', '01/01/2022', '28/02/2022', '01/03/2022', '15/04/2022',
         '21/04/2022', '01/05/2022', '16/06/2022', '07/09/2022', '12/10/2022', '02/11/2022', '15/11/2022', '25/12/2022',
         '01/01/2023', '20/02/2023', '21/02/2023', '07/04/2023', '21/04/2023', '01/05/2023', '08/06/2023', '07/09/2023',
         '12/10/2023', '02/11/2023', '15/11/2023', '25/12/2023', '01/01/2024', '12/02/2024', '13/02/2024', '29/03/2024',
         '21/04/2024', '01/05/2024', '30/05/2024', '07/09/2024', '12/10/2024', '02/11/2024', '15/11/2024', '25/12/2024',
         '01/01/2025', '03/03/2025', '04/03/2025', '18/04/2025', '21/04/2025', '01/05/2025', '19/06/2025', '07/09/2025',
         '12/10/2025', '02/11/2025', '15/11/2025', '25/12/2025', '01/01/2026', '16/02/2026', '17/02/2026', '03/04/2026',
         '21/04/2026', '01/05/2026', '04/06/2026', '07/09/2026', '12/10/2026', '02/11/2026', '15/11/2026', '25/12/2026',
         '01/01/2027', '08/02/2027', '09/02/2027', '26/03/2027', '21/04/2027', '01/05/2027', '27/05/2027', '07/09/2027',
         '12/10/2027', '02/11/2027', '15/11/2027', '25/12/2027', '01/01/2028', '28/02/2028', '29/02/2028', '14/04/2028',
         '21/04/2028', '01/05/2028', '15/06/2028', '07/09/2028', '12/10/2028', '02/11/2028', '15/11/2028', '25/12/2028',
         '01/01/2029', '12/02/2029', '13/02/2029', '30/03/2029', '21/04/2029', '01/05/2029', '31/05/2029', '07/09/2029',
         '12/10/2029', '02/11/2029', '15/11/2029', '25/12/2029', '01/01/2030', '04/03/2030', '05/03/2030', '19/04/2030',
         '21/04/2030', '01/05/2030', '20/06/2030', '07/09/2030', '12/10/2030', '02/11/2030', '15/11/2030', '25/12/2030',
         '01/01/2031', '24/02/2031', '25/02/2031', '11/04/2031', '21/04/2031', '01/05/2031', '12/06/2031', '07/09/2031',
         '12/10/2031', '02/11/2031', '15/11/2031', '25/12/2031', '01/01/2032', '09/02/2032', '10/02/2032', '26/03/2032',
         '21/04/2032', '01/05/2032', '27/05/2032', '07/09/2032', '12/10/2032', '02/11/2032', '15/11/2032', '25/12/2032',
         '01/01/2033', '28/02/2033', '01/03/2033', '15/04/2033', '21/04/2033', '01/05/2033', '16/06/2033', '07/09/2033',
         '12/10/2033', '02/11/2033', '15/11/2033', '25/12/2033', '01/01/2034', '20/02/2034', '21/02/2034', '07/04/2034',
         '21/04/2034', '01/05/2034', '08/06/2034', '07/09/2034', '12/10/2034', '02/11/2034', '15/11/2034', '25/12/2034',
         '01/01/2035', '05/02/2035', '06/02/2035', '23/03/2035', '21/04/2035', '01/05/2035', '24/05/2035', '07/09/2035',
         '12/10/2035', '02/11/2035', '15/11/2035', '25/12/2035', '01/01/2036', '25/02/2036', '26/02/2036', '11/04/2036',
         '21/04/2036', '01/05/2036', '12/06/2036', '07/09/2036', '12/10/2036', '02/11/2036', '15/11/2036', '25/12/2036',
         '01/01/2037', '16/02/2037', '17/02/2037', '03/04/2037', '21/04/2037', '01/05/2037', '04/06/2037', '07/09/2037',
         '12/10/2037', '02/11/2037', '15/11/2037', '25/12/2037', '01/01/2038', '08/03/2038', '09/03/2038', '21/04/2038',
         '23/04/2038', '01/05/2038', '24/06/2038', '07/09/2038', '12/10/2038', '02/11/2038', '15/11/2038', '25/12/2038',
         '01/01/2039', '21/02/2039', '22/02/2039', '08/04/2039', '21/04/2039', '01/05/2039', '09/06/2039', '07/09/2039',
         '12/10/2039', '02/11/2039', '15/11/2039', '25/12/2039', '01/01/2040', '13/02/2040', '14/02/2040', '30/03/2040',
         '21/04/2040', '01/05/2040', '31/05/2040', '07/09/2040', '12/10/2040', '02/11/2040', '15/11/2040', '25/12/2040',
         '01/01/2041', '04/03/2041', '05/03/2041', '19/04/2041', '21/04/2041', '01/05/2041', '20/06/2041', '07/09/2041',
         '12/10/2041', '02/11/2041', '15/11/2041', '25/12/2041', '01/01/2042', '17/02/2042', '18/02/2042', '04/04/2042',
         '21/04/2042', '01/05/2042', '05/06/2042', '07/09/2042', '12/10/2042', '02/11/2042', '15/11/2042', '25/12/2042',
         '01/01/2043', '09/02/2043', '10/02/2043', '27/03/2043', '21/04/2043', '01/05/2043', '28/05/2043', '07/09/2043',
         '12/10/2043', '02/11/2043', '15/11/2043', '25/12/2043', '01/01/2044', '29/02/2044', '01/03/2044', '15/04/2044',
         '21/04/2044', '01/05/2044', '16/06/2044', '07/09/2044', '12/10/2044', '02/11/2044', '15/11/2044', '25/12/2044',
         '01/01/2045', '20/02/2045', '21/02/2045', '07/04/2045', '21/04/2045', '01/05/2045', '08/06/2045', '07/09/2045',
         '12/10/2045', '02/11/2045', '15/11/2045', '25/12/2045', '01/01/2046', '05/02/2046', '06/02/2046', '23/03/2046',
         '21/04/2046', '01/05/2046', '24/05/2046', '07/09/2046', '12/10/2046', '02/11/2046', '15/11/2046', '25/12/2046',
         '01/01/2047', '25/02/2047', '26/02/2047', '12/04/2047', '21/04/2047', '01/05/2047', '13/06/2047', '07/09/2047',
         '12/10/2047', '02/11/2047', '15/11/2047', '25/12/2047', '01/01/2048', '17/02/2048', '18/02/2048', '03/04/2048',
         '21/04/2048', '01/05/2048', '04/06/2048', '07/09/2048', '12/10/2048', '02/11/2048', '15/11/2048', '25/12/2048',
         '01/01/2049', '01/03/2049', '02/03/2049', '16/04/2049', '21/04/2049', '01/05/2049', '17/06/2049', '07/09/2049',
         '12/10/2049', '02/11/2049', '15/11/2049', '25/12/2049', '01/01/2050', '21/02/2050', '22/02/2050', '08/04/2050',
         '21/04/2050', '01/05/2050', '09/06/2050', '07/09/2050', '12/10/2050', '02/11/2050', '15/11/2050', '25/12/2050',
         '01/01/2051', '13/02/2051', '14/02/2051', '31/03/2051', '21/04/2051', '01/05/2051', '01/06/2051', '07/09/2051',
         '12/10/2051', '02/11/2051', '15/11/2051', '25/12/2051', '01/01/2052', '04/03/2052', '05/03/2052', '19/04/2052',
         '21/04/2052', '01/05/2052', '20/06/2052', '07/09/2052', '12/10/2052', '02/11/2052', '15/11/2052', '25/12/2052',
         '01/01/2053', '17/02/2053', '18/02/2053', '04/04/2053', '21/04/2053', '01/05/2053', '05/06/2053', '07/09/2053',
         '12/10/2053', '02/11/2053', '15/11/2053', '25/12/2053', '01/01/2054', '09/02/2054', '10/02/2054', '27/03/2054',
         '21/04/2054', '01/05/2054', '28/05/2054', '07/09/2054', '12/10/2054', '02/11/2054', '15/11/2054', '25/12/2054',
         '01/01/2055', '01/03/2055', '02/03/2055', '16/04/2055', '21/04/2055', '01/05/2055', '17/06/2055', '07/09/2055',
         '12/10/2055', '02/11/2055', '15/11/2055', '25/12/2055', '01/01/2056', '14/02/2056', '15/02/2056', '31/03/2056',
         '21/04/2056', '01/05/2056', '01/06/2056', '07/09/2056', '12/10/2056', '02/11/2056', '15/11/2056', '25/12/2056',
         '01/01/2057', '05/03/2057', '06/03/2057', '20/04/2057', '21/04/2057', '01/05/2057', '21/06/2057', '07/09/2057',
         '12/10/2057', '02/11/2057', '15/11/2057', '25/12/2057', '01/01/2058', '25/02/2058', '26/02/2058', '12/04/2058',
         '21/04/2058', '01/05/2058', '13/06/2058', '07/09/2058', '12/10/2058', '02/11/2058', '15/11/2058', '25/12/2058',
         '01/01/2059', '10/02/2059', '11/02/2059', '28/03/2059', '21/04/2059', '01/05/2059', '29/05/2059', '07/09/2059',
         '12/10/2059', '02/11/2059', '15/11/2059', '25/12/2059', '01/01/2060', '01/03/2060', '02/03/2060', '16/04/2060',
         '21/04/2060', '01/05/2060', '17/06/2060', '07/09/2060', '12/10/2060', '02/11/2060', '15/11/2060', '25/12/2060',
         '01/01/2061', '21/02/2061', '22/02/2061', '08/04/2061', '21/04/2061', '01/05/2061', '09/06/2061', '07/09/2061',
         '12/10/2061', '02/11/2061', '15/11/2061', '25/12/2061', '01/01/2062', '06/02/2062', '07/02/2062', '24/03/2062',
         '21/04/2062', '01/05/2062', '25/05/2062', '07/09/2062', '12/10/2062', '02/11/2062', '15/11/2062', '25/12/2062',
         '01/01/2063', '26/02/2063', '27/02/2063', '13/04/2063', '21/04/2063', '01/05/2063', '14/06/2063', '07/09/2063',
         '12/10/2063', '02/11/2063', '15/11/2063', '25/12/2063', '01/01/2064', '18/02/2064', '19/02/2064', '04/04/2064',
         '21/04/2064', '01/05/2064', '05/06/2064', '07/09/2064', '12/10/2064', '02/11/2064', '15/11/2064', '25/12/2064',
         '01/01/2065', '09/02/2065', '10/02/2065', '27/03/2065', '21/04/2065', '01/05/2065', '28/05/2065', '07/09/2065',
         '12/10/2065', '02/11/2065', '15/11/2065', '25/12/2065', '01/01/2066', '22/02/2066', '23/02/2066', '09/04/2066',
         '21/04/2066', '01/05/2066', '10/06/2066', '07/09/2066', '12/10/2066', '02/11/2066', '15/11/2066', '25/12/2066',
         '01/01/2067', '14/02/2067', '15/02/2067', '01/04/2067', '21/04/2067', '01/05/2067', '02/06/2067', '07/09/2067',
         '12/10/2067', '02/11/2067', '15/11/2067', '25/12/2067', '01/01/2068', '05/03/2068', '06/03/2068', '20/04/2068',
         '21/04/2068', '01/05/2068', '21/06/2068', '07/09/2068', '12/10/2068', '02/11/2068', '15/11/2068', '25/12/2068',
         '01/01/2069', '25/02/2069', '26/02/2069', '12/04/2069', '21/04/2069', '01/05/2069', '13/06/2069', '07/09/2069',
         '12/10/2069', '02/11/2069', '15/11/2069', '25/12/2069', '01/01/2070', '10/02/2070', '11/02/2070', '28/03/2070',
         '21/04/2070', '01/05/2070', '29/05/2070', '07/09/2070', '12/10/2070', '02/11/2070', '15/11/2070', '25/12/2070',
         '01/01/2071', '02/03/2071', '03/03/2071', '17/04/2071', '21/04/2071', '01/05/2071', '18/06/2071', '07/09/2071',
         '12/10/2071', '02/11/2071', '15/11/2071', '25/12/2071', '01/01/2072', '22/02/2072', '23/02/2072', '08/04/2072',
         '21/04/2072', '01/05/2072', '09/06/2072', '07/09/2072', '12/10/2072', '02/11/2072', '15/11/2072', '25/12/2072',
         '01/01/2073', '06/02/2073', '07/02/2073', '24/03/2073', '21/04/2073', '01/05/2073', '25/05/2073', '07/09/2073',
         '12/10/2073', '02/11/2073', '15/11/2073', '25/12/2073', '01/01/2074', '26/02/2074', '27/02/2074', '13/04/2074',
         '21/04/2074', '01/05/2074', '14/06/2074', '07/09/2074', '12/10/2074', '02/11/2074', '15/11/2074', '25/12/2074',
         '01/01/2075', '18/02/2075', '19/02/2075', '05/04/2075', '21/04/2075', '01/05/2075', '06/06/2075', '07/09/2075',
         '12/10/2075', '02/11/2075', '15/11/2075', '25/12/2075', '01/01/2076', '02/03/2076', '03/03/2076', '17/04/2076',
         '21/04/2076', '01/05/2076', '18/06/2076', '07/09/2076', '12/10/2076', '02/11/2076', '15/11/2076', '25/12/2076',
         '01/01/2077', '22/02/2077', '23/02/2077', '09/04/2077', '21/04/2077', '01/05/2077', '10/06/2077', '07/09/2077',
         '12/10/2077', '02/11/2077', '15/11/2077', '25/12/2077', '01/01/2078', '14/02/2078', '15/02/2078', '01/04/2078',
         '21/04/2078', '01/05/2078', '02/06/2078', '07/09/2078', '12/10/2078', '02/11/2078', '15/11/2078', '25/12/2078'
         ]

    return feriados
