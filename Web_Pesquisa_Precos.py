
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


import pandas as pd
import undetected_chromedriver as uc

from script_busca_google import busca_google_shopping
from script_busca_pe import busca_pe

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
            print('AI SE QUER DE GRAÇA NEH?')
        # # pesquisa no Busca Pé
        lista_ofertas_buscape = busca_pe(
            produto, termos_banidos, preco_minimo, preco_maximo)
        if lista_ofertas_buscape:
            tabela_buscape = pd.DataFrame(lista_ofertas_buscape, columns=[
                                          'produto', 'preco', 'link'])
            tabela_ofertas = tabela_ofertas.append(tabela_buscape)
        else:
            tabela_buscape = None
            print('AI SE QUER DE GRAÇA NEH?')
    print(tabela_ofertas)
    print(type(lista_ofertas_google))

    # exportar para o excel

    tabela_ofertas = tabela_ofertas.reset_index(drop=True)
    tabela_ofertas.to_excel("Ofertas.xlsx", index=False)
