import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
# libs
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
        By. XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(produto)
    driver.find_element(
        By. XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(Keys.ENTER)
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
        nome = produto.find_element(By. CLASS_NAME, 'Xjkr3b').text
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

                    # print(nome, preco, link)
                    lista_ofertas_google.append((nome, preco, link))

            except:
                continue
    return lista_ofertas_google
