from sqlmodel import SQLModel, create_engine, Session

# Emplacement db
DATABASE_URL = "sqlite:///database.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    """Crée les tables dans la base à partir des modèles."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency FastAPI : fournit une session DB, fermée automatiquement après usage."""
    with Session(engine) as session:
        yield session