from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.setting import setting


SQLALCHEMY_DATABASE_URL = setting.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    db = SessionLocal()
    try: 
        yield db 
    finally:
        db.close()