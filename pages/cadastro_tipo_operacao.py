import streamlit as st
import sys
import streamlit as st
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from tools.tipo_operacao import inserir_tipo_operacao, listar_tipo_operacao, atualizar_tipo_operacao, deletar_tipo_operacao

st.title("Gestão de Tipo de Operação de Gastos (Categorias)")

usuario_id = st.session_state['id_usuario']

st.subheader("Cadastro de Tipo de Operação de Gastos")

# Campo de texto para inserir nova tipo_operacao
nome_nova_tipo_operacao = st.text_input("Nome do novo Tipo de Operação")

if st.button("Cadastrar"):
    if nome_nova_tipo_operacao.strip():
        inserir_tipo_operacao(nome_nova_tipo_operacao.strip(), usuario_id)
        st.success(f"tipo_operacao '{nome_nova_tipo_operacao}' cadastrada!")
        st.rerun()
    else:
        st.warning("Digite um nome válido para o Tipo de Operação.")

st.write("---")

st.subheader("Alterar ou Excluir Tipo de Operação")

# Carrega as tipo_operacao existentes
tipo_operacao_existentes = listar_tipo_operacao(usuario_id)

# Cria um dicionário {nome: id} para exibir no selectbox
opcoes = {f"{c[1]} (ID: {c[0]})": c[0] for c in tipo_operacao_existentes}

if opcoes:
    tipo_operacao_selecionada = st.selectbox("Selecione a tipo_operacao", list(opcoes.keys()))
    tipo_operacao_id_selecionada = opcoes[tipo_operacao_selecionada]

    # Text input para alterar o nome
    novo_nome = st.text_input("Novo nome", value=tipo_operacao_selecionada.split(" (ID:")[0])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Alterar Tipo de Operação"):
            if novo_nome.strip():
                atualizar_tipo_operacao(tipo_operacao_id_selecionada, novo_nome.strip())
                st.rerun()
            else:
                st.warning("Digite um nome válido para o Tipo de Operação.")

    with col2:
        if st.button("Excluir Tipo de Operação"):
            deletar_tipo_operacao(tipo_operacao_id_selecionada)
            st.rerun()
else:
    st.info("Não há Tipo de Operação cadastradas ainda.")