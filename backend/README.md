# Backend FastAPI - Barbershop & Community API

Uma API REST completa que combina funcionalidades de uma plataforma de comunidade com um sistema de agendamento para barbearia.

## Pré-requisitos
- Python 3.10+
- Criar um virtualenv

## Instalação

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Variáveis de ambiente (exemplo `.env`)

```env
AUTH0_DOMAIN=your-domain.auth0.com
API_AUDIENCE=your-audience
ALGORITHMS=RS256
DATABASE_URL=sqlite+aiosqlite:///./dev.db
```

## Rodar a aplicação

```bash
uvicorn app.main:app --reload --port 8000
```

## Popular dados iniciais (barbershop)

```bash
python seed_data.py
```

Isso criará:
- 3 serviços (Serviço 1, 2 e 3)
- 3 barbeiros (Barbeiro 1, 2 e 3)

## Documentação Interativa

Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para ver a documentação Swagger/OpenAPI.

## Observações
- A API valida JWTs emitidos pelo Auth0 utilizando o JWKS do domínio (apenas para rotas de comunidade).
- Perfis/roles são extraídos do claim `roles` (se estiverem no token). Adapte conforme seu issuer.
- Banco padrão: SQLite (zero-config) conforme enunciado.
- **CORS** está habilitado para `http://localhost:5173` e `http://localhost:3000`.

---

# Rotas da API

## 🪒 **Barbershop API** (sem autenticação)

### Services (`/api/services`)

#### `GET /api/services`
Listar todos os serviços.
- **Query params**:
  - `active_only` (bool, padrão: true) - Filtrar apenas serviços ativos
- **Response**: Lista de serviços

#### `GET /api/services/{service_id}`
Obter detalhes de um serviço específico.
- **Response**: Dados do serviço

#### `POST /api/services`
Criar um novo serviço.
- **Body**:
  ```json
  {
    "name": "string",
    "duration": "30min|1h|1h30min",
    "price": "string",
    "description": "string",
    "active": true
  }
  ```

#### `PUT /api/services/{service_id}`
Atualizar um serviço.
- **Body**: Campos opcionais para atualizar

#### `DELETE /api/services/{service_id}`
Desativar um serviço (soft delete).

---

### Barbers (`/api/barbers`)

#### `GET /api/barbers`
Listar todos os barbeiros.
- **Query params**:
  - `active_only` (bool, padrão: true) - Filtrar apenas barbeiros ativos
- **Response**: Lista de barbeiros

#### `GET /api/barbers/{barber_id}`
Obter detalhes de um barbeiro específico.

#### `POST /api/barbers`
Criar um novo barbeiro.
- **Body**:
  ```json
  {
    "name": "string",
    "email": "string",
    "specialty": "string",
    "active": true
  }
  ```

#### `PUT /api/barbers/{barber_id}`
Atualizar um barbeiro.

#### `DELETE /api/barbers/{barber_id}`
Desativar um barbeiro (soft delete).

---

### Bookings (`/api/bookings`)

#### `POST /api/bookings`
Criar um novo agendamento.
- **Body**:
  ```json
  {
    "customer_name": "string",
    "customer_email": "string",
    "customer_phone": "string",
    "service_id": int,
    "barber_id": int,
    "booking_date": "YYYY-MM-DD",
    "booking_time": "HH:MM"
  }
  ```
- **Response**: Agendamento criado com detalhes do serviço e barbeiro

#### `GET /api/bookings`
Listar agendamentos com filtros.
- **Query params**:
  - `barber_id` (int, opcional) - Filtrar por barbeiro
  - `date` (string, opcional) - Filtrar por data (YYYY-MM-DD)
  - `status` (string, opcional) - Filtrar por status (confirmed, cancelled, completed)
- **Response**: Lista de agendamentos com detalhes completos

#### `GET /api/bookings/available-times`
Obter horários disponíveis para agendamento.
- **Query params**:
  - `barber_id` (int, obrigatório)
  - `date` (string, obrigatório) - Data (YYYY-MM-DD)
  - `service_id` (int, obrigatório) - Para calcular duração
- **Response**:
  ```json
  {
    "available_times": ["09:00", "09:30", "10:00", ...]
  }
  ```

#### `GET /api/bookings/{booking_id}`
Obter detalhes de um agendamento específico.

#### `PUT /api/bookings/{booking_id}`
Atualizar um agendamento (status, data ou horário).
- **Body**:
  ```json
  {
    "status": "confirmed|cancelled|completed",
    "booking_date": "YYYY-MM-DD",
    "booking_time": "HH:MM"
  }
  ```

#### `DELETE /api/bookings/{booking_id}`
Cancelar um agendamento (seta status=cancelled).

---

## 💬 **Community API** (com autenticação)

### Posts (`/posts`)

#### `POST /posts`
Criar um novo post.
- **Autenticação**: Obrigatória
- **Body**:
  ```json
  {
    "title": "string",
    "content": "string",
    "category": "string",
    "tags": ["string"]
  }
  ```

#### `GET /posts`
Listar posts com filtros e paginação.
- **Query params**:
  - `limit` (int, padrão: 10)
  - `offset` (int, padrão: 0)
  - `q` (string, opcional) - Busca em título e conteúdo
  - `category` (string, opcional)
  - `tag` (string, opcional)
  - `author_sub` (string, opcional)
  - `order_by` (string, opcional) - created_at ou popularity

#### `GET /posts/search`
Buscar posts.
- **Query params**: Mesmos de GET /posts, mas `q` é obrigatório

#### `PUT /posts/{post_id}`
Editar um post.
- **Autenticação**: Obrigatória (autor ou MODERATOR/ADMIN)

#### `DELETE /posts/{post_id}`
Deletar um post.
- **Autenticação**: Obrigatória (autor ou MODERATOR/ADMIN)
- **Regra**: Moderadores não podem deletar conteúdo de ADMIN

#### `POST /posts/{post_id}/like`
Curtir um post.
- **Autenticação**: Obrigatória

---

### Comments

#### `POST /{post_id}/comments`
Criar comentário em um post.
- **Autenticação**: Obrigatória

#### `GET /{post_id}/comments`
Listar comentários de um post.
- **Query params**: `limit`, `offset`

#### `POST /comments/{comment_id}/like`
Curtir um comentário.
- **Autenticação**: Obrigatória

#### `DELETE /comments/{comment_id}`
Deletar um comentário.
- **Autenticação**: Obrigatória (autor ou MODERATOR/ADMIN)

#### `PUT /comments/{comment_id}/hide`
Ocultar um comentário.
- **Autenticação**: Obrigatória (apenas MODERATOR ou ADMIN)

---

### Categories (`/categories`)

Todas as rotas requerem autenticação de ADMIN.

#### `POST /categories` - Criar categoria
#### `PUT /categories/{cat_id}` - Editar categoria
#### `DELETE /categories/{cat_id}` - Deletar categoria

---

### Tags (`/tags`)

#### `GET /tags`
Listar todas as tags (sem autenticação).

---

### Users (`/users`)

#### `GET /users/me`
Obter perfil do usuário autenticado.
- **Autenticação**: Obrigatória

#### `PUT /users/me`
Atualizar perfil do usuário autenticado.
- **Autenticação**: Obrigatória

---

## Roles e Permissões (Community API)

- **USER**: Pode criar posts, comentários e curtir conteúdo. Pode editar/deletar apenas seu próprio conteúdo.
- **MODERATOR**: Pode deletar posts/comentários de usuários comuns (não ADMIN) e ocultar comentários.
- **ADMIN**: Todas as permissões de MODERATOR + gerenciar categorias. Não pode ter conteúdo deletado por moderadores.
