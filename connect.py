from sqlalchemy import create_engine

db_url = f"postgresql://postgres:bezhan2009@127.0.0.1:5432/postgres"
engine = create_engine(db_url, echo=False)
