from sqlmodel import SQLModel, Session, create_engine
from models import Review
DATABASE_URL = "sqlite:///REVIEWAPI.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_table():
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created")
    
def get_session():
    """Dependency that provides a database session per request"""
    
    with Session(engine) as session:
        yield session