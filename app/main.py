from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.base import Base
from app.core.router import api_router
from app.core.exceptions import AppError
from app.core.exception_handlers import app_exception_handler

from app.db.session import get_db_session

app = FastAPI()

app.include_router(api_router)
app.add_exception_handler(AppError, app_exception_handler)




@app.get("/")
async def read_root():
  return {"message": "Привет, мир!"}

@app.get("/db-check")
async def get_one(session: AsyncSession = Depends(get_db_session)):
  result = await session.execute(text("SELECT 1"))
  return {"RESULT": result.scalar()}

@app.get("/tables")
async def get_tables():
  return list(Base.metadata.tables.keys())