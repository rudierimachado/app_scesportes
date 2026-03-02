from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from passlib.context import CryptContext

# Create all tables
models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    db = SessionLocal()
    try:
        # Check if admin exists
        user = db.query(models.User).filter(models.User.email == "admin@admin.com").first()
        if not user:
            print("Creating default admin user...")
            hashed_password = pwd_context.hash("admin@123")
            admin_user = models.User(
                email="admin@admin.com",
                hashed_password=hashed_password,
                full_name="Administrador",
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
            
        print("Database initialized successfully with PostgreSQL!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
