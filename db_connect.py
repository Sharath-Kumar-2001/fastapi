from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(str(settings.DATABASE_URL))
def get_db_session():
    return sessionmaker(bind=engine)()
app = FastAPI()

@app.get("/health")
async def health_check():
    try:
        with get_db_session() as connection:
            connection.execute(text("SELECT 1")) 
            return "Database Connection successful!"
    except Exception as e:
        return "Database connection has error"