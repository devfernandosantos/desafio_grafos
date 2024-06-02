from pydantic import BaseModel
from typing import List

class NoBase(BaseModel):
    nome: str
    coordenada: str

class NoCreate(NoBase):
    pass

class NoResponse(NoBase):
    id: int

    class Config:
        orm_mode = True

class ArestaBase(BaseModel):
    no_origem_id: int
    no_destino_id: int
    linha: str

class ArestaCreate(ArestaBase):
    pass

class ArestaResponse(ArestaBase):
    id: int

    class Config:
        orm_mode = True

class GrafoBase(BaseModel):
    nome: str

class GrafoCreate(GrafoBase):
    nos: List[NoCreate]
    arestas: List[ArestaCreate]

class GrafoResponse(GrafoBase):
    id: int
    nos: List[NoResponse]
    arestas: List[ArestaResponse]

    class Config:
        orm_mode = True
