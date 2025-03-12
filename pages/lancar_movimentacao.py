from dotenv import load_dotenv
import time
import streamlit as st

from tools import gravar_movimentacao, listar_classes, inserir_classe, gerar_classificacao, listar_tipo_operacao

load_dotenv()

usuario_id = st.session_state['id_usuario']

@st.dialog("Aceita a sugestão de classe?")
def sugestao_classe(classe_sugerida):
	st.write(f"A classe sugerida foi: {classe_sugerida}")

	col1, col2 = st.columns([0.5, 0.5])

	with col1:
		if st.button("Sim"):
			
			inserir_classe(classe_sugerida, usuario_id)
			atualizar_classes()
			st.session_state.classe_gastos = next(key for key, value in st.session_state.lista_classe.items() if value == classe_sugerida)
			
			st.rerun()
	with col2:
		if st.button("Não"):
			st.rerun()

	st.markdown("---")
	nova_classe = st.text_input("Nova classe", key='nova_classe')

	if st.button("Gravar nova classe"):
		inserir_classe(nova_classe, usuario_id)

		atualizar_classes()

		st.session_state.classe_gastos = next(key for key, value in st.session_state.lista_classe.items() if value == nova_classe)
		st.rerun()


def atualizar_classes():
	st.session_state.lista_classe = dict(listar_classes(usuario_id))

tipo_movimentacao = dict(listar_tipo_operacao(usuario_id))

if 'lista_classe' not in st.session_state: 
	st.session_state.lista_classe = dict(listar_classes(usuario_id))

st.write("## Lançamentos de Gastos")

data = st.date_input(label='Data do gasto', format="DD/MM/YYYY")

col1, col2, col3 = st.columns(3)

with col1:
	input_tipo = st.selectbox('Tipo', list(tipo_movimentacao.keys()), format_func=lambda x: tipo_movimentacao[x], key='tipo_gastos')

with col2:
	valor = st.number_input(label='Valor')
	
with col3:
	input_classe = st.selectbox('Classe', list(st.session_state.lista_classe.keys()), index = None, placeholder='', format_func=lambda x: st.session_state.lista_classe[x], key='classe_gastos')

descricao = st.text_input(label='Descrição do gasto', key='descricao_gastos')

if st.button('Gravar'):
	if not input_classe:
		classe_sugerida = gerar_classificacao(descricao, tipo_movimentacao[st.session_state.tipo_gastos], usuario_id)

		sugestao_classe(classe_sugerida)
	
	else:

		gravar_movimentacao(descricao, valor, str(data), usuario_id, input_tipo, input_classe)

		st.success('Gasto gravado com sucesso!')

		time.sleep(1)

		st.rerun()