# 🎬 API - Gerenciador de Lista de Filmes

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.14-ff6b6b.svg)](https://sqlmodel.tiangolo.com/)
[![Status](https://img.shields.io/badge/status-em_desenvolvimento-yellow)](https://github.com/CaioVHilario/gerenciador_filmes)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Uma API RESTful completa para gerenciar sua coleção de filmes favoritos. Desenvolvida como parte do aprendizado em backend com Python, FastAPI e boas práticas de desenvolvimento.

## ✨ Funcionalidades

- ✅ **CRUD Completo** - Create, Read, Update, Delete de filmes
- 🔍 **Múltiplas Buscas** - Por título, diretor, gênero
- 🎯 **Validação de Dados** - Schemas Pydantic para entradas seguras
- 📚 **Documentação Automática** - Swagger UI e ReDoc inclusos
- 🗄️ **Banco de Dados** - SQLite com SQLModel para ORM moderno

## 🛠️ Tecnologias

- **Python 3.10+**
- **FastAPI** - Framework web moderno e rápido
- **SQLModel** - ORM com suporte a type hints
- **SQLite** - Banco de dados para desenvolvimento
- **Uvicorn** - Servidor ASGI de alta performance
- **Pydantic** - Validação de dados e serialização

## 🎯 Próximos Objetivos de Aprendizado

### 🔐 Autenticação JWT
- Implementar sistema de usuários e autenticação
- Proteger endpoints com JWT tokens
- Aprender sobre segurança em APIs

### 🗄️ Migração para PostgreSQL
- Configurar e conectar com PostgreSQL
- Aprender diferenças entre SQLite e PostgreSQL
- Gerenciar migrações de banco

### 🧪 Testes com Pytest
- Escrever testes unitários para os endpoints
- Aprender Test-Driven Development (TDD)
- Configurar cobertura de testes

### 🐳 Dockerização
- Criar Dockerfile para a aplicação
- Aprender sobre containers e orquestração
- Configurar Docker Compose para desenvolvimento

### 📄 Paginação
- Implementar paginação nos endpoints de listagem
- Melhorar performance com grandes volumes de dados

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior
- Git

### Instalação

1. **Clone o repositório**
 ```bash
git clone https://github.com/CaioVHilario/gerenciador_filmes.git
cd gerenciador_filmes
```

2. **Crie um ambiente virtual (recomendado)**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```
    
3. **Instale as dependências**

```bash
pip install -r requirements.txt
```    

4. **Execute a API**

```bash
uvicorn app.main:app --reload
```

5. **Acesse a documentação**

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📚 Exemplos de Uso

### Criar um filme

```bash

curl -X POST "http://127.0.0.1:8000/movies/" \
-H "Content-Type: application/json" \
-d '{
  "title": "O Poderoso Chefão",
  "description": "Uma família mafiosa luta pelo poder",
  "year": 1972,
  "director": "Francis Ford Coppola",
  "genre": "Crime, Drama",
  "rating": 9.2
}
```

### Buscar filmes por diretor

```bash
curl -X GET "http://127.0.0.1:8000/movies/director/Coppola"
```

### Buscar filmes por título

```bash
curl -X GET "http://127.0.0.1:8000/movies/title/poderoso"
```
## 📁 Estrutura do Projeto

```text
gerenciador_filmes/
├── app/
│   ├── main.py          # Aplicação FastAPI principal
│   ├── database.py      # Configuração do banco de dados
│   ├── models.py        # Modelos SQLModel
│   ├── schemas.py       # Schemas Pydantic
│   └── routers/
│       └── movies.py    # Endpoints de filmes
├── data/
│   └── movies.db        # Banco de dados SQLite
├── requirements.txt
└── README.md`
```

## 📊 Endpoints da API

### CRUD Básico

|Método|Endpoint|Descrição|
|---|---|---|
|`POST`|`/movies/`|Criar novo filme|
|`GET`|`/movies/`|Listar todos os filmes|
|`GET`|`/movies/{id}`|Buscar filme por ID|
|`PATCH`|`/movies/{id}`|Atualizar filme parcialmente|
|`DELETE`|`/movies/{id}`|Deletar filme|

### Buscas

|Método|Endpoint|Descrição|
|---|---|---|
|`GET`|`/movies/title/{title}`|Busca por título|
|`GET`|`/movies/director/{director}`|Busca por diretor|
|`GET`|`/movies/genre/{genre}`|Busca por gênero|

## 🗓️ Roadmap

### ✅ Concluído

- Configuração inicial do projeto
    
- Modelo de dados `Movie`
    
- Configuração do banco SQLite
    
- Endpoints CRUD completos
    
- Buscas por título, diretor e gênero

- Busca com filtros múltiplos

- Busca em tempo real

- Validação de dados Pydantic
    
    
### 🔄 Em Desenvolvimento

- **Autenticação JWT** - Sistema de usuários e segurança

- **PostgreSQL** - Migração do banco de dados

- **Testes com Pytest** - Qualidade e confiabilidade do código

- **Docker** - Containerização da aplicação

- **Paginação** - Melhoria de performance em listas
    

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fork o projeto
    
2. Criar uma branch para sua feature (`git checkout -b feature/nova-feature`)
    
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova feature'`)
    
4. Push para a branch (`git push origin feature/nova-feature`)
    
5. Abrir um Pull Request
    
## 🎓 Sobre Este Projeto

Este projeto faz parte da minha jornada de aprendizado em desenvolvimento backend. Cada funcionalidade implementada representa um novo conceito ou tecnologia que estou explorando.

**Objetivo principal**: Aprender construindo uma aplicação real, seguindo boas práticas e padrões profissionais.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://license/) para mais detalhes.

---

**Desenvolvido com ❤️ como parte do aprendizado em Python e FastAPI**