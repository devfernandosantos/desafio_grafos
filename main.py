from fastapi import FastAPI
from routes import grafo_route
from config.database import engine, Base

app = FastAPI(
    title="Graph API",
    description="API para gerenciar grafos e rotas entre nós.",
    version="1.0.0"
)

app.include_router(grafo_route.router, prefix="/grafos", tags=["grafos"])
