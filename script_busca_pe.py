# criar um navegador

###############
# entrar no buscape
# pesquisar o nome do produto na barra de pesquisa
#
# entrar no google
# pesquisar o nome do produto no google
# clicar na aba shopping
# pegar o preço do produto no shopping
###############

# para cada item dentro da nossa base de dados ( para cada produto )
# procurar esse produto no google shopping
# verificar se algum dos produtos do google shopping está dentro da minha faixa de preço
# procurara esse produto no buscape
# verificar se algum dos produtos do buscape está dentro da minha faixa de preço
# salvar as ofertas boas em um dataframe( tabela )
# exportar pro excel
# enviar por e-mail o resultado da tabela

# libs
from time import sleep

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# importando/visualizar a base de dados
# tabela_produtos = pd.read_excel('buscas.xlsx')
# print(tabela_produtos)

# Criando a instância
option = uc.ChromeOptions()

# Utilizar-se do método 'add_argument' p/
# modificar o padrão de notificações e desabilitar o pop-up

# novo UC
option.add_argument(
    '--no-first-run --no-service-autorun --password-store=basic')
option.add_experimental_option("excludeSwitches", ['enable-logging'])
option.add_argument('--disable-notifications')
option.add_argument(('--ignore-certificate-erros'))
option.add_argument(('--start-minimized'))

##########################################


def busca_pe(produto, termos_banidos, preco_minimo, preco_maximo):

    # if __name__ == "__main__":

    termos_banidos = termos_banidos.lower()
    driver = uc.Chrome()
    # driver.minimize_window()
    # declarando produto e termos banidos
    # tratando "caixa alta"
    produto = produto.lower()

    lista_termos_banidos = termos_banidos.split(" ")  # transform. em lista
    lista_termos_produto = produto.split(" ")

    # precos
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)
    #print(preco_minimo, preco_maximo)

    driver.get('https://www.buscape.com.br/')

    driver.find_element(By. XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div/div/div[1]/input').send_keys(
        produto, Keys.ENTER)
    sleep(5)

    lista_produtos = driver.find_elements(
        By.CLASS_NAME, 'Cell_Content__fT5st')
    # print(f'Foram encontrados {len(lista_produtos)} produtos na página: ')

    lista_ofertas = []
    for item in lista_produtos:
        nome = item.find_element(
            By.CLASS_NAME, 'Cell_Name__pxLaW').text
        nome = nome.lower()

        # verificação do nome
        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True

        tem_todos_termos_produto = True
        for palavra in lista_termos_produto:
            if palavra not in nome:
                tem_todos_termos_produto = False

        if not tem_termos_banidos and tem_todos_termos_produto:
            try:
                preco = item.find_element(
                    By.CLASS_NAME, 'CellPrice_MainValue__JXsj_').text
                preco = preco.replace("R$", "").replace(
                    " ", "").replace(".", "")
                preco = preco.replace(",", ".")
                preco = float(preco)

                if not preco_minimo <= preco <= preco_maximo:
                    pass
                else:

                    link = item.get_attribute('href')
                    # print(nome, preco, link)
                    lista_ofertas.append((nome, preco, link))
                    print(lista_ofertas)
            except:
                continue
    return lista_ofertas
