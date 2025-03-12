import streamlit as st
from tools import inserir_classe, listar_classes, atualizar_classe, deletar_classe

st.title("Gestão de Classes de Gastos (Categorias)")

usuario_id = st.session_state['id_usuario']

st.subheader("Cadastro de Classes de Gastos")

# Campo de texto para inserir nova classe
nome_nova_classe = st.text_input("Nome da nova classe")

if st.button("Cadastrar"):
    if nome_nova_classe.strip():
        inserir_classe(nome_nova_classe.strip(), usuario_id)
        st.success(f"Classe '{nome_nova_classe}' cadastrada!")
        st.rerun()
    else:
        st.warning("Digite um nome válido para a classe.")

st.write("---")

st.subheader("Alterar ou Excluir Classes")

# Carrega as classes existentes
classes_existentes = listar_classes(usuario_id)

# Cria um dicionário {nome: id} para exibir no selectbox
opcoes = {f"{c[1]} (ID: {c[0]})": c[0] for c in classes_existentes}

if opcoes:
    classe_selecionada = st.selectbox("Selecione a classe", list(opcoes.keys()))
    classe_id_selecionada = opcoes[classe_selecionada]

    # Text input para alterar o nome
    novo_nome = st.text_input("Novo nome", value=classe_selecionada.split(" (ID:")[0])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Alterar Classe"):
            if novo_nome.strip():
                atualizar_classe(classe_id_selecionada, novo_nome.strip())
                st.rerun()
            else:
                st.warning("Digite um nome válido para a classe.")

    with col2:
        if st.button("Excluir Classe"):
            deletar_classe(classe_id_selecionada)
            st.rerun()
else:
    st.info("Não há classes cadastradas ainda.")