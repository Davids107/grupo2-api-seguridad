# Conexion a la base de datos - Persona 5.

# IMPORTANTE (segun lo pedido): el Grupo 1 todavia no entrega su esquema, asi que este archivo se deja SIMPLE, solo con lo minimo para que los demas puedan
# probar login/usuarios con datos de prueba. No se construye nada mas del lado de base de datos hasta que me pases los pasos/el esquema real.

# Cuando llegue el esquema del Grupo 1:
#  1. Cambiar DATABASE_URL en .env por la conexion real.
#  2. Poner USE_TEST_DATA=false.
#  3. Reemplazar el modelo Usuario de abajo por el modelo/tablas reales.

import os
from datetime import datetime, timezone

import bcrypt
from dotenv import load_dotenv
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
USE_TEST_DATA = os.getenv("USE_TEST_DATA", "true").lower() == "true"

# SQLite necesita este parametro extra para trabajar con varias peticiones a la vez.
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


# ---- Modelo Temporal, solo para probar login (Reemplazar despues) ----
class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nombre = Column(String(120), nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False, default="estudiante")
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    if not USE_TEST_DATA:
        return
    with SessionLocal() as db:
        if db.execute(select(Usuario.id).limit(1)).first():
            return
        db.add_all([
            Usuario(email="admin@example.com", nombre="Admin Prueba",
                    password_hash=hash_password("Admin123!"), rol="admin"),
            Usuario(email="docente@example.com", nombre="Docente Prueba",
                    password_hash=hash_password("Docente123!"), rol="docente"),
            Usuario(email="estudiante@example.com", nombre="Estudiante Prueba",
                    password_hash=hash_password("Estudiante123!"), rol="estudiante"),
        ])
        db.commit()
