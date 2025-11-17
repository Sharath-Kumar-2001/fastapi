from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

@app.get("/health")
async def health():
  return {"status": "ok"}

class AddResult(BaseModel):
  result: int

@app.get("/add", response_model=AddResult)
def add(a:int,b:int):
  c = a+b
  return {"result": c}

@app.get("/multiply", response_model=AddResult)
def multiply(a:int,b:int):
  c = a*b
  return {"result": c}

