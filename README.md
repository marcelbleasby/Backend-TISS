# TISS Backend - Documentação Completa

## Visão Geral
Este projeto é um **backend em FastAPI** para geração e persistência de guias no **padrão TISS** dos planos de saúde brasileiros. Integra com o **Docling** para renderização das guias em formato XML.

## Funcionalidades Principais
- **Autenticação Segura**
  - Token estático no header das requisições
- **Geração de Guias TISS**
  - Tipos suportados: consulta, SADT e internação
  - Retorno em formato XML
- **Gestão de Guias**
  - Persistência em PostgreSQL
  - Busca por nome do paciente
  - Recuperação por ID

## Arquitetura
| Componente       | Tecnologia     | Função                           |
|------------------|----------------|----------------------------------|
| Backend          | FastAPI        | API RESTful                      |
| Renderização     | Docling        | Geração de XML TISS              |
| Banco de Dados   | PostgreSQL     | Armazenamento persistente        |
| ORM              | SQLAlchemy     | Comunicação com DB               |
| Containerização  | Docker         | Ambiente isolado e reproduzível  |

## Configuração do Ambiente

### Pré-requisitos
- Docker
- Docker Compose
- Git (para clonar o repositório)

### Passos de Instalação
1. **Clonar repositório**
   ```bash
   git clone https://github.com/marcelbleasby/Backend-TISS
   cd Backend-TISS
   ```

2. **Configurar variáveis de ambiente**
   Criar arquivo `.env` na raiz com:
   ```env
   DATABASE_URL=postgresql://tiss_user:tiss_password@db:5432/tiss
   STATIC_TOKEN=seu_token_super_seguro
   ```

3. **Inicializar containers**
   ```bash
   docker-compose up --build
   ```

## Acesso à API
- **URL Base**: `http://localhost:8000`
- **Documentação Interativa**: `http://localhost:8000/docs` (Swagger UI)

## Endpoints

### POST /guides
Gera nova guia TISS e persiste no banco de dados.

**Headers:**
```
Authorization: Bearer <STATIC_TOKEN>
```

**Exemplo de Request Body:**
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

**Respostas:**
- 201 Created: Guia gerada com sucesso
- 401 Unauthorized: Token inválido/missing
- 422 Unprocessable Entity: Dados inválidos

### GET /guides
Lista todas as guias, com filtro opcional.

**Parâmetros Query:**
- `patient_name` (opcional): Filtra por nome do paciente

**Exemplo:**
```
GET /guides?patient_name=João
```

### GET /guides/{guide_id}
Recupera uma guia específica por ID.

**Exemplo:**
```
GET /guides/1
```

## Estrutura do Projeto
```
Backend-TISS/
├── app/
│   ├── __init__.py
│   ├── main.py          # Configuração FastAPI
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Modelos Pydantic
│   └── database.py      # Configuração DB
├── .env                 # Variáveis de ambiente
├── requirements.txt     # Dependências Python
└── docker-compose.yml   # Configuração Docker
```

## Dependências
Listadas em `requirements.txt`:
```
fastapi==0.68.0
uvicorn==0.15.0
sqlalchemy==1.4.22
psycopg2-binary==2.9.1
pydantic==1.8.2
python-dotenv==0.19.0
```

## Serviços Docker
| Serviço    | Imagem           | Porta  | Descrição                     |
|------------|------------------|--------|-------------------------------|
| backend    | Custom FastAPI   | 8000   | Aplicação principal           |
| db         | postgres:13      | 5432   | Banco de dados PostgreSQL     |

## Modelos de Dados

### Guide (Banco de Dados)
- id: Integer (PK)
- guide_type: String
- patient_name: String
- provider_name: String
- operator_name: String
- xml_content: Text
- created_at: DateTime

### GuideInput (Pydantic)
- guide_type: Enum (consulta, sadt, internacao)
- patient_name: str
- provider_name: str
- operator_name: str
- data: dict (dados específicos da guia)

## Fluxo de Trabalho Recomendado
1. Gerar guia via POST /guides
2. Armazenar localmente o ID retornado
3. Recuperar guias quando necessário via GET /guides ou GET /guides/{id}

## Observações Importantes
- O token estático deve ser mantido em segredo
- O formato dos dados específicos (`data`) varia conforme o tipo de guia
- Todas as requisições devem incluir o header de autorização
