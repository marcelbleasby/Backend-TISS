# TISS Backend

Este projeto é um **backend em FastAPI** para a geração e persistência de guias no **padrão TISS** dos planos de saúde do Brasil. Ele integra com o **Docling** para renderizar as guias no formato XML.

## Funcionalidades

- **Autenticação via Token Estático**: O backend requer um token específico, enviado no header de cada requisição.
- **Geração de Guias TISS**: Através da rota POST `/guides`, é possível enviar os dados para gerar a guia TISS (consulta, SADT ou internação) e retornar o XML gerado.
- **Persistência de Guias**: Todas as guias geradas são salvas em um banco de dados PostgreSQL, incluindo o conteúdo do XML.
- **Busca e Listagem de Guias**: É possível buscar guias salvas por nome do paciente (`GET /guides?patient_name={nome}`) e obter uma guia por ID (`GET /guides/{guide_id}`).

## Arquitetura

- **FastAPI**: Framework para o backend RESTful.
- **Docling**: Usado para gerar as guias TISS a partir dos dados recebidos.
- **PostgreSQL**: Banco de dados utilizado para persistir as guias geradas.
- **SQLAlchemy**: ORM utilizado para comunicação com o banco de dados.
- **Docker**: Contêineres para o ambiente backend e banco de dados.

## Inicialização do Projeto

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd <diretorio-do-repositorio>
