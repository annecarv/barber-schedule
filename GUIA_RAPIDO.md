# 🚀 Guia Rápido - Barbershop API

## ⚡ Início Rápido

```bash
# 1. Iniciar o backend (em um terminal)
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# 2. Iniciar o frontend (em outro terminal)
npm run dev

# 3. Acessar
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/docs
```

## 🎯 Principais Endpoints

### Listar Dados

```bash
# Serviços
GET http://localhost:8000/api/services

# Barbeiros
GET http://localhost:8000/api/barbers

# Agendamentos (com filtros opcionais)
GET http://localhost:8000/api/bookings?barber_id=1&date=2025-12-31

# Horários disponíveis
GET http://localhost:8000/api/bookings/available-times?barber_id=1&date=2025-12-31&service_id=1
```

### Criar Agendamento

```bash
POST http://localhost:8000/api/bookings
Content-Type: application/json

{
  "customer_name": "João Silva",
  "customer_email": "joao@email.com",
  "customer_phone": "(11) 98765-4321",
  "service_id": 1,
  "barber_id": 1,
  "booking_date": "2025-12-31",
  "booking_time": "14:00"
}
```

### Cancelar Agendamento

```bash
DELETE http://localhost:8000/api/bookings/{booking_id}
```

## 📊 Dados Iniciais

### Serviços (IDs: 1, 2, 3)
- **ID 1**: Serviço 1 - 30min - R$ 25
- **ID 2**: Serviço 2 - 1h - R$ 50
- **ID 3**: Serviço 3 - 1h30min - R$ 75

### Barbeiros (IDs: 1, 2, 3)
- **ID 1**: Barbeiro 1 - barbeiro1@barbearia.com.br
- **ID 2**: Barbeiro 2 - barbeiro2@barbearia.com.br
- **ID 3**: Barbeiro 3 - barbeiro3@barbearia.com.br

## 🔧 Comandos Úteis

```bash
# Popular dados novamente (se deletou o banco)
python seed_data.py

# Rodar testes do backend
cd backend
source .venv/bin/activate
python -m pytest tests/ -v

# Ver logs do servidor
# Os logs aparecem no terminal onde você rodou uvicorn

# Resetar banco de dados
# Simplesmente delete o arquivo dev.db e rode novamente
rm dev.db
python seed_data.py
```

## 💡 Exemplos de Uso em JavaScript

### Listar Serviços
```javascript
const services = await fetch('http://localhost:8000/api/services')
  .then(res => res.json());
console.log(services);
```

### Criar Agendamento
```javascript
const booking = await fetch('http://localhost:8000/api/bookings', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    customer_name: "Maria Santos",
    service_id: 1,
    barber_id: 2,
    booking_date: "2025-12-31",
    booking_time: "10:00"
  })
}).then(res => res.json());

console.log('Agendamento criado:', booking);
```

### Ver Horários Disponíveis
```javascript
const times = await fetch(
  'http://localhost:8000/api/bookings/available-times?' +
  new URLSearchParams({
    barber_id: '1',
    date: '2025-12-31',
    service_id: '1'
  })
).then(res => res.json());

console.log('Horários disponíveis:', times.available_times);
```

## 🐛 Troubleshooting

### Backend não inicia
- Certifique-se que está no virtualenv: `source .venv/bin/activate`
- Verifique se a porta 8000 está livre: `lsof -i :8000`

### CORS Error no Frontend
- Backend já está configurado com CORS para `localhost:5173` e `localhost:3000`
- Se estiver usando outra porta, adicione em `backend/app/main.py`

### Horários não aparecem disponíveis
- Verifique se os IDs de barber_id e service_id existem
- Data deve estar no formato `YYYY-MM-DD`
- Certifique-se que o barbeiro não tem agendamentos conflitantes

### Erro ao criar agendamento
- Verifique se o horário está realmente disponível
- Service e Barber devem estar ativos (`active: true`)
- Data e hora devem estar no formato correto

## 📚 Recursos

- **Documentação Interativa**: http://localhost:8000/docs
- **API Backend**: Veja `backend/README.md`
- **Exemplo de Integração**: Veja `EXEMPLO_INTEGRACAO.md`
- **Service API TypeScript**: Veja `src/services/api.ts`
