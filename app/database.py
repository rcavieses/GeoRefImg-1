from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool, QueuePool
from app.config import settings

Base = declarative_base()

# Determinar si usamos pool de conexiones (Azure SQL) o no (SQLite)
use_connection_pool = settings.app_env != "development"

pool_config = {}
if use_connection_pool:
    # Configuración optimizada para Azure SQL con pymssql
    pool_config = {
        "poolclass": QueuePool,
        "pool_size": 3,
        "max_overflow": 5,
        "pool_pre_ping": True,
        "pool_recycle": 3600,  # Recicla conexiones cada hora
        "connect_args": {
            "timeout": 30,
            "login_timeout": 30,
            "charset": "utf8"
        }
    }
else:
    # SQLite no necesita pool
    pool_config = {"poolclass": NullPool}

# Crear engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    **pool_config
)

# Event listeners para mejor manejo de conexiones
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configurar SQLite en modo WAL para mejor concurrencia"""
    if settings.app_env == "development":
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Crear todas las tablas"""
    Base.metadata.create_all(bind=engine)
