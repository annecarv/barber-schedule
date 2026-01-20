import { useEffect, useState } from "react";
import { Mail, Phone, Clock, DollarSign, Calendar } from "lucide-react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";

interface Appointment {
  id: string;
  date: string;
  time: string;
  serviceName: string;
  duration: number;
  price: string;
  barberId: string;
  barberName: string;
  clientName: string;
  clientEmail: string;
  clientPhone: string;
}

function getToday() {
  const [d, m, y] = new Date()
    .toLocaleDateString("pt-BR")
    .split("/")
    .map((x) => x.padStart(2, "0"));

  return `${y}-${m}-${d}`;
}

function formatDateHeader(date: string) {
  const [y, m, d] = date.split("-").map(Number);
  const dt = new Date(y, m - 1, d);
  const today = new Date();

  today.setHours(0, 0, 0, 0);
  dt.setHours(0, 0, 0, 0);

  const isToday = dt.getTime() === today.getTime();

  const weekdays = [
    "Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado",
  ];
  const months = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez",
  ];

  const label = `${weekdays[dt.getDay()]}, ${d.toString().padStart(2, "0")} ${months[dt.getMonth()]}`;

  return isToday ? `HOJE — ${label}` : label.toUpperCase();
}

export function AdminAgenda() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const today = getToday();

  useEffect(() => {
    const stored = localStorage.getItem("appointments");
    if (!stored) return;

    try {
      const parsed: Appointment[] = JSON.parse(stored);
      const filtered = parsed
        .filter((apt) => apt.date >= today)
        .sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));

      setAppointments(filtered);
    } catch (error) {
      console.error(error);
    }
  }, [today]);

  if (appointments.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-neutral-400 gap-2 border-2 border-dashed border-neutral-200 rounded-xl bg-neutral-50/50">
        <Calendar className="w-10 h-10 opacity-20" />
        <p className="text-xs font-normal">Nenhum agendamento futuro.</p>
      </div>
    );
  }

  const grouped = appointments.reduce<Record<string, Appointment[]>>(
    (acc, apt) => {
      acc[apt.date] = acc[apt.date] || [];
      acc[apt.date].push(apt);
      return acc;
    },
    {}
  );

  const sortedDates = Object.keys(grouped).sort();

  return (
    <div className="w-full space-y-6 pb-8 pr-1">
      {sortedDates.map((date) => (
        <div key={date} className="relative">
          
          {/* CORREÇÃO DO SCROLL:
            Removi 'sticky', 'top-0', 'z-30' e 'bg-white'.
            Agora é um bloco normal que rola junto com a página (igual ao código antigo),
            mas mantendo o visual limpo do novo.
          */}
          <div className="flex items-center gap-2 mb-2 mt-4">
            <div className="h-2 w-2 rounded-full bg-amber-500 ring-2 ring-amber-100 ml-1"></div>
            <h3 className="text-xs font-medium text-neutral-500 uppercase tracking-wide">
              {formatDateHeader(date)}
            </h3>
            {/* Adicionei uma linha sutil para preencher o espaço, similar ao antigo mas mais leve */}
            <div className="h-px flex-1 bg-neutral-100 ml-2"></div>
          </div>

          <div className="grid gap-2 pl-3 border-l border-neutral-100 ml-2">
            {grouped[date].map((apt) => (
              <Card
                key={apt.id}
                /* Visual COMPACTO mantido */
                className="group flex flex-col sm:flex-row items-start sm:items-center gap-3 p-3 border-neutral-200 hover:border-amber-400 transition-all duration-200 bg-white shadow-sm"
              >
                {/* 1. HORÁRIO */}
                <div className="flex flex-row sm:flex-col items-center sm:items-center justify-center min-w-[60px] gap-2 sm:gap-0 border-b sm:border-b-0 sm:border-r border-neutral-100 pb-2 sm:pb-0 sm:pr-3">
                  <span className="text-lg font-medium text-neutral-700 tracking-tight">
                    {apt.time}
                  </span>
                  <div className="flex items-center gap-1 text-[10px] text-neutral-400 font-normal">
                    <Clock className="w-2.5 h-2.5" />
                    <span>{apt.duration}m</span>
                  </div>
                </div>

                {/* 2. CLIENTE & SERVIÇO */}
                <div className="flex-1 min-w-0 space-y-1">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium text-neutral-800 truncate text-sm">
                      {apt.clientName}
                    </h4>
                  </div>
                  
                  <p className="text-xs font-medium text-amber-600">
                    {apt.serviceName}
                  </p>

                  <div className="flex flex-wrap items-center gap-2 pt-0.5">
                    <div className="flex items-center gap-1 text-[10px] text-neutral-500 bg-neutral-50 px-2 py-0.5 rounded-md">
                      <Phone className="w-2.5 h-2.5" />
                      <span>{apt.clientPhone}</span>
                    </div>
                    
                    <div className="hidden sm:flex items-center gap-1 text-[10px] text-neutral-400">
                      <Mail className="w-2.5 h-2.5" />
                      <span className="truncate max-w-[140px]">{apt.clientEmail}</span>
                    </div>
                  </div>
                </div>

                {/* 3. PREÇO */}
                <div className="mt-1 sm:mt-0 pl-1">
                  <Badge 
                    variant="secondary" 
                    className="flex items-center gap-1 px-2 py-1 bg-green-50 text-green-700 border-green-200 text-xs font-medium hover:bg-green-100 h-6"
                  >
                    <DollarSign className="w-3 h-3" />
                    {apt.price}
                  </Badge>
                </div>
              </Card>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}