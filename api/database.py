# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), ".env")
# load_dotenv(dotenv_path)

# engine = create_engine(
#     os.getenv('SQLAlCHEMY_DATABASE_URL', "sqlite:///./vt.db"), connect_args={"check_same_thread": False, "timeout": 15}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()