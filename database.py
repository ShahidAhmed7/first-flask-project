import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pymysql

# Get the absolute path of the .env file
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent / ".env"

# Load environment variables
load_dotenv(dotenv_path)

# Get DB credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create Database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

def get_job_list():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))

        result_all = result.all()

        jobs_list = [dict(row._mapping) for row in result_all]
        return jobs_list
    
def get_job_data(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),{"val" : id})
        res = result.all()
        if len(res) == 0:
            return None 
        return dict(res[0]._mapping)

    


