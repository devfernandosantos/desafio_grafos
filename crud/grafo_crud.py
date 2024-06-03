from sqlalchemy.orm import Session
from models.grafo_model import Grafo, No, Aresta
from schemas.grafo_schema import GrafoCreate, GrafoUpdate, GrafoResponse
from sqlalchemy import func
from typing import List
from collections import OrderedDict
import uuid
import networkx as nx

def create_grafo(db: Session, grafo: GrafoCreate) -> GrafoResponse:
    db_grafo = Grafo(id=uuid.uuid4(), nome=grafo.nome)
    db.add(db_grafo)
    db.commit()
    db.refresh(db_grafo)

    nos_map = {}
    for no in grafo.nos:
        coordenada_wkt = f'POINT({no.coordenada[0]} {no.coordenada[1]})'
        db_no = No(
            id=uuid.uuid4(),
            grafo_id=db_grafo.id,
            nome=no.nome,
            coordenada=f'SRID=4326;{coordenada_wkt}'
        )
        db.add(db_no)
        db.commit()
        db.refresh(db_no)
        nos_map[no.nome] = db_no.id

    for aresta in grafo.arestas:
        linha_wkt = f"LINESTRING({', '.join([f'{coord[0]} {coord[1]}' for coord in aresta.linha])})"
        no_origem_id = nos_map.get(aresta.no_origem_id)
        no_destino_id = nos_map.get(aresta.no_destino_id)

        if no_origem_id is None:
            raise KeyError(f"Nó de origem com nome {aresta.no_origem_id} não encontrado no mapeamento.")
        if no_destino_id is None:
            raise KeyError(f"Nó de destino com nome {aresta.no_destino_id} não encontrado no mapeamento.")

        db_aresta = Aresta(
            id=uuid.uuid4(),
            grafo_id=db_grafo.id,
            no_origem_id=no_origem_id,
            no_destino_id=no_destino_id,
            linha=f'SRID=4326;{linha_wkt}'
        )
        db.add(db_aresta)
    db.commit()

    return formatar_response(db_grafo, db)

def get_grafo(db: Session, grafo_id: uuid.UUID) -> GrafoResponse:
    db_grafo = db.query(Grafo).filter(Grafo.id == grafo_id).first()
    if db_grafo is None:
        return None

    return formatar_response(db_grafo, db)

def get_all_grafos(db: Session) -> List[GrafoResponse]:
    grafos = db.query(Grafo).all()
    return [formatar_response(grafo, db) for grafo in grafos]

def update_grafo(db: Session, grafo_id: uuid.UUID, grafo: GrafoUpdate) -> GrafoResponse:
    db_grafo = db.query(Grafo).filter(Grafo.id == grafo_id).first()
    if db_grafo is None:
        return None

    db_grafo.nome = grafo.nome
    db.commit()
    db.refresh(db_grafo)

    return formatar_response(db_grafo, db)

def delete_grafo(db: Session, grafo_id: uuid.UUID):
    db_grafo = db.query(Grafo).filter(Grafo.id == grafo_id).first()
    if db_grafo is None:
        return None

    db.delete(db_grafo)
    db.commit()

    return None

def formatar_response(grafo: Grafo, db: Session) -> GrafoResponse:
    nos = [
        OrderedDict([
            ("id", str(no.id)),
            ("nome", no.nome),
            ("coordenada", list(map(float, db.scalar(func.ST_AsText(no.coordenada)).replace("POINT(", "").replace(")", "").split())))
        ])
        for no in grafo.nos
    ]
    arestas = [
        OrderedDict([
            ("id", str(aresta.id)),
            ("no_origem_id", str(aresta.no_origem_id)),
            ("no_destino_id", str(aresta.no_destino_id)),
            ("linha", [
                list(map(float, coord.split()))
                for coord in db.scalar(func.ST_AsText(aresta.linha)).replace("LINESTRING(", "").replace(")", "").split(",")
            ])
        ])
        for aresta in grafo.arestas
    ]
    return OrderedDict([
        ("id", str(grafo.id)),
        ("nome", grafo.nome),
        ("nos", nos),
        ("arestas", arestas)
    ])

def get_all_routes(db: Session, grafo_id: uuid.UUID, start_node_id: uuid.UUID, end_node_id: uuid.UUID, max_stops: int = None):
    grafo = db.query(Grafo).filter(Grafo.id == grafo_id).first()
    if not grafo:
        return None

    G = nx.DiGraph()

    for no in grafo.nos:
        G.add_node(no.id, name=no.nome, coordenada=no.coordenada)

    for aresta in grafo.arestas:
        G.add_edge(aresta.no_origem_id, aresta.no_destino_id, id=aresta.id)

    all_paths = list(nx.all_simple_paths(G, source=start_node_id, target=end_node_id, cutoff=max_stops))
    
    return all_paths

def get_shortest_route(db: Session, grafo_id: uuid.UUID, start_node_id: uuid.UUID, end_node_id: uuid.UUID):
    grafo = db.query(Grafo).filter(Grafo.id == grafo_id).first()
    if not grafo:
        return None

    G = nx.DiGraph()

    for no in grafo.nos:
        G.add_node(no.id, name=no.nome, coordenada=no.coordenada)

    for aresta in grafo.arestas:
        G.add_edge(aresta.no_origem_id, aresta.no_destino_id, id=aresta.id)

    shortest_path = nx.shortest_path(G, source=start_node_id, target=end_node_id, weight=None, method='dijkstra')
    
    return shortest_path
