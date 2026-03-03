from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def migrate():
    """Dropa e recria as tabelas matches e match_events para garantir estrutura correta."""
    print("Atualizando estrutura do banco...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS match_events CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS matches CASCADE"))
        conn.commit()
    print("Tabelas matches/match_events removidas.")

    # Recria todas as tabelas (users ja existe, nao sera afetada)
    models.Base.metadata.create_all(bind=engine)
    print("Tabelas recriadas com sucesso.")

def init_db():
    db = SessionLocal()
    try:
        # Seed users
        seed_users = [
            {"email": "admin@admin.com", "password": "admin@123", "full_name": "Administrador", "role": "admin"},
            {"email": "mesario@mesario.com", "password": "mesario@123", "full_name": "Mesário Padrão", "role": "mesario"},
            {"email": "torcedor@torcedor.com", "password": "torcedor@123", "full_name": "Torcedor Padrão", "role": "pais"},
        ]

        for u in seed_users:
            existing = db.query(models.User).filter(models.User.email == u["email"]).first()
            if not existing:
                print(f"Criando usuario {u['role']}: {u['email']}...")
                db.add(models.User(
                    email=u["email"],
                    hashed_password=pwd_context.hash(u["password"]),
                    full_name=u["full_name"],
                    role=u["role"],
                    is_active=True,
                ))
                db.commit()
                print(f"  -> Criado.")
            else:
                print(f"{u['role']} existe: id={existing.id}, role={existing.role}")

        print("Banco inicializado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
    init_db()
