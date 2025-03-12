import sys
import streamlit as st
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from tools.login import verificar_senha

if 'id_usuario' not in st.session_state:
    st.session_state['id_usuario'] = None

pages = {
    "Funções":[
        st.Page('dashboard.py', title='Dashboard', icon='📊'),
        st.Page('lancar_movimentacao.py', title='Lançar Movimentação', icon='💸'),
        st.Page('listar_operacoes.py', title='Listar Operações', icon='📊')
    ],
    "Cadastros":[
        st.Page('cadastros_classes.py', title='Cadastros de Classes', icon='📋'),
        st.Page('cadastro_tipo_operacao.py', title='Cadastros de Tipo de Operação', icon='📋'),
    ]
}


if st.session_state['id_usuario']:

    pg = st.navigation(pages)
    pg.run()

    if st.sidebar.button('Logout'):
        st.session_state['id_usuario'] = None


else:
    st.write("## Login")
    email = st.text_input(label='E-mail')
    senha = st.text_input(label='Senha')

    if st.button('Entrar'):

        retorno_verificacao = verificar_senha(email, senha)

        if retorno_verificacao:
            st.session_state['id_usuario'] = retorno_verificacao
            st.rerun()
        
        else:
            st.error("Usuário ou senha inválidos.")