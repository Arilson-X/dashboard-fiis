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
        cotacao = st.slider('Cotação', 1.00,2000.00,(1.00,2000.00),10.00)
    with st.sidebar.expander('Faixa de FFO Yield'):
        ffo_yield = st.slider('FFO Yield', 0.00,30.00,(0.00,30.00),1.00)
    with st.sidebar.expander('Faixa de Dividend Yield'):
        dividend_yield = st.slider('Dividend Yield', 0.00,30.00,(0.00,30.00),1.00)
    with st.sidebar.expander('Faixa de P/VP'):
        p_vp = st.slider('P/VP', 0.00,3.00,(0.00,3.00),0.05)
    with st.sidebar.expander('Faixa Valor de Mercado'):
        valor_mercado = st.slider('Valor de Mercado',0,100000000000,(0,100000000000),10000000)
    with st.sidebar.expander('Faixa de Liquidez'):
        liquidez = st.slider('Liquidez',metricas["liquidez"][0],metricas["liquidez"][1],(metricas["liquidez"]),100000)
    with st.sidebar.expander('Faixa de Quantidade de Imóveis'):
        qtd_imoveis = st.slider('Quantidade de Imóveis',0,100,(0,100),1)
    with st.sidebar.expander('Faixa de Preço M2'):
        preco_m2 = st.slider('Preço M2',0,30000,(0,30000),500)
    with st.sidebar.expander('Faixa de Aluguel M2'):
        aluguel_m2 = st.slider('Aluguel M2',0,2000,(0,2000),100)
    with st.sidebar.expander('Faixa de Cap Rate'):
        cap_rate = st.slider('Cap Rate',0.00,30.00,(0.00,30.00),1.00)
    with st.sidebar.expander('Faixa de Vacância'):
        vacancia = st.slider('Vacância',0.00,100.00,(0.00,100.00),1.00)
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