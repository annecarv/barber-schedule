import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_session, init_db
from app.models.models import Service, Barber
from app.auth import get_password_hash
from sqlmodel import select

async def seed_data():
    await init_db()

    async for session in get_session():
        result = await session.exec(select(Service))
        existing_services = result.all()

        if not existing_services:
            print("Criando servicos...")
            services = [
                Service(
                    name="Corte Simples",
                    duration="30min",
                    price="R$ 25",
                    description="Corte basico",
                    active=True
                ),
                Service(
                    name="Corte + Barba",
                    duration="1h",
                    price="R$ 50",
                    description="Corte completo com barba",
                    active=True
                ),
                Service(
                    name="Tratamento Premium",
                    duration="1h30min",
                    price="R$ 75",
                    description="Tratamento premium completo",
                    active=True
                )
            ]

            for service in services:
                session.add(service)

            await session.commit()
            print(f"Criados {len(services)} servicos")

        result_barbers = await session.exec(select(Barber))
        existing_barbers = result_barbers.all()

        if not existing_barbers:
            print("Criando barbeiros...")
            barbers = [
                Barber(
                    name="Barbeiro 1",
                    email="barbeiro1@barbearia.com.br",
                    password_hash=get_password_hash("871374"),
                    specialty="Barbas, Cortes Classicos",
                    active=True
                ),
                Barber(
                    name="Barbeiro 2",
                    email="barbeiro2@barbearia.com.br",
                    password_hash=get_password_hash("871374"),
                    specialty="Cortes Modernos",
                    active=True
                ),
                Barber(
                    name="Barbeiro 3",
                    email="barbeiro3@barbearia.com.br",
                    password_hash=get_password_hash("871374"),
                    specialty="Barbas, Cortes Classicos, Cortes Modernos",
                    active=True
                )
            ]

            for barber in barbers:
                session.add(barber)

            await session.commit()
            print(f"Criados {len(barbers)} barbeiros")

        print("\nDados criados!")
        print("\nServicos:")
        result_services = await session.exec(select(Service))
        for s in result_services.all():
            print(f"  - {s.name} ({s.duration}) - {s.price}")

        print("\nBarbeiros:")
        result_barbers = await session.exec(select(Barber))
        for b in result_barbers.all():
            print(f"  - {b.name} ({b.email})")

        print("\nCredenciais de acesso:")
        print("  Email: barbeiro1@barbearia.com.br")
        print("  Senha: 871374")

        break

if __name__ == "__main__":
    asyncio.run(seed_data())
