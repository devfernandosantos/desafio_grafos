from pydantic import BaseModel
from typing import List, Tuple, Optional, Union
from uuid import UUID

class NoBase(BaseModel):
    nome: str
    coordenada: Tuple[float, float]

class NoCreate(NoBase):
    pass

class NoResponse(NoBase):
    id: UUID

    class Config:
        orm_mode = True

class ArestaBase(BaseModel):
    no_origem_id: str
    no_destino_id: str
    linha: List[Tuple[float, float]]

class ArestaCreate(ArestaBase):
    pass

class ArestaResponse(ArestaBase):
    id: UUID

    class Config:
        orm_mode = True

class GrafoBase(BaseModel):
    nome: str

class GrafoCreate(GrafoBase):
    nos: List[NoCreate]
    arestas: List[ArestaCreate]

class GrafoResponse(GrafoBase):
    id: UUID
    nos: List[NoResponse]
    arestas: List[ArestaResponse]

    class Config:
        orm_mode = True

class GrafoUpdate(BaseModel):
    nome: Optional[str] = None
    nos: Optional[List[Union[NoCreate, NoResponse]]] = None
    arestas: Optional[List[Union[ArestaCreate, ArestaResponse]]] = None
