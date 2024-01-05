from time import sleep
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

# Define a url inicial onde será coletado os dados
url = 'https://www.fundamentus.com.br/fii_resultado.php'
# Define os header para o acesso do WebDriver
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

def trata_html(input):
    """ 
    Formata o texto do html, removendo os espaços
    Args:
        input (string): Objeto string com as informações de uma pagina com a marcação html
    Returns:
        string: O objeto de entrada formatado no padrão ISO-8859-1
    """
    input = input.decode('ISO-8859-1')
    return " ".join(input.split()).replace('> <', '><')


def formata_coluna(df_init):
    """ 
    Formata as colunas do dataframe dividindo por 100

    Esta função recebe o dataframe e faz o tratamento para que algumas de suas colunas sejam
    divididas por 100 para que estejam na unidade correta.
    Args:
        input (Dataframe): Objeto Dataframe do Pandas com as informações de FII's
    Returns:
        Dataframe: Objeto Dataframe do Pandas com as colunas convertidas para a unidade correta
    """
    df = df_init
    df['Cotação'] = df['Cotação']/100
    df['FFO Yield'] = df['FFO Yield']/100
    df['Dividend Yield'] = df['Dividend Yield']/100
    df['P/VP'] = df['P/VP']/100
    df['Cap Rate'] = df['Cap Rate']/100
    df['Vacância Média'] = df['Vacância Média']/100

    return df

def replace_dataframe(df_init):
    """ 
    Formata as colunas do dataframe trocando alguns valores incoerentes

    Esta função recebe o dataframe e faz o tratamento para que em algumas de suas colunas sejam
    feito o tratamento removendo ou substituido caracteres especiais, segue abaixo as trocas:
        '%' por ''
        '-' por '0'
        '.' por ''
        ',' por '.'
    Args:
        input (Dataframe): Objeto Dataframe do Pandas com as informações de FII's
    Returns:
        Dataframe: Objeto Dataframe do Pandas com as colunas com caracteres substituidos
    """
    lista_colunas = [
    'Min 52 sem',
    'Max 52 sem', 
    'Vol Medio em 2 meses',
    'FFO Cota',
    'Dividendo/Cota',
    'VP/Cota',
    'Resultado 3m Receita',
    'Resultado 3m Venda Ativos',
    'Resultado 3m FFO',
    'Resultado 3m Rend.Ditribuida',
    'Resultado 12m Receita',
    'Resultado 12m Venda Ativos',
    'Resultado 12m FFO',
    'Resultado 12m Rend.Ditribuida',
    'Ativos',
    'Patrimonio Liquido',
    'Imoveis/Pl do fii',
    'Area m2',
    'Taxa de Admin. sobre PL',
    'Taxa de Admin. sobre Vl.Mercado']

    df = df_init
    for coluna in lista_colunas:
        df[coluna] = df[coluna].str.replace('%', '')
        df[coluna] = df[coluna].str.replace('-', '0')
        df[coluna] = df[coluna].str.replace('.', '')
        df[coluna] = df[coluna].str.replace(',', '.').astype(float)

    return df

def get_fiis():
    """ 
    Busca a informação dos Fundos de Investimento Imobiliário

    Esta função é a responsável por acessar o site www.fundamentus.com.br e coletar as informações iniciais
    da tabela de fundos imobiliários e convertando para um dataframe do Python

    Returns:
        Dataframe: Objeto Dataframe do Pandas com as informações dos FII's
    """
    try:
        req = Request(url, headers = headers)
        response = urlopen(req)
        html = response.read()
        
    except HTTPError as e:
        print(e.status, e.reason)
        
    except URLError as e:
        print(e.reason)
    
    html = trata_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll('table')
    str_table = str(table)
    str_table = str_table.replace("%","")
    str_table = str_table.replace(".","")
    df_fiis = pd.read_html(str_table,decimal=',')[0]

    return(df_fiis)

df_fiis = get_fiis()
df_fiis = formata_coluna(df_fiis)