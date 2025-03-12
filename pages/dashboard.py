import streamlit as st
import pandas as pd
import datetime
from tools import listar_movimentacoes_completas

st.set_page_config(layout="wide")

st.title("Dashboard de Gastos")

# Exemplo: usuário logado = 1 (pode vir de sessão ou login real)
usuario_id = st.session_state['id_usuario']

datas = st.date_input(
    "Selecione o intervalo de datas (início e fim)",
    value=(datetime.date.today().replace(day=1), datetime.date.today()),
    format="DD/MM/YYYY"
)

try:
    data_inicial, data_final = datas
    # Convertemos para string no formato YYYY-MM-DD (SQLite-friendly)
    data_inicial_str = data_inicial.strftime("%Y-%m-%d")
    data_final_str = data_final.strftime("%Y-%m-%d")
except ValueError:
    st.warning("Selecione duas datas (início e fim).")

# Botão para atualizar o filtro
if st.button("Atualizar Dashboard"):
    dados = listar_movimentacoes_completas(usuario_id, data_inicial_str, data_final_str)

    # Se não vier nada, exibir mensagem
    if not dados:
        st.warning("Nenhuma movimentação encontrada neste período.")

    # Converte a lista de tuplas em um DataFrame pandas
    df = pd.DataFrame(dados, columns=[
        "id",
        "descricao",
        "valor",
        "data",
        "tipo_operacao",
        "classe"
    ])

    # ================== KPIs ================== #

    df_saidas = df[df['tipo_operacao'] == 'Saida']

    total_entradas = df[df['tipo_operacao'] == 'Entrada']["valor"].sum()
    total_gasto = df_saidas["valor"].sum()
    lucro = total_entradas - total_gasto
    qtd_saidas = df[df['tipo_operacao'] == 'Saida'].shape[0]

    media_gastos = 0 if qtd_saidas==0 else total_gasto/qtd_saidas

    # Exibindo KPIs lado a lado
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    kpi_col1.metric("Total Entradas", f"R$ {total_entradas:,.2f}")
    kpi_col2.metric("Total Gasto", f"R$ {total_gasto:,.2f}")
    kpi_col3.metric("Lucro", f"R$ {lucro:,.2f}")
    kpi_col4.metric("Média de Gastos", f"R$ {media_gastos:,.2f}")

    st.divider()  # linha separadora (Streamlit 1.20+)

    # ================== GRÁFICOS ================== #

    # 1) Gasto por Classe
    df_classe = df_saidas.groupby("classe")["valor"].sum().reset_index()
    st.subheader("Gastos por Classe")
    st.bar_chart(data=df_classe, x="classe", y="valor")

    # 2) Gasto por Tipo de Operação
    df_tipo = df_saidas.groupby("tipo_operacao")["valor"].sum().reset_index()
    st.subheader("Gastos por Tipo de Operação")
    st.bar_chart(data=df_tipo, x="tipo_operacao", y="valor")

    # 3) Evolução de Gastos ao Longo do Tempo (se quiser ver por data)
    # Convertendo "data" para datetime (pandas) para agrupar por dia
    df["data"] = pd.to_datetime(df_saidas["data"], format="%Y-%m-%d", errors="coerce")
    df_data = df.groupby("data")["valor"].sum().reset_index()
    df_data = df_data.sort_values("data")  # Garante ordenação ascendente

    st.subheader("Evolução dos Gastos (Linha do Tempo)")
    st.line_chart(data=df_data, x="data", y="valor")

    # Exibe a tabela final (opcional)
    st.subheader("Detalhes das Movimentações")
    st.dataframe(df, use_container_width=True)
