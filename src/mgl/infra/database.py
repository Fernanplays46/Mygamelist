from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///mgl.db"

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
