import streamlit as st
import plotly.express as px
import pandas as pd

def filter(papeis, segmentos, metricas):
    st.sidebar.title('Filtros')
    with st.sidebar.expander('Papeis'):
        papel = st.multiselect('Selecione os Papeis', papeis, papeis)
    with st.sidebar.expander('Segmentos'):
        segmento = st.multiselect('Segmentos', segmentos, segmentos)
    with st.sidebar.expander('Faixa de Cotação'):
        cotacao = st.slider('Cotação', metricas["cotacao"][0],metricas["cotacao"][1],(metricas["cotacao"]),20.00)
    with st.sidebar.expander('Faixa de FFO Yield'):
        ffo_yield = st.slider('FFO Yield', metricas["ffo_yield"][0],metricas["ffo_yield"][1],(metricas["ffo_yield"]),20.00)
    with st.sidebar.expander('Faixa de Dividend Yield'):
        dividend_yield = st.slider('Dividend Yield', metricas["dividend_yield"][0],metricas["dividend_yield"][1],(metricas["dividend_yield"]),1.00)
    with st.sidebar.expander('Faixa de P/VP'):
        p_vp = st.slider('P/VP', metricas["p_vp"][0],metricas["p_vp"][1],(metricas["p_vp"]),0.05)
    with st.sidebar.expander('Faixa Valor de Mercado'):
        valor_mercado = st.slider('Valor de Mercado',metricas["valor_mercado"][0],metricas["valor_mercado"][1],(metricas["valor_mercado"]),100000)
    with st.sidebar.expander('Faixa de Liquidez'):
        liquidez = st.slider('Liquidez',metricas["liquidez"][0],metricas["liquidez"][1],(metricas["liquidez"]),100000)
    with st.sidebar.expander('Faixa de Quantidade de Imóveis'):
        qtd_imoveis = st.slider('Quantidade de Imóveis',metricas["qtd_imoveis"][0],metricas["qtd_imoveis"][1],(metricas["qtd_imoveis"]),1)
    with st.sidebar.expander('Faixa de Preço M2'):
        preco_m2 = st.slider('Preço M2',metricas["preco_m2"][0],metricas["preco_m2"][1],(metricas["preco_m2"]),10)
    with st.sidebar.expander('Faixa de Aluguel M2'):
        aluguel_m2 = st.slider('Aluguel M2',metricas["aluguel_m2"][0],metricas["aluguel_m2"][1],(metricas["aluguel_m2"]),10)
    with st.sidebar.expander('Faixa de Cap Rate'):
        cap_rate = st.slider('Cap Rate',metricas["cap_rate"][0],metricas["cap_rate"][1],(metricas["cap_rate"]),10.00)
    with st.sidebar.expander('Faixa de Vacância'):
        vacancia = st.slider('Vacância',metricas["vacancia"][0],metricas["vacancia"][1],(metricas["vacancia"]),5.00)
    return {
        'Papel' : papel,
        'Segmento' : segmento,
        'Cotacao' : cotacao,
        'FFO Yield' : ffo_yield,
        'Dividend' : dividend_yield,
        'P/VP': p_vp,
        'Valor Mercado': valor_mercado,
        'Liquidez': liquidez,
        'Qtd Imoveis': qtd_imoveis,
        'Preco M2': preco_m2,
        'Aluguel M2': aluguel_m2,
        'Cap Rate': cap_rate,
        'Vacancia':vacancia
    }
def scatter_graph(df,x,y):
    fig = px.scatter(df,x=x,y=y,hover_data=['Papel','Segmento'])
    fig.update_layout(title=f'{x} x {y}')
    return fig

def boxplot_graph(df, y):
    fig = px.box(df, y=y)
    fig.update_layout(title=f'Distribuição de FII pela {y}')
    return fig

def histogram_graph(df,x):
    fig = px.histogram(df, x=x)
    fig.update_layout(title=f'Distribuição de FII pela {x}',
                      bargap=0.1)
    return fig