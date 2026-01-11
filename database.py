from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# CHANGE username, password, host if needed
DATABASE_URL = "mysql+mysqlconnector://root:Vaishnavi%4016@localhost:3306/product_catalog"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
