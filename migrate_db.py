"""
Script para adicionar colunas faltantes nas tabelas do banco.
Rode uma vez: python migrate_db.py
"""
from sqlalchemy import text
from database import engine

migrations = [
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS home_score INTEGER DEFAULT 0",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS away_score INTEGER DEFAULT 0",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)",
    "ALTER TABLE matches ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'agendado'",
]

with engine.connect() as conn:
    for sql in migrations:
        try:
            conn.execute(text(sql))
            print(f"OK: {sql}")
        except Exception as e:
            print(f"SKIP: {sql} -> {e}")
    conn.commit()

print("\nMigração concluída!")
