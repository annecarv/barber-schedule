# BarberSchedule Lite

Este é o código-fonte do **BarberSchedule Lite**, uma aplicação front-end simples, desenvolvida com **React** e **Vite**.

O projeto inclui:

- Página inicial (landing page).  
- Sistema de agendamento. 
- Tela de login.  
- Dashboard dos profissionais, com exibição dos agendamentos. 
- Componentes do design, baseados no layout do Figma.  

Design original no Figma:

https://www.figma.com/pt-br/comunidade/file/1578834151539150314/barberschedule-lite
---

## 🚀 Tecnologias Utilizadas:

- **React + TypeScript**.
- **Vite**.
- **TailwindCSS**.
- **Shadcn/UI**.
- **Lucide Icons**.

---

## 🔧 Como Instalar e Rodar?

Dentro da pasta do projeto, (após o `git clone`):

### 1. Instale as dependências:

```
npm install
```

### 2. Rode o servidor de desenvolvimento:

```
npm run dev
```

O projeto abrirá em:

👉 http://localhost:5173/ (ou porta similar)

---

## 🔐 Sobre o Login (IMPORTANTE):

A tela de login permite acesso apenas ao **modo profissional**.

Atualmente **não há cadastro**, e o único usuário permitido é o que está definido diretamente no código.

As credenciais são:

```
E-mail: barbeiro1@barbearia.com.br

Senha: 871374
```

Qualquer valor diferente disso fará o login falhar.

---

## 📁 Estrutura Geral:

As principais partes do projeto incluem:

- `LandingPage` – Página Inicial.  
- `BookingPage` – Fluxo de Agendamento.  
- `LoginPage` – Autenticação.  
- `ProfessionalDashboard` – Painel com Agendamentos.

- Componentes UI organizados em `/components/ui`

---

## 📌 Observações:

- Todos os agendamentos e dados de login são armazenados via **localStorage**.  
- O projeto serve como **prototipação/demonstração**.
- Direiros são reservados! Ladrões de código serão processados.