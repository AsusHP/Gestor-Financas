from typing import List, Tuple
from db import get_supabase_client

supabase = get_supabase_client()

def listar_tipo_operacao(usuario_id: int) -> List[Tuple[int, str]]:
    response = (
        supabase.table("tipo_operacao")
        .select("id, nome")
        .eq("usuario_id", usuario_id)
        .execute()
    )
    return [(item['id'], item['nome']) for item in response.data]

def inserir_tipo_operacao(nome, usuario_id):
    response = (
        supabase.table("tipo_operacao")
        .insert({"nome": nome, "usuario_id": usuario_id})
        .execute()
    )
    return response.data

def atualizar_tipo_operacao(tipo_operacao_id, novo_nome):
    response = (
        supabase.table("tipo_operacao")
        .update({"nome": novo_nome})
        .eq("id", tipo_operacao_id)
        .execute()
    )
    return response.data

def deletar_tipo_operacao(tipo_operacao_id):
    response = (
        supabase.table("tipo_operacao")
        .delete()
        .eq("id", tipo_operacao_id)
        .execute()
    )
    return response.data