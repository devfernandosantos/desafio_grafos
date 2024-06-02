from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from crud import grafo_crud
from schemas.grafo_schema import GrafoCreate, GrafoResponse, GrafoUpdate
from config.database import get_db
from fastapi.responses import JSONResponse
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=GrafoResponse)
def create_grafo(grafo: GrafoCreate, db: Session = Depends(get_db)):
    response = grafo_crud.create_grafo(db, grafo)
    return JSONResponse(content=response)

@router.get("/{grafo_id}", response_model=GrafoResponse)
def read_grafo(grafo_id: UUID, db: Session = Depends(get_db)):
    db_grafo = grafo_crud.get_grafo(db, grafo_id)
    if db_grafo is None:
        raise HTTPException(status_code=404, detail="Grafo não encontrado")
    return JSONResponse(content=db_grafo)

@router.get("/", response_model=list[GrafoResponse])
def read_grafos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grafos = grafo_crud.get_all_grafos(db, skip=skip, limit=limit)
    return JSONResponse(content=grafos)

@router.patch("/{grafo_id}", response_model=GrafoResponse)
def update_grafo(grafo_id: UUID, grafo: GrafoUpdate, db: Session = Depends(get_db)):
    db_grafo = grafo_crud.update_grafo(db, grafo_id, grafo)
    if db_grafo is None:
        raise HTTPException(status_code=404, detail="Grafo não encontrado")
    return JSONResponse(content=db_grafo)

@router.delete("/{grafo_id}", status_code=204)
def delete_grafo(grafo_id: UUID, db: Session = Depends(get_db)):
    db_grafo = grafo_crud.get_grafo(db, grafo_id)
    if db_grafo is None:
        raise HTTPException(status_code=404, detail="Grafo não encontrado")
    grafo_crud.delete_grafo(db, grafo_id)
    return Response(status_code=204)
