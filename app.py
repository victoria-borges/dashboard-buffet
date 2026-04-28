import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Criativa Buffet",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Título
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎉 Criativa Buffet</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Dashboard de Gestão de Eventos</h4>", unsafe_allow_html=True)

# Carregar dados
url = "https://docs.google.com/spreadsheets/d/187qy-6aS8pkUpgtJ6n5GvHIfutpRHgwfh8xqYtuFMNw/export?format=csv"

df = pd.read_csv(url)
df = df.dropna(how='all')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df['data_evento'] = pd.to_datetime(df['data_evento'], dayfirst=True)

# Criar coluna de lucro
df['lucro'] = df['valor_total'] - df['custo_estimado']

# Filtros
st.sidebar.markdown("## 🔎 Filtros Inteligentes")
st.sidebar.markdown("---")

tema = st.sidebar.multiselect(
    "Selecione o Tema:",
    options=df['tema'].unique(),
    default=df['tema'].unique()
)

df_filtrado = df[df['tema'].isin(tema)].copy()

# KPIs (indicadores)
st.markdown("### 📊 Indicadores Principais")
total_faturamento = df_filtrado['valor_total'].sum()
total_lucro = df_filtrado['lucro'].sum()
total_eventos = df_filtrado.shape[0]
ticket_medio = df_filtrado['valor_total'].mean()

# Criar colunas na tela
col1, col2, col3, col4 = st.columns(4)

# Mostrar indicadores
col1.metric("💰 Faturamento Total", f"R$ {total_faturamento:,.2f}")
col2.metric("📈 Lucro Total", f"R$ {total_lucro:,.2f}")
col3.metric("🎂 Eventos", total_eventos)
col4.metric("🧾 Ticket Médio", f"R$ {ticket_medio:,.2f}")
st.markdown("---")

# Gráficos

# Faturamento por mês
df_filtrado['mes'] = df_filtrado['data_evento'].dt.month
faturamento_mes = df_filtrado.groupby('mes', as_index=False)['valor_total'].sum()
faturamento_mes.columns = ['Mês', 'Faturamento']

st.subheader("📊 Faturamento por Mês")

fig_faturamento = px.bar(
    faturamento_mes,
    x='Mês',
    y='Faturamento',
    text='Faturamento'
)

fig_faturamento.update_traces(
    texttemplate='R$ %{text:,.2f}',
    textposition='outside'
)

fig_faturamento.update_layout(
    xaxis_tickangle=0,
    xaxis=dict(tickmode='linear'),
    yaxis_title="Faturamento",
    xaxis_title="Mês"
)

st.plotly_chart(fig_faturamento, use_container_width=True)

st.markdown("---")

# Temas mais vendidos
temas = df_filtrado['tema'].value_counts().reset_index()
temas.columns = ['Tema', 'Quantidade']

st.subheader("🎉 Temas Mais Vendidos")

fig_temas = px.bar(
    temas,
    x='Tema',
    y='Quantidade',
    text=None
)

fig_temas.update_traces(
    textposition='inside'
)

fig_temas.update_layout(
    xaxis_tickangle=0,
    yaxis_title="Quantidade",
    xaxis_title="Tema"
)

st.plotly_chart(fig_temas, use_container_width=True)

st.markdown("---")

# Criar cópia para exibição
df_exibir = df_filtrado.copy()
df_exibir.index = df_exibir.index + 1

# Formatando data
df_exibir['data_evento'] = df_exibir['data_evento'].dt.strftime('%d/%m/%Y')

# Formatando valor
df_exibir['valor_total'] = df_exibir['valor_total'].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)
# Mostrar tabela
st.markdown("## 📋 Dados dos Eventos")
st.dataframe(df_exibir, use_container_width=True)

# RODAPÉ
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Criativa Buffet © 2026 | Projeto de Análise de Dados</p>",
    unsafe_allow_html=True
)
