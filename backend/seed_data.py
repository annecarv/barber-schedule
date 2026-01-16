"""Script to populate initial data for barbershop"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_session, init_db
from app.models.models import Service, Barber
from sqlmodel import select

async def seed_data():
    """Seed initial data"""
    await init_db()

    async for session in get_session():
        # Check if data already exists
        result = await session.exec(select(Service))
        existing_services = result.all()

        if not existing_services:
            print("Creating services...")
            services = [
                Service(
                    name="Serviço 1",
                    duration="30min",
                    price="R$ 25",
                    description="Corte básico",
                    active=True
                ),
                Service(
                    name="Serviço 2",
                    duration="1h",
                    price="R$ 50",
                    description="Corte completo com barba",
                    active=True
                ),
                Service(
                    name="Serviço 3",
                    duration="1h30min",
                    price="R$ 75",
                    description="Tratamento premium completo",
                    active=True
                )
            ]

            for service in services:
                session.add(service)

            await session.commit()
            print(f"Created {len(services)} services")

        # Check if barbers exist
        result_barbers = await session.exec(select(Barber))
        existing_barbers = result_barbers.all()

        if not existing_barbers:
            print("Creating barbers...")
            barbers = [
                Barber(
                    name="Barbeiro 1",
                    email="barbeiro1@barbearia.com.br",
                    specialty="Barbas, Cortes Clássicos",
                    active=True
                ),
                Barber(
                    name="Barbeiro 2",
                    email="barbeiro2@barbearia.com.br",
                    specialty="Cortes Modernos",
                    active=True
                ),
                Barber(
                    name="Barbeiro 3",
                    email="barbeiro3@barbearia.com.br",
                    specialty="Barbas, Cortes Clássicos, Cortes Modernos",
                    active=True
                )
            ]

            for barber in barbers:
                session.add(barber)

            await session.commit()
            print(f"Created {len(barbers)} barbers")

        print("\nData seeding completed!")
        print("\nServices:")
        result_services = await session.exec(select(Service))
        for s in result_services.all():
            print(f"  - {s.name} ({s.duration}) - {s.price}")

        print("\nBarbers:")
        result_barbers = await session.exec(select(Barber))
        for b in result_barbers.all():
            print(f"  - {b.name} - {b.specialty}")

        break  # Only need one session

if __name__ == "__main__":
    asyncio.run(seed_data())
