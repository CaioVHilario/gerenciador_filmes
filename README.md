# API - Gerenciador de Lista de Filmes

[![Status](https://img.shields.io/badge/status-em_desenvolvimento-yellow)](https://https://github.com/CaioVHilario/gerenciador_filmes)

API RESTful para gerenciar uma coleção de filmes. Este projeto está sendo construído como parte dos meus estudos em desenvolvimento backend com Python.

## Objetivo

O objetivo principal é implementar um CRUD (Create, Read, Update, Delete) completo para gerenciar filmes, aprendendo os fundamentos do FastAPI, SQLModel e arquitetura de APIs REST.

## Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI:** Para a construção da API.
* **SQLModel:** Para o ORM (interação com o banco de dados) e validação de dados.
* **SQLite:** Como banco de dados de desenvolvimento.
* **Uvicorn:** Como servidor ASGI.

## Status Atual

* [x] Configuração inicial do projeto.
* [x] Definição do modelo de dados (`Movie`).
* [x] Configuração do banco de dados SQLite e criação de tabelas no *lifespan* da aplicação.
* [x] Endpoint: `POST /movies` (Create)
* [ ] Endpoint: `GET /movies` (Read All)
* [ ] Endpoint: `GET /movies/{id}` (Read One)
* [ ] Endpoint: `PATCH /movies/{id}` (Update)
* [ ] Endpoint: `DELETE /movies/{id}` (Delete)