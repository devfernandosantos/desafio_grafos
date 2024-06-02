from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

Base = declarative_base()

class Grafo(Base):
    __tablename__ = "grafos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    nos = relationship("No", back_populates="grafo", cascade="all, delete-orphan")
    arestas = relationship("Aresta", back_populates="grafo", cascade="all, delete-orphan")

class No(Base):
    __tablename__ = "nos"

    id = Column(Integer, primary_key=True, index=True)
    grafo_id = Column(Integer, ForeignKey('grafos.id'), nullable=False)
    nome = Column(String, index=True)
    coordenada = Column(Geometry('POINT', srid=4326))
    grafo = relationship("Grafo", back_populates="nos")

class Aresta(Base):
    __tablename__ = "arestas"

    id = Column(Integer, primary_key=True, index=True)
    grafo_id = Column(Integer, ForeignKey('grafos.id'), nullable=False)
    no_origem_id = Column(Integer, ForeignKey('nos.id'), nullable=False)
    no_destino_id = Column(Integer, ForeignKey('nos.id'), nullable=False)
    linha = Column(Geometry('LINESTRING', srid=4326))
    grafo = relationship("Grafo", back_populates="arestas")
    no_origem = relationship("No", foreign_keys=[no_origem_id])
    no_destino = relationship("No", foreign_keys=[no_destino_id])
