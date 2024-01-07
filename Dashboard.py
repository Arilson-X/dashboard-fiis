from time import sleep
from io import StringIO
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import streamlit as st
import Components

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
    df_fiis = pd.read_html(StringIO(str_table),decimal=',')[0]

    return(df_fiis)

def formata_numero(valor, prefixo = '', porcentagem = False):
    if porcentagem:
        return f'{prefixo} {valor:.2f}%'
    else:
        for unidade in ['', 'mil']:
            if valor <1000:
                return f'{prefixo} {valor:.2f} {unidade}'
            valor /= 1000
        return f'{prefixo} {valor:.2f} milhões'

df_fiis = get_fiis()
df_fiis = formata_coluna(df_fiis)

# Parâmetros de Filtros
papeis = list(df_fiis['Papel'])
segmentos = list(df_fiis['Segmento'].unique())

# Métricas
max_Cotacao = df_fiis['Cotação'].max()
min_Cotacao = df_fiis['Cotação'].min()
max_FFO_yield = df_fiis['FFO Yield'].max()
min_FFO_yield = df_fiis['FFO Yield'].min()
max_Dividend_Yield = df_fiis['Dividend Yield'].max()
min_Dividend_Yield = df_fiis['Dividend Yield'].min()
max_P_VP = df_fiis['P/VP'].max()
min_P_VP = df_fiis['P/VP'].min()
max_Valor_Mercado = df_fiis['Valor de Mercado'].max()
min_Valor_Mercado = df_fiis['Valor de Mercado'].min()
max_liquidez = df_fiis['Liquidez'].max()
min_liquidez = df_fiis['Liquidez'].min()
max_Qtd_Imoveis = df_fiis['Qtd de imóveis'].max()
min_Qtd_Imoveis = df_fiis['Qtd de imóveis'].min()
max_Preco_m2 = df_fiis['Preço do m2'].max()
min_Preco_m2 = df_fiis['Preço do m2'].min()
max_Aluguel_m2 = df_fiis['Aluguel por m2'].max()
min_Aluguel_m2 = df_fiis['Aluguel por m2'].min()
max_Cap_Rate = df_fiis['Cap Rate'].max()
min_Cap_Rate = df_fiis['Cap Rate'].min()
max_Vacancia_Media = df_fiis['Vacância Média'].max()
min_Vacancia_Media = df_fiis['Vacância Média'].min()

metricas = {
    'cotacao':[min_Cotacao,max_Cotacao],
    'ffo_yield':[min_FFO_yield,max_FFO_yield],
    'dividend_yield':[min_Dividend_Yield,max_Dividend_Yield],
    'p_vp':[min_P_VP,max_P_VP],
    'valor_mercado':[min_Valor_Mercado,max_Valor_Mercado],
    'liquidez':[min_liquidez,max_liquidez],
    'qtd_imoveis':[min_Qtd_Imoveis,max_Qtd_Imoveis],
    'preco_m2':[min_Preco_m2,max_Preco_m2],
    'aluguel_m2':[min_Aluguel_m2,max_Aluguel_m2],
    'cap_rate':[min_Cap_Rate,max_Cap_Rate],
    'vacancia':[min_Vacancia_Media,max_Vacancia_Media]
}

number_columns = list(df_fiis.columns)
number_columns.remove('Papel')
number_columns.remove('Segmento')

# Estruturando Dashboard
st.set_page_config(page_icon="chart_with_upwards_trend",
                   layout="wide",
                   page_title="Dashboard FII's")

st.header("Dashboard de Fundos de Investimentos Imobiliários :chart_with_upwards_trend:",divider="blue")
st.markdown('> "Não faço isso pelo dinheiro. É a diversão de fazer dinheiro e vê-lo crescer" - Warren Buffet')
st.divider()
filtros = Components.filter(papeis,segmentos,metricas)

f_papel = filtros['Papel']
f_segmento = filtros['Segmento']
f_cotacao = filtros['Cotacao']
f_dividend = filtros['Dividend']
f_ffo_yield = filtros['FFO Yield']
f_p_vp = filtros['P/VP']
f_valor_mercado = filtros['Valor Mercado']
f_liquidez = filtros['Liquidez']
f_qtd_imoveis = filtros['Qtd Imoveis']
f_preco_m2 = filtros['Preco M2']
f_aluguel_m2 = filtros['Aluguel M2']
f_cap_rate = filtros['Cap Rate']
f_vacancia = filtros['Vacancia']

query = '''
Papel in @f_papel and \
Segmento in @f_segmento and \
@f_cotacao[0] <= `Cotação` <= @f_cotacao[1] and \
@f_dividend[0] <= `Dividend Yield` <= @f_dividend[1] and \
@f_ffo_yield[0] <= `FFO Yield` <= @f_ffo_yield[1] and \
@f_p_vp[0] <= `P/VP` <= @f_p_vp[1] and \
@f_valor_mercado[0] <= `Valor de Mercado` <= @f_valor_mercado[1] and \
@f_liquidez[0] <= `Liquidez` <= @f_liquidez[1] and \
@f_qtd_imoveis[0] <= `Qtd de imóveis` <= @f_qtd_imoveis[1] and \
@f_preco_m2[0] <= `Preço do m2` <= @f_preco_m2[1] and \
@f_aluguel_m2[0] <= `Aluguel por m2` <= @f_aluguel_m2[1] and \
@f_cap_rate[0] <= `Cap Rate` <= @f_cap_rate[1] and \
@f_vacancia[0] <= `Vacância Média` <= @f_vacancia[1]
'''

aba1, aba2, aba3 = st.tabs(['Métricas','Estatísticas','-----'])

dados_filtrados = df_fiis.query(query)
with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        col_1,col_2 = st.columns(2)
        with col_1:
            variavel_1 = st.selectbox('Variável x',number_columns)
        with col_2:   
            variavel_2 = st.selectbox('Variável y',number_columns)
        st.plotly_chart(Components.scatter_graph(dados_filtrados,variavel_1,variavel_2),use_container_width= True)
    with coluna2:
        variavel_3 = st.selectbox('Variável ',number_columns)
        st.plotly_chart(Components.boxplot_graph(dados_filtrados,variavel_3), use_container_width=True)

    variavel_4 = st.selectbox('Variável 3',number_columns)
    st.plotly_chart(Components.histogram_graph(dados_filtrados,variavel_4), use_container_width=True)

