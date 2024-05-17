from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Assuming you have SQLALCHEMY_DATABASE_URL defined somewhere
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://Earl:Earl0006@localhost:3306/computerlaboratory"  # Replace with your actual database URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()