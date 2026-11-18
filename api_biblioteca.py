from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API Biblioteca Virtual - V2", version="1.0")

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    quantidade_disponivel: int

catalogo_livros = [
    {"id": 1, "titulo": "Sistemas Distribuídos: Princípios e Paradigmas", "autor": "Andrew Tanenbaum", "quantidade_disponivel": 3},
    {"id": 2, "titulo": "Clean Code", "autor": "Robert C. Martin", "quantidade_disponivel": 5},
    {"id": 3, "titulo": "Redes de Computadores", "autor": "James Kurose", "quantidade_disponivel": 2}
]

# Rota principal (Interface Web)
@app.get("/", response_class=HTMLResponse)
def pagina_inicial():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# 1. GET -> Consultar todos os livros ou um específico
@app.get("/livros", response_model=List[Livro])
def listar_livros():
    return catalogo_livros

@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):
    for livro in catalogo_livros:
        if livro["id"] == livro_id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# 2. POST -> Cadastrar novo livro
@app.post("/livros", response_model=Livro, status_code=201)
def cadastrar_livro(livro: Livro):
    for item in catalogo_livros:
        if item["id"] == livro.id:
            raise HTTPException(status_code=400, detail="ID de livro já cadastrado")
    catalogo_livros.append(livro.model_dump())
    return livro

# 3. PUT -> Atualizar dados ou estoque
@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    for index, item in enumerate(catalogo_livros):
        if item["id"] == livro_id:
            catalogo_livros[index] = livro_atualizado.model_dump()
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# 4. DELETE -> Remover um livro
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int):
    for index, item in enumerate(catalogo_livros):
        if item["id"] == livro_id:
            catalogo_livros.pop(index)
            return {"mensagem": "Livro removido com sucesso"}
    raise HTTPException(status_code=404, detail="Livro não encontrado")