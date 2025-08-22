import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mssql+pyodbc://user:password@localhost/BizManager?driver=ODBC+Driver+17+for+SQL+Server")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
