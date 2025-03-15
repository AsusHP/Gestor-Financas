from typing import List, Tuple
from db import get_supabase_client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

supabase = get_supabase_client()

def listar_classes(usuario_id: int) -> List[Tuple[int, str]]:
    response = (
        supabase
        .table("classes")
        .select("*")
        .eq("usuario_id", usuario_id)
        .execute()
    )
    return [(item['id'], item['nome']) for item in response.data]

def inserir_classe(nome: str, usuario_id: int):

    classes_atuais = listar_classes(usuario_id)
    if nome not in [classe[1] for classe in classes_atuais]:

        supabase.table("classes") \
            .insert({"nome": nome, "usuario_id": usuario_id}) \
            .execute()

def atualizar_classe(classe_id, novo_nome):
    supabase.table("classes") \
        .update({"nome": novo_nome}) \
        .eq("id", classe_id) \
        .execute()
    
def deletar_classe(classe_id):
    supabase.table("classes") \
        .delete() \
        .eq("id", classe_id) \
        .execute()

def gerar_classificacao(descricao: str, tipo_movimentacao: str, usuario_id: int) -> str:
     
	client = OpenAI()
	 
	classes_atuais = [classe[1] for classe in listar_classes(usuario_id)]
	
	response = (
		supabase
		.table("movimentacoes")
		.select("descricao, tipo_operacao(nome), classe(nome)")
		.eq("usuario_id", usuario_id)
		.execute()
	)

	resultados = "\n\n".join([f"Descricao: {item['descricao']}\nTipo: {item['tipo_operacao']['nome']}\nCategoria: {item['classe']['nome']}" for item in response.data])

	system_prompt = f"""
	Você é um assistente de classificação de gastos pessoais, sua função é axiliar na classificação de um gasto, a partir da sua descrição.

	Caso a descrição seja de uma categoria que não existe, você deve criar uma nova categoria.

	## A nova categoria deve:
	- ter um nome breve e explicativo

	## Resposta
	- Responda apenas com a categoria, sem nenhum outro texto

	## As categorias já cadastradas são:
	{classes_atuais}

	## Outras classificações:
	{resultados}
	"""

	query = f"""Descricao: {descricao}
	Tipo: {tipo_movimentacao}
	Categoria: ?"""

	completion = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[
				{ "role": "system", "content": system_prompt },
			{"role": "user",
			"content": query
		}]
	)
	
	return completion.choices[0].message.content
