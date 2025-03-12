from db import get_supabase_client

supabase = get_supabase_client()

def verificar_senha(email, senha_informada):
    # Busca o hash armazenado pelo e-mail
    response = (
        supabase.table("usuarios")
        .select("senha")
        .eq("email", email)
        .execute()
    )

    if not response.data:
        return False

    hash_senha_armazenada = response.data[0]['senha']
    
    # Verifica a senha fornecida com a hash armazenada
    if senha_informada == hash_senha_armazenada:
        response = (
            supabase.table("usuarios")
            .select("id")
            .eq("email", email)
            .eq("senha", hash_senha_armazenada)
            .execute()
        )

        return response.data[0]['id']
    else:
        return False
