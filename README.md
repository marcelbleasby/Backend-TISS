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
git clone https://github.com/marcelbleasby/Backend-TISS
cd Backend-TISS
```

### 2. Criar o seu arquivo .env
Crie um arquivo na raiz do seu projeto
```bash
DATABASE_URL=postgresql://tiss_user:tiss_password@db:5432/tiss
STATIC_TOKEN=seu_token_super_seguro
```
### 3. Montar seu docker-compose para aplicação
Execute o seguinte comando para inicializar o projeto:
```bash
docker-compose up --build
```
### 4. Acesse seu backend
Após a inicialização, o backend estará disponível em http://localhost:8000. O Swagger UI estará acessível em http://localhost:8000/docs

### 5. Teste sua API
Você pode testar as seguintes rotas:
	•	POST /guides: Envie os dados no formato GuideInput para gerar uma guia TISS e salvar no banco de dados.
Exemplo de corpo de requisição:
```json
{
  "guide_type": "consulta",
  "patient_name": "João da Silva",
  "provider_name": "Clínica ABC",
  "operator_name": "Operadora XYZ",
  "data": {
    "codigo": "12345",
    "valor": "100.00"
  }
}
```
•	GET /guides: Liste todas as guias salvas. Pode filtrar pela query patient_name.
•	GET /guides/{guide_id}: Busque uma guia específica pelo ID.

O resto das funcionalidades é com vocês

Docker Compose

O docker-compose.yml define dois serviços:
	•	db: Servidor PostgreSQL com o banco de dados tiss.
	•	backend: Contêiner com o FastAPI, que depende do banco de dados e expõe a API na porta 8000.

Variáveis de Ambiente
	•	DATABASE_URL: URL de conexão com o banco de dados PostgreSQL.
	•	STATIC_TOKEN: Token de autenticação para acessar as rotas da API.

Dependências

As dependências do projeto estão definidas em requirements.txt:
	•	fastapi: Framework para criar a API RESTful.
	•	uvicorn: Servidor ASGI para rodar o FastAPI.
	•	sqlalchemy: ORM para interação com o banco de dados.
	•	psycopg2-binary: Driver PostgreSQL para SQLAlchemy.
	•	pydantic: Biblioteca para validação de dados.
	•	python-dotenv: Carregamento das variáveis de ambiente do arquivo .env.

Como Funciona
	1.	O frontend envia os dados para o backend através de uma requisição POST.
	2.	O backend usa o Docling CLI para gerar o arquivo XML TISS.
	3.	O XML gerado é salvo no banco de dados PostgreSQL juntamente com as informações da guia (tipo, paciente, provedor, operadora).
	4.	O usuário pode buscar, listar ou obter detalhes sobre as guias salvas.

Contribuindo

Se desejar contribuir, siga os passos abaixo:
	1.	Faça um fork do repositório.
	2.	Crie uma branch para a sua funcionalidade (git checkout -b feature-nome).
	3.	Faça commit das suas mudanças (git commit -am 'Adiciona nova funcionalidade').
	4.	Push para a branch (git push origin feature-nome).
	5.	Abra um Pull Request.


