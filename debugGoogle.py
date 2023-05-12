
###############
# entrar no def_busca_google
# pesquisar o nome do produto no def_busca_google
# clicar na aba shopping
# pegar o preço do produto no shopping
###############

# para cada item dentro da nossa base de dados ( para cada produto )
# procurar esse produto no def_busca_google shopping
# verificar se algum dos produtos do def_busca_google shopping está dentro da minha faixa de preço
# procurara esse produto no buscape
# verificar se algum dos produtos do buscape está dentro da minha faixa de preço
# salvar as ofertas boas em um dataframe( tabela )
# exportar pro excel
# enviar por e-mail o resultado da tabela


### FUNÇÕES  ####

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def busca_google_shopping(produto, termos_banidos, preco_minimo, preco_maximo):

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

    driver.get('https://www.google.com.br/')
    driver.find_element(
        By.     CLASS_NAME, "gLFyf").send_keys(produto)
    driver.find_element(
        By.     CLASS_NAME, "gLFyf").send_keys(Keys.ENTER)
    # listar todos os elementos que possuem o name_class hdtb-mitem;
    menu_google = driver.find_elements(By. CLASS_NAME, "hdtb-mitem")
    for menu in menu_google:
        if 'Shopping' in menu.text:
            menu.click()
            break

    # cabeçalho com todos os itens
    lista_resultados = driver.find_elements(
        By. CLASS_NAME, "sh-dgr__grid-result")

    lista_ofertas_google = []
    for produto in lista_resultados:  # for para repassar por cada item

        # aqui é possível utilizar o "produto" como método para find_element
        nome = produto.find_element(By. CLASS_NAME, 'tAxDx').text
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

        # se tem_termos_banidos = False
        # e o tem_todos_termos_produto = True
        if not tem_termos_banidos and tem_todos_termos_produto:
            try:
                preco = produto.find_element(By. CLASS_NAME, "a8Pemb").text
                preco = preco.replace("R$", "").replace(
                    " ", "").replace(".", "")
                preco = preco.replace(",", ".")
                preco = float(preco)

            # validar se o preco esta no min. and max.
                if not preco_minimo <= preco <= preco_maximo:
                    pass
                else:
                    # python parent - estrutura de árvore HTML
                    elemento_link = produto.find_element(
                        By. CLASS_NAME, "aULzUe")
                    elemento_pai = elemento_link.find_element(
                        By. XPATH, '..')  # cd ..
                    link = elemento_pai.get_attribute('href')

                    print(nome, preco, link)
                    # adiciona informações do elemento encontrado na tela a tabela excel
                    lista_ofertas_google.append((nome, preco, link))
                    print(lista_ofertas_google)
            except:
                continue
    return lista_ofertas_google


#################


# libs


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
##########################################


if __name__ == "__main__":
    # importando/visualizar a base de dados
    tabela_produtos = pd.read_excel(
        r'C:\PYTHON\Projeto AutomacaoWebPesquisaDePrecos\buscas.xlsx')
    print(tabela_produtos)
    # criar uma tabela vazia. Sempre que encontrar uma oferta, adiciona no DataFrame
    tabela_ofertas = pd.DataFrame()

    # percorrer pelas informações presentes na base de dados
    for linha in tabela_produtos.index:  # index = indices da tabela

        # tabela_produtos.loc[linha, coluna]

        #######################################################################
        produto = tabela_produtos.loc[linha, "Nome"]
        termos_banidos = tabela_produtos.loc[linha, "Termos banidos"]

        preco_minimo = tabela_produtos.loc[linha, "Preço mínimo"]
        preco_maximo = tabela_produtos.loc[linha, "Preço máximo"]

        #######################################################################

        # # pesquisa no Google Shopping
        lista_ofertas_google = busca_google_shopping(produto, termos_banidos,
                                                     preco_minimo, preco_maximo)

        if lista_ofertas_google:
            tabela_google_shopping = pd.DataFrame(lista_ofertas_google, columns=[
                                                  'produto', 'preco', 'link'])
            tabela_ofertas = tabela_ofertas.append(tabela_google_shopping)

        else:
            tabela_google_shopping = None

        # # # pesquisa no Busca Pé
        # lista_ofertas_buscape = busca_pe(
        #     produto, termos_banidos, preco_minimo, preco_maximo)
        # if lista_ofertas_buscape:
        #     tabela_buscape = pd.DataFrame(lista_ofertas_buscape, columns=[
        #                                   'produto', 'preco', 'link'])
        #     tabela_ofertas = tabela_ofertas.append(tabela_buscape)
        # else:
        #     tabela_buscape = None

    print(tabela_ofertas)
    print(type(lista_ofertas_google))

    # exportar para o excel

    tabela_ofertas = tabela_ofertas.reset_index(drop=True)
    tabela_ofertas.to_excel("Ofertas.xlsx", index=False)
