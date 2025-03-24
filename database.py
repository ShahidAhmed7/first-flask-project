import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
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
    
def add_user(user_type,name,username,email,password_hash):
    with engine.connect() as conn:
        trans = conn.begin()
        try : 
            conn.execute(text("INSERT INTO users (name,username,email,password_hash,user_type) VALUES (:name,:username,:email, :password_hash, :user_type)"),{'name' : name,'username':username,'email':email,'password_hash':password_hash,'user_type':user_type})
            trans.commit()
            return True
        except SQLAlchemyError as e: 
            print(f"Database Error: {e}") # ✅ Catch SQL Errors
            trans.rollback() # 🔄 Undo changes on failure             
            return False   

    
def get_user(username):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username})
        res = result.all()  # Fetch all results (it will return at most one row)
        
        if len(res) == 0:
            return None
        return dict(res[0]._mapping)  # Convert the first row to a dictionary

def delete_job_data(id):
    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(text("DELETE FROM jobs WHERE id = :val"),{"val" : id})
        trans.commit()

def add_job_data(title,salary,company,location,responsibilities,requirements,posted_by):
    with engine.connect() as conn:
        trans = conn.begin()
        try : 
            conn.execute(text("INSERT INTO jobs (title,salary,currency,company,location,responsibilities,requirements,posted_by) VALUES (:title,:salary,:currency, :company, :location, :responsibilities, :requirements, :posted_by)"),{'title' : title, 'salary' : salary, 'currency': 'BDT', 'company': company, 'location' : location, 'responsibilities': responsibilities, 'requirements': requirements, 'posted_by' : posted_by})
            trans.commit()
            return True
        except SQLAlchemyError as e: 
            print(f"Database Error: {e}") # ✅ Catch SQL Errors
            trans.rollback() # 🔄 Undo changes on failure             
            return False  