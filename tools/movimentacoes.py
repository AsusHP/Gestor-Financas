from DB.connection import get_supabase_client

supabase = get_supabase_client()

def listar_movimentacoes_completas(usuario_id, data_inicial=None, data_final=None):
    """
    Retorna as movimentacoes do usuario dentro de um range de datas (opcional).

    data_inicial e data_final devem estar em formato 'YYYY-MM-DD' caso sejam fornecidas.
    Se não forem, listará todas as movimentações do usuário.
    """
    query = supabase.table("movimentacoes").select("id, descricao, valor, data, tipo_operacao(nome), classe(nome)").eq("usuario_id", usuario_id)

    if data_inicial and data_final:
        query = query.gte("data", data_inicial).lte("data", data_final)

    response = query.order("data").execute()

    return [
        (item['id'], item['descricao'], item['valor'], item['data'], item['tipo_operacao']['nome'], item['classe']['nome'])
        for item in response.data
    ]


def listar_movimentacoes(usuario_id, data_inicial, data_final):
    """
    Retorna as movimentações entre data_inicial e data_final (texto 'YYYY-MM-DD').
    Faz JOIN com tipo_operacao e classes, para exibir seus nomes.
    """
    response = (
        supabase.table("movimentacoes")
        .select("id, descricao, valor, data, tipo_operacao(nome), classe(nome)")
        .eq("usuario_id", usuario_id)
        .gte("data", data_inicial)
        .lte("data", data_final)
        .order("data")
        .execute()
    )
    return [
        (item['id'], item['descricao'], item['valor'], item['data'], item['tipo_operacao']['nome'], item['classe']['nome'])
        for item in response.data
    ]

def excluir_movimentacao(mov_id):
    """Exclui a movimentação pelo 'id'."""
    supabase.table("movimentacoes") \
        .delete() \
        .eq("id", mov_id) \
        .execute()

def gravar_movimentacao(descricao, valor, data, usuario_id, tipo_operacao, classe):
    """
    Grava uma movimentação na tabela 'movimentacoes'.

    :param descricao: Descrição da movimentação (str)
    :param valor: Valor da movimentação (float)
    :param data: Data da movimentação no formato 'YYYY-MM-DD' (str)
    :param usuario_id: ID do usuário associado (int)
    :param tipo_operacao: ID do tipo de operação (int)
    :param classe: ID da classe associada (int)
    """
    supabase.table("movimentacoes") \
        .insert({
            "descricao": descricao,
            "valor": valor,
            "data": data,
            "usuario_id": usuario_id,
            "tipo_operacao": tipo_operacao,
            "classe": classe
        }) \
        .execute()


