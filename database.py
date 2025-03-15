from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Corrected the engine typo
engine = create_engine("postgresql+psycopg2://postgres:SuperAman1234@localhost/person",echo=True)

Base = declarative_base()

# Corrected the typo in sessionlocal binding
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
    