from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
  return {"hello": "world deploy"}

@app.get("/health")
async def health():
  return {"status": "ok"}
