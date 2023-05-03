from sqlmodel import Session, SQLModel, create_engine

from app.settings import settings

engine = create_engine(f"{settings.db_url}/{settings.db_name}")
SQLModel.metadata.bind = engine
SQLModel.metadata.create_all()

db_session = Session(engine)
