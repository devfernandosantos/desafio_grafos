import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from geoalchemy2 import Geometry
from sqlalchemy import func

Base = declarative_base()

class Grafo(Base):
    __tablename__ = "grafos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, index=True)
    nos = relationship("No", back_populates="grafo", cascade="all, delete-orphan")
    arestas = relationship("Aresta", back_populates="grafo", cascade="all, delete-orphan")

    def to_wkt(self, db: Session):
        for no in self.nos:
            no.coordenada = db.scalar(func.ST_AsText(no.coordenada))
        for aresta in self.arestas:
            aresta.linha = db.scalar(func.ST_AsText(aresta.linha))
    
    def __str__(self):
        nos_str = '\n'.join([f'No ID: {no.id}, Nome: {no.nome}, Coordenada: {no.coordenada}' for no in self.nos])
        arestas_str = '\n'.join([f'Aresta ID: {aresta.id}, Origem: {aresta.no_origem_id}, Destino: {aresta.no_destino_id}, Linha: {aresta.linha}' for aresta in self.arestas])
        return f'Grafo ID: {self.id}, Nome: {self.nome}\nNos:\n{nos_str}\nArestas:\n{arestas_str}'

class No(Base):
    __tablename__ = "nos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    grafo_id = Column(UUID(as_uuid=True), ForeignKey('grafos.id'), nullable=False)
    nome = Column(String, index=True)
    coordenada = Column(Geometry('POINT', srid=4326))
    grafo = relationship("Grafo", back_populates="nos")

    def convert_to_wkt(self, db: Session):
        self.coordenada = db.scalar(func.ST_AsText(self.coordenada))

class Aresta(Base):
    __tablename__ = "arestas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    grafo_id = Column(UUID(as_uuid=True), ForeignKey('grafos.id'), nullable=False)
    no_origem_id = Column(UUID(as_uuid=True), ForeignKey('nos.id'), nullable=False)
    no_destino_id = Column(UUID(as_uuid=True), ForeignKey('nos.id'), nullable=False)
    linha = Column(Geometry('LINESTRING', srid=4326))
    grafo = relationship("Grafo", back_populates="arestas")
    no_origem = relationship("No", foreign_keys=[no_origem_id])
    no_destino = relationship("No", foreign_keys=[no_destino_id])

    def convert_to_wkt(self, db: Session):
        self.linha = db.scalar(func.ST_AsText(self.linha))
