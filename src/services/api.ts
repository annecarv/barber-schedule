const API_BASE_URL = 'http://localhost:8000/api';

export interface Service {
  id: number;
  name: string;
  duration: string;
  price: string;
  description?: string;
  active: boolean;
  created_at: string;
}

export interface Barber {
  id: number;
  name: string;
  email: string;
  specialty?: string;
  active: boolean;
  created_at: string;
}

export interface Booking {
  id: number;
  customer_name: string;
  customer_email?: string;
  customer_phone?: string;
  service_id: number;
  service_name: string;
  service_duration: string;
  service_price: string;
  barber_id: number;
  barber_name: string;
  booking_date: string;
  booking_time: string;
  status: string;
  created_at: string;
  updated_at?: string;
}

export interface BookingCreate {
  customer_name: string;
  customer_email?: string;
  customer_phone?: string;
  service_id: number;
  barber_id: number;
  booking_date: string;
  booking_time: string;
}

export const getServices = async (): Promise<Service[]> => {
  const response = await fetch(`${API_BASE_URL}/services`);
  if (!response.ok) throw new Error('Failed to fetch services');
  return response.json();
};

export const getService = async (id: number): Promise<Service> => {
  const response = await fetch(`${API_BASE_URL}/services/${id}`);
  if (!response.ok) throw new Error('Failed to fetch service');
  return response.json();
};

export const getBarbers = async (): Promise<Barber[]> => {
  const response = await fetch(`${API_BASE_URL}/barbers`);
  if (!response.ok) throw new Error('Failed to fetch barbers');
  return response.json();
};

export const getBarber = async (id: number): Promise<Barber> => {
  const response = await fetch(`${API_BASE_URL}/barbers/${id}`);
  if (!response.ok) throw new Error('Failed to fetch barber');
  return response.json();
};

export const createBooking = async (booking: BookingCreate): Promise<Booking> => {
  const response = await fetch(`${API_BASE_URL}/bookings`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(booking),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create booking');
  }

  return response.json();
};

export const getAvailableTimes = async (
  barberId: number,
  date: string,
  serviceId: number
): Promise<string[]> => {
  const params = new URLSearchParams({
    barber_id: barberId.toString(),
    date: date,
    service_id: serviceId.toString(),
  });

  const response = await fetch(`${API_BASE_URL}/bookings/available-times?${params}`);
  if (!response.ok) throw new Error('Failed to fetch available times');

  const data = await response.json();
  return data.available_times;
};

export const getBookings = async (
  barberId?: number,
  date?: string,
  status?: string
): Promise<Booking[]> => {
  const params = new URLSearchParams();
  if (barberId) params.append('barber_id', barberId.toString());
  if (date) params.append('date', date);
  if (status) params.append('status', status);

  const response = await fetch(`${API_BASE_URL}/bookings?${params}`);
  if (!response.ok) throw new Error('Failed to fetch bookings');

  return response.json();
};

export const getBooking = async (id: number): Promise<Booking> => {
  const response = await fetch(`${API_BASE_URL}/bookings/${id}`);
  if (!response.ok) throw new Error('Failed to fetch booking');
  return response.json();
};

export const cancelBooking = async (id: number): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/bookings/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Failed to cancel booking');
};
