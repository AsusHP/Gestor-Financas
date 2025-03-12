import streamlit as st
import datetime
from tools import listar_movimentacoes, excluir_movimentacao

# 1) Título do app
st.title("Filtrar e Excluir Movimentações")

# 2) Supõe que você já obteve o usuario_id após login
usuario_id = st.session_state.get("id_usuario", 1)  # ou defina um valor default qualquer

# 3) Seleção de intervalo de datas
datas = st.date_input(
    "Selecione o intervalo de datas (início e fim)",
    value=(datetime.date.today().replace(day=1), datetime.date.today()),
    format="DD/MM/YYYY"
)

if len(datas) < 2:
    st.warning("Selecione duas datas (início e fim).")
    st.stop()

data_inicial, data_final = datas
data_inicial_str = data_inicial.strftime("%Y-%m-%d")
data_final_str = data_final.strftime("%Y-%m-%d")

# 4) Se não existir 'resultados' no session_state, inicializa com None
if 'resultados' not in st.session_state:
    st.session_state['resultados'] = None

# 5) Botão para buscar/atualizar a lista
if st.button("Filtrar Movimentações"):
    st.session_state['resultados'] = listar_movimentacoes(usuario_id, data_inicial_str, data_final_str)

# 6) Exiba os resultados mesmo fora do IF do botão
resultado_consulta = st.session_state['resultados']  # apenas para facilitar leitura

if resultado_consulta:
    st.write(f"Encontradas {len(resultado_consulta)} movimentações nesse intervalo:")

    # Loop para cada item
    for item in resultado_consulta:
        mov_id, descricao, valor, data_str, tipo_nome, classe_nome = item

        st.write(
            f"**ID**: {mov_id} | **Data**: {data_str or '-'} | "
            f"**Descrição**: {descricao or '-'} | **Valor**: R$ {valor:.2f} | "
            f"**Classe**: {classe_nome or '-'} | **Tipo**: {tipo_nome or '-'}"
        )

        # Botão Excluir fora do "if st.button('Filtrar ...')"
        if st.button("Excluir", key=f"excluir_{mov_id}"):
            excluir_movimentacao(mov_id)
            st.success(f"Movimentação ID={mov_id} excluída!")
            # Força recarregar a página para recarregar o banco de dados e remover o item
            st.session_state['resultados'] = [
                r for r in st.session_state['resultados'] if r[0] != mov_id
            ]
            st.rerun()
else:
    st.info("Nenhuma movimentação encontrada ou ainda não filtrada.")
