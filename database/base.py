import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


basedir = os.path.abspath(os.path.dirname(__name__))
URL = "sqlite:///" + basedir + "/bot_db.db"

engine = create_engine(URL)
Session = sessionmaker(bind=engine)
session = Session()
