from fastapi import FastAPI
from routes import grafo_route

app = FastAPI()

app.include_router(grafo_route.router, prefix="/grafos", tags=["grafos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Grafo API"}
