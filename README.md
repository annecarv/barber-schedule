# BarberSchedule Lite

Sistema completo de agendamento para barbearia com frontend React e backend FastAPI.

## Tecnologias Utilizadas

### Frontend
- React 18 + TypeScript
- Vite (bundler)
- React Router (navegacao)
- TailwindCSS (estilizacao)
- Shadcn/UI (componentes)
- Lucide Icons (icones)

### Backend
- FastAPI (framework)
- SQLModel (ORM)
- SQLite (banco de dados)
- Pydantic (validacao)
- JWT (autenticacao)
- Bcrypt (hash de senhas)

## Funcionalidades

### Telas Implementadas
- Landing Page - apresentacao do negocio
- Pagina de Agendamento - fluxo completo com selecao de servico, barbeiro, data e horario
- Tela de Login - autenticacao de profissionais e administradores
- Dashboard Profissional - visualizacao de agendamentos do dia e futuros
- Painel Admin - gerenciamento de servicos, barbeiros e agenda geral

### Recursos
- Layout responsivo
- Validacao de formularios
- Sistema de rotas com React Router
- Componentes reutilizaveis (Button, Input, Card, Calendar, etc)
- Integracao com API REST

## Estrutura do Projeto

```
/
├── src/
│   ├── components/
│   │   ├── ui/              # Componentes reutilizaveis
│   │   ├── LandingPage.tsx
│   │   ├── BookingPage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── ProfessionalDashboard.tsx
│   │   ├── AdminPanel.tsx
│   │   └── AdminAgenda.tsx
│   ├── services/
│   │   └── api.ts           # Servicos de API
│   └── utils/
│       └── routes.tsx       # Configuracao de rotas
├── backend/
│   ├── app/
│   │   ├── auth.py          # Autenticacao JWT
│   │   ├── database.py      # Configuracao do banco
│   │   ├── main.py          # Aplicacao FastAPI
│   │   ├── models/          # Modelos SQLModel
│   │   ├── schemas/         # Schemas Pydantic
│   │   └── routers/         # Endpoints da API
│   ├── requirements.txt
│   └── seed_data.py
└── README.md
```

## Instalacao e Execucao

### Frontend

```bash
npm install
npm run dev
```

Acesse: http://localhost:5173

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```

Documentacao da API: http://localhost:8000/docs

## Credenciais de Acesso

### Profissional
```
Email: barbeiro1@barbearia.com.br
Senha: 871374
```
Acesso: `/profissional/dashboard`

### Administrador
```
Email: admin@barbearia.com.br
Senha: admin123
```
Acesso: `/admin/dashboard`

## API Endpoints

### Autenticacao
- POST /auth/register - Registrar barbeiro
- POST /auth/login - Login (retorna JWT)

### Servicos
- GET /api/services - Listar servicos
- POST /api/services - Criar servico
- PUT /api/services/{id} - Atualizar servico
- DELETE /api/services/{id} - Desativar servico

### Barbeiros
- GET /api/barbers - Listar barbeiros
- POST /api/barbers - Criar barbeiro
- PUT /api/barbers/{id} - Atualizar barbeiro
- DELETE /api/barbers/{id} - Desativar barbeiro

### Agendamentos
- GET /api/bookings - Listar agendamentos
- GET /api/bookings/available-times - Horarios disponiveis
- POST /api/bookings - Criar agendamento
- PUT /api/bookings/{id} - Atualizar agendamento
- DELETE /api/bookings/{id} - Cancelar agendamento
