# Desafio Grafos

Este projeto é um CRUD de grafos desenvolvido com FastAPI e SQLAlchemy. Ele permite criar, ler, atualizar e deletar grafos, além de buscar rotas e a rota mais curta entre nós em um grafo.

## Requisitos

- Python 3.11
- Docker e Docker Compose

## Instalação

1. Clone o repositório:

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2. Configure o ambiente virtual e instale as dependências:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Configure o banco de dados no arquivo `config/database.py`.

4. Inicie o sistema usando Docker Compose:

    ```bash
    docker-compose up
    ```

O sistema estará disponível em `http://127.0.0.1:8000`.

## Endpoints

### Criar um Grafo

- **URL**: `/grafos/`
- **Método**: `POST`
- **Corpo da Requisição**:
    ```json
    {
        "nome": "Test Grafo",
        "nos": [
            {"nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    }
    ```
- **Resposta de Sucesso**: `200 OK`
    ```json
    {
        "id": "a47135a7-d216-44c1-b109-fc7b200a09fe",
        "nome": "Test Grafo",
        "nos": [
            {"id": "f60ef40a-0998-43bf-8e1f-967886efcda6", "nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"id": "72cdf86b-710f-4ba4-bdd2-6075e9281308", "nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    }
    ```

### Ler um Grafo

- **URL**: `/grafos/{grafo_id}`
- **Método**: `GET`
- **Resposta de Sucesso**: `200 OK`
    ```json
    {
        "id": "a47135a7-d216-44c1-b109-fc7b200a09fe",
        "nome": "Test Grafo",
        "nos": [
            {"id": "f60ef40a-0998-43bf-8e1f-967886efcda6", "nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"id": "72cdf86b-710f-4ba4-bdd2-6075e9281308", "nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    }
    ```

### Listar Todos os Grafos

- **URL**: `/grafos/`
- **Método**: `GET`
- **Resposta de Sucesso**: `200 OK`
    ```json
    [
        {
            "id": "a47135a7-d216-44c1-b109-fc7b200a09fe",
            "nome": "Test Grafo",
            "nos": [
                {"id": "f60ef40a-0998-43bf-8e1f-967886efcda6", "nome": "No 1", "coordenada": [-73.935242, 40.73061]},
                {"id": "72cdf86b-710f-4ba4-bdd2-6075e9281308", "nome": "No 2", "coordenada": [-73.975242, 40.75061]}
            ],
            "arestas": [
                {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                    [-73.935242, 40.73061],
                    [-73.975242, 40.75061]
                ]}
            ]
        }
    ]
    ```

### Atualizar um Grafo

- **URL**: `/grafos/{grafo_id}`
- **Método**: `PATCH`
- **Corpo da Requisição**:
    ```json
    {
        "nome": "Updated Grafo"
    }
    ```
- **Resposta de Sucesso**: `200 OK`
    ```json
    {
        "id": "a47135a7-d216-44c1-b109-fc7b200a09fe",
        "nome": "Updated Grafo",
        "nos": [
            {"id": "f60ef40a-0998-43bf-8e1f-967886efcda6", "nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"id": "72cdf86b-710f-4ba4-bdd2-6075e9281308", "nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    }
    ```

### Deletar um Grafo

- **URL**: `/grafos/{grafo_id}`
- **Método**: `DELETE`
- **Resposta de Sucesso**: `204 No Content`

### Obter Todas as Rotas

- **URL**: `/grafos/{grafo_id}/routes?start_node_id={start_node_id}&end_node_id={end_node_id}`
- **Método**: `GET`
- **Parâmetros de Consulta**:
    - `start_node_id`: ID do nó inicial.
    - `end_node_id`: ID do nó final.
    - `max_stops` (opcional): Número máximo de paradas.
- **Resposta de Sucesso**: `200 OK`
    ```json
    [
        ["f60ef40a-0998-43bf-8e1f-967886efcda6", "72cdf86b-710f-4ba4-bdd2-6075e9281308"]
    ]
    ```

### Obter a Rota Mais Curta

- **URL**: `/grafos/{grafo_id}/shortest_route?start_node_id={start_node_id}&end_node_id={end_node_id}`
- **Método**: `GET`
- **Parâmetros de Consulta**:
    - `start_node_id`: ID do nó inicial.
    - `end_node_id`: ID do nó final.
- **Resposta de Sucesso**: `200 OK`
    ```json
    ["f60ef40a-0998-43bf-8e1f-967886efcda6", "72cdf86b-710f-4ba4-bdd2-6075e9281308"]
    ```

### Obter Todas as Rotas

- **URL**: `/grafos/{grafo_id}/routes?start_node_id={start_node_id}&end_node_id={end_node_id}`
- **Método**: `GET`
- **Parâmetros de Consulta**:
    - `start_node_id`: ID do nó inicial.
    - `end_node_id`: ID do nó final.
    - `max_stops` (opcional): Número máximo de paradas.
- **Resposta de Sucesso**: `200 OK`
    ```json
    [
        ["f60ef40a-0998-43bf-8e1f-967886efcda6", "72cdf86b-710f-4ba4-bdd2-6075e9281308"]
    ]
    ```

### Obter a Rota Mais Curta

- **URL**: `/grafos/{grafo_id}/shortest_route?start_node_id={start_node_id}&end_node_id={end_node_id}`
- **Método**: `GET`
- **Parâmetros de Consulta**:
    - `start_node_id`: ID do nó inicial.
    - `end_node_id`: ID do nó final.
- **Resposta de Sucesso**: `200 OK`
    ```json
    ["f60ef40a-0998-43bf-8e1f-967886efcda6", "72cdf86b-710f-4ba4-bdd2-6075e9281308"]
    ```

## Testes

Para rodar os testes, utilize o comando:

```bash
pytest
