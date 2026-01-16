# Backend FastAPI - Barbershop API

API REST para sistema de agendamento de barbearia com autenticacao JWT.

## Tecnologias

- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- JWT (python-jose)
- Bcrypt (hash de senhas)

## Estrutura do Projeto

```
backend/
├── app/
│   ├── auth.py           # Autenticacao JWT
│   ├── database.py       # Configuracao do banco
│   ├── main.py           # Aplicacao FastAPI
│   ├── models/
│   │   └── models.py     # Modelos SQLModel
│   ├── schemas/
│   │   └── schemas.py    # Schemas Pydantic
│   └── routers/
│       ├── auth.py       # Login e registro
│       ├── services.py   # CRUD servicos
│       ├── barbers.py    # CRUD barbeiros
│       └── bookings.py   # CRUD agendamentos
├── requirements.txt
├── seed_data.py
└── dev.db
```

## Instalacao

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar

```bash
uvicorn app.main:app --reload --port 8000
```

## Popular dados iniciais

```bash
python seed_data.py
```

Cria 3 servicos e 3 barbeiros com credenciais de acesso.

## Credenciais de Acesso

```
Email: barbeiro1@barbearia.com.br
Senha: 871374
```

## Documentacao Interativa

Acesse http://localhost:8000/docs para a documentacao Swagger.

## Autenticacao JWT

### Registro de barbeiro

```
POST /auth/register
{
  "name": "Nome do Barbeiro",
  "email": "email@exemplo.com",
  "password": "senha123",
  "specialty": "Cortes Modernos"
}
```

### Login

```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=barbeiro1@barbearia.com.br&password=871374
```

Retorna:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Usar token

Adicione o header em requisicoes autenticadas:
```
Authorization: Bearer eyJ...
```

## Rotas da API

### Auth (/auth)

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /auth/register | Registrar barbeiro |
| POST | /auth/login | Login (retorna JWT) |

### Services (/api/services)

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | /api/services | Listar servicos |
| GET | /api/services/{id} | Obter servico |
| POST | /api/services | Criar servico |
| PUT | /api/services/{id} | Atualizar servico |
| DELETE | /api/services/{id} | Desativar servico |

### Barbers (/api/barbers)

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | /api/barbers | Listar barbeiros |
| GET | /api/barbers/{id} | Obter barbeiro |
| POST | /api/barbers | Criar barbeiro |
| PUT | /api/barbers/{id} | Atualizar barbeiro |
| DELETE | /api/barbers/{id} | Desativar barbeiro |

### Bookings (/api/bookings)

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | /api/bookings | Listar agendamentos |
| GET | /api/bookings/{id} | Obter agendamento |
| GET | /api/bookings/available-times | Horarios disponiveis |
| POST | /api/bookings | Criar agendamento |
| PUT | /api/bookings/{id} | Atualizar agendamento |
| DELETE | /api/bookings/{id} | Cancelar agendamento |

## Exemplo de Agendamento

```json
POST /api/bookings
{
  "customer_name": "Joao Silva",
  "customer_email": "joao@email.com",
  "customer_phone": "(11) 98765-4321",
  "service_id": 1,
  "barber_id": 1,
  "booking_date": "2025-12-31",
  "booking_time": "14:00"
}
```

## Variaveis de Ambiente

```env
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite+aiosqlite:///./dev.db
```
