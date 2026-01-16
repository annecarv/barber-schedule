# 📚 Exemplo de Integração do Frontend com o Backend

## Como modificar o BookingPage para usar o backend

### Antes (usando localStorage):

```typescript
const SERVICES = [
  { id: "service1", name: "Serviço 1", duration: "30min", price: "R$ 25" },
  // ...
];

const BARBERS = [
  { id: "barber1", name: "Barbeiro 1", specialty: "Barbas, Cortes Clássicos" },
  // ...
];
```

### Depois (usando o backend):

```typescript
import { useEffect, useState } from "react";
import { getServices, getBarbers, getAvailableTimes, createBooking, Service, Barber } from "../services/api";

function BookingPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [barbers, setBarbers] = useState<Barber[]>([]);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [selectedBarber, setSelectedBarber] = useState<Barber | null>(null);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(undefined);
  const [selectedTime, setSelectedTime] = useState<string | null>(null);
  const [availableTimes, setAvailableTimes] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  // Carregar serviços e barbeiros quando o componente montar
  useEffect(() => {
    const loadData = async () => {
      try {
        const [servicesData, barbersData] = await Promise.all([
          getServices(),
          getBarbers()
        ]);
        setServices(servicesData);
        setBarbers(barbersData);
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
      }
    };

    loadData();
  }, []);

  // Carregar horários disponíveis quando serviço, barbeiro e data forem selecionados
  useEffect(() => {
    const loadAvailableTimes = async () => {
      if (selectedService && selectedBarber && selectedDate) {
        try {
          setLoading(true);
          const dateStr = selectedDate.toISOString().split('T')[0]; // YYYY-MM-DD
          const times = await getAvailableTimes(
            selectedBarber.id,
            dateStr,
            selectedService.id
          );
          setAvailableTimes(times);
        } catch (error) {
          console.error("Erro ao carregar horários:", error);
        } finally {
          setLoading(false);
        }
      }
    };

    loadAvailableTimes();
  }, [selectedService, selectedBarber, selectedDate]);

  // Função para finalizar o agendamento
  const handleConfirmBooking = async () => {
    if (!selectedService || !selectedBarber || !selectedDate || !selectedTime) {
      alert("Por favor, preencha todos os campos");
      return;
    }

    try {
      setLoading(true);

      const dateStr = selectedDate.toISOString().split('T')[0];

      const booking = await createBooking({
        customer_name: "Nome do Cliente", // Pegar de um formulário
        customer_email: "cliente@email.com", // Opcional
        customer_phone: "(11) 98765-4321", // Opcional
        service_id: selectedService.id,
        barber_id: selectedBarber.id,
        booking_date: dateStr,
        booking_time: selectedTime
      });

      alert(`Agendamento confirmado! ID: ${booking.id}`);
      // Redirecionar ou limpar formulário
    } catch (error: any) {
      alert(`Erro: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Renderizar lista de serviços */}
      <div>
        <h3>Serviços</h3>
        {services.map(service => (
          <div
            key={service.id}
            onClick={() => setSelectedService(service)}
            className={selectedService?.id === service.id ? "selected" : ""}
          >
            <h4>{service.name}</h4>
            <p>{service.duration} - {service.price}</p>
            {service.description && <p>{service.description}</p>}
          </div>
        ))}
      </div>

      {/* Renderizar lista de barbeiros */}
      <div>
        <h3>Barbeiros</h3>
        {barbers.map(barber => (
          <div
            key={barber.id}
            onClick={() => setSelectedBarber(barber)}
            className={selectedBarber?.id === barber.id ? "selected" : ""}
          >
            <h4>{barber.name}</h4>
            <p>{barber.specialty}</p>
          </div>
        ))}
      </div>

      {/* Calendário de data */}
      <Calendar
        mode="single"
        selected={selectedDate}
        onSelect={setSelectedDate}
      />

      {/* Horários disponíveis */}
      <div>
        <h3>Horários Disponíveis</h3>
        {loading ? (
          <p>Carregando...</p>
        ) : (
          <div>
            {availableTimes.map(time => (
              <button
                key={time}
                onClick={() => setSelectedTime(time)}
                className={selectedTime === time ? "selected" : ""}
              >
                {time}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Botão de confirmar */}
      <button
        onClick={handleConfirmBooking}
        disabled={!selectedService || !selectedBarber || !selectedDate || !selectedTime || loading}
      >
        {loading ? "Confirmando..." : "Confirmar Agendamento"}
      </button>
    </div>
  );
}
```

## Modificar o ProfessionalDashboard

```typescript
import { useEffect, useState } from "react";
import { getBookings, Booking } from "../services/api";

function ProfessionalDashboard() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadBookings = async () => {
      try {
        setLoading(true);
        const dateStr = selectedDate.toISOString().split('T')[0];

        // Carregar agendamentos do barbeiro logado
        // Por enquanto, vamos usar barberId = 1
        const data = await getBookings(1, dateStr);
        setBookings(data);
      } catch (error) {
        console.error("Erro ao carregar agendamentos:", error);
      } finally {
        setLoading(false);
      }
    };

    loadBookings();
  }, [selectedDate]);

  return (
    <div>
      <h2>Meus Agendamentos</h2>

      {/* Calendário para selecionar data */}
      <Calendar
        mode="single"
        selected={selectedDate}
        onSelect={(date) => date && setSelectedDate(date)}
      />

      {/* Lista de agendamentos */}
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <div>
          {bookings.length === 0 ? (
            <p>Nenhum agendamento para esta data</p>
          ) : (
            bookings.map(booking => (
              <div key={booking.id} className="booking-card">
                <h3>{booking.booking_time}</h3>
                <p><strong>Cliente:</strong> {booking.customer_name}</p>
                <p><strong>Serviço:</strong> {booking.service_name}</p>
                <p><strong>Duração:</strong> {booking.service_duration}</p>
                <p><strong>Valor:</strong> {booking.service_price}</p>
                <p><strong>Status:</strong> {booking.status}</p>
                {booking.customer_phone && (
                  <p><strong>Telefone:</strong> {booking.customer_phone}</p>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
```

## Próximos Passos

1. **Remover localStorage**: Deletar ou comentar todo código relacionado a `localStorage`
2. **Adicionar formulário de cliente**: Coletar nome, email e telefone do cliente
3. **Tratamento de erros**: Adicionar toast notifications para erros
4. **Loading states**: Melhorar UX com skeletons/spinners
5. **Autenticação**: Integrar login do barbeiro para saber qual barbeiro está logado

## URLs Importantes

- **Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

## Testando

1. Certifique-se que o backend está rodando: `uvicorn app.main:app --reload --port 8000`
2. Inicie o frontend: `npm run dev`
3. Acesse: http://localhost:5173
