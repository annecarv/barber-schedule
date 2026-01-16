# Backend FastAPI - Barbershop API

API REST para sistema de agendamento de barbearia.

## Pre-requisitos

- Python 3.10+

## Instalacao

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Variaveis de ambiente (.env)

```env
DATABASE_URL=sqlite+aiosqlite:///./dev.db
```

## Executar

```bash
uvicorn app.main:app --reload --port 8000
```

## Popular dados iniciais

```bash
python seed_data.py
```

Cria 3 servicos e 3 barbeiros.

## Documentacao

Acesse http://localhost:8000/docs para a documentacao Swagger.

## Rotas da API

### Services (/api/services)

- GET /api/services - Listar servicos
- GET /api/services/{id} - Obter servico
- POST /api/services - Criar servico
- PUT /api/services/{id} - Atualizar servico
- DELETE /api/services/{id} - Desativar servico

### Barbers (/api/barbers)

- GET /api/barbers - Listar barbeiros
- GET /api/barbers/{id} - Obter barbeiro
- POST /api/barbers - Criar barbeiro
- PUT /api/barbers/{id} - Atualizar barbeiro
- DELETE /api/barbers/{id} - Desativar barbeiro

### Bookings (/api/bookings)

- POST /api/bookings - Criar agendamento
- GET /api/bookings - Listar agendamentos (filtros: barber_id, date, status)
- GET /api/bookings/available-times - Horarios disponiveis (params: barber_id, date, service_id)
- GET /api/bookings/{id} - Obter agendamento
- PUT /api/bookings/{id} - Atualizar agendamento
- DELETE /api/bookings/{id} - Cancelar agendamento

## Exemplo de agendamento

```json
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
