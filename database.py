import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.environ.get("POSTGRES_URL"))
session = sessionmaker(autoflush=False, autocommit=False,  bind=engine)
Base = declarative_base()
from models import * 
Base.metadata.create_all(bind=engine)