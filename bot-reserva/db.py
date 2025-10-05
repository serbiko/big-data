# db.py
import psycopg2

def get_conn():
    return psycopg2.connect(
        host="localhost",   # se o bot rodar em container JUNTOS com o DB, use "postgres"
        port=5432,
        database="postgres",
        user="postgres",
        password="senha123",
    )

def salvar_conversa(usuario: str, mensagem: str) -> None:
    if not mensagem or not mensagem.strip():
        return
    if not usuario:
        usuario = "desconhecido"
    usuario = usuario[:100]
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO conversas (usuario, mensagem) VALUES (%s, %s)",
                (usuario, mensagem),
            )
    finally:
        conn.close()
