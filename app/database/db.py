from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

db_url = 'postgresql://postgres:1wprjenuxhskaRRlet@localhost/fast_insta'

engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()