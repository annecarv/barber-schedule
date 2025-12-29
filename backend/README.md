Backend FastAPI - Plataforma de Comunidade

Pré-requisitos
- Python 3.10+
- Criar um virtualenv

Instalação

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Variáveis de ambiente (exemplo `.env`)

```env
AUTH0_DOMAIN=your-domain.auth0.com
API_AUDIENCE=your-audience
ALGORITHMS=RS256
DATABASE_URL=sqlite+aiosqlite:///./dev.db
```

Rodar a aplicação

```bash
uvicorn app.main:app --reload --port 8000
```

Observações
- A API valida JWTs emitidos pelo Auth0 utilizando o JWKS do domínio.
- Perfis/roles são extraídos do claim `roles` (se estiverem no token). Adapte conforme seu issuer.
- Banco padrão: SQLite (zero-config) conforme enunciado.
