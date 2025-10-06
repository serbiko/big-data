# db.py
import os
import json
from typing import Optional, Any, Dict

import psycopg2
from psycopg2.extras import RealDictCursor


# ====== Config por variáveis de ambiente (altere no Windows se quiser) ======
PG_HOST = os.getenv("POSTGRES_HOST", "localhost")   # se seu DB estiver em Docker junto do bot: "postgres"
PG_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
PG_DB   = os.getenv("POSTGRES_DB", "postgres")
PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "senha123")


def get_conn():
    """Abre uma conexão com o Postgres."""
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS,
    )


# ============================ Conversas ============================

def salvar_conversa(usuario: str, mensagem: Optional[str], payload: Optional[Dict[str, Any]] = None) -> None:
    """
    Salva uma linha em public.conversas (usuario, mensagem, data default now(), payload jsonb).
    Se sua tabela não tiver a coluna 'payload', o fallback tenta inserir só (usuario, mensagem).
    """
    # Não insere linhas vazias
    if (mensagem is None or not str(mensagem).strip()) and not payload:
        return

    if not usuario:
        usuario = "desconhecido"
    usuario = usuario[:100]

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO public.conversas (usuario, mensagem, payload) VALUES (%s, %s, %s)",
                    (usuario, mensagem, json.dumps(payload) if payload is not None else None),
                )
            except psycopg2.errors.UndefinedColumn:
                # Fallback caso payload não exista na tabela
                conn.rollback()
                cur.execute(
                    "INSERT INTO public.conversas (usuario, mensagem) VALUES (%s, %s)",
                    (usuario, mensagem),
                )
    finally:
        conn.close()


# ============================ Reservas ============================

def criar_reserva(
    reserva_id: str,
    passageiro: str,
    origem: str,
    destino: str,
    data_hora: Optional[str],   # pode ser None ou string 'YYYY-MM-DD HH:MM:SS'
    localizador: str,
    valor: Optional[float],
    status: str,
) -> None:
    """
    Cria uma reserva (INSERT). Usa ON CONFLICT DO NOTHING para não quebrar se já existir o mesmo id.
    """
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO public.reservas
                    (id, passageiro, origem, destino, data_hora, localizador, valor, status)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (reserva_id, passageiro, origem, destino, data_hora, localizador, valor, status),
            )
    finally:
        conn.close()


def get_reserva(reserva_id: str) -> Optional[Dict[str, Any]]:
    """
    Busca uma reserva por id. Retorna dict com colunas:
    id, passageiro, origem, destino, data_hora, localizador, valor, status
    ou None se não encontrar.
    """
    conn = get_conn()
    try:
        with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, passageiro, origem, destino, data_hora, localizador, valor, status
                FROM public.reservas
                WHERE id = %s
                """,
                (reserva_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()


def cancelar_reserva(reserva_id: str) -> bool:
    """
    Atualiza o status para 'Cancelada' se ainda não estiver cancelada.
    Retorna True se atualizou alguma linha (ou seja, existia e mudou).
    """
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE public.reservas SET status = 'Cancelada' WHERE id = %s AND status <> 'Cancelada'",
                (reserva_id,),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def status_reserva(reserva_id: str) -> Optional[str]:
    """
    Retorna o status (string) da reserva, ou None se não existir.
    """
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("SELECT status FROM public.reservas WHERE id = %s", (reserva_id,))
            row = cur.fetchone()
            return row[0] if row else None
    finally:
        conn.close()
