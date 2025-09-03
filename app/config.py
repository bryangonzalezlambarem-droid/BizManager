import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = "supersecreto"  
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://sa:Te-lambaremb29@localhost\\SQLEXPRESS/BizManager?driver=ODBC+Driver+17+for+SQL+Server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
