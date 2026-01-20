import { useEffect, useState } from "react";
import { Plus, Edit, Trash2, DollarSign, Clock, Scissors } from "lucide-react";
import { useNavigate } from "react-router";
import { Header } from "./Header";
import { AdminAgenda } from "./AdminAgenda";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import {
  getServices,
  getBarbers,
  createService,
  updateService,
  deleteService as apiDeleteService,
  createBarber,
  updateBarber,
  deleteBarber as apiDeleteBarber,
  Service,
  Barber,
} from "../services/api";

export function AdminPanel() {
  const [services, setServices] = useState<Service[]>([]);
  const [barbers, setBarbers] = useState<Barber[]>([]);
  const [loading, setLoading] = useState(true);

  const [showServiceModal, setShowServiceModal] = useState(false);
  const [editingService, setEditingService] = useState<Service | null>(null);
  const [serviceName, setServiceName] = useState("");
  const [serviceDuration, setServiceDuration] = useState("30min");
  const [servicePrice, setServicePrice] = useState("");

  const [showBarberModal, setShowBarberModal] = useState(false);
  const [editingBarber, setEditingBarber] = useState<Barber | null>(null);
  const [barberName, setBarberName] = useState("");
  const [barberSpecialty, setBarberSpecialty] = useState("");
  const [barberEmail, setBarberEmail] = useState("");
  const [barberPassword, setBarberPassword] = useState("");

  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const [showAgendaGeral, setShowAgendaGeral] = useState(false);

  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      setLoading(true);
      const [servicesData, barbersData] = await Promise.all([
        getServices(),
        getBarbers(),
      ]);
      setServices(servicesData);
      setBarbers(barbersData);
    } catch (error) {
      console.error("Erro ao carregar dados:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("logged");
    setShowLogoutModal(true);
  };

  const openServiceModal = (service?: Service) => {
    if (service) {
      setEditingService(service);
      setServiceName(service.name);
      setServiceDuration(service.duration);
      setServicePrice(service.price.replace(/[^\d]/g, ""));
    } else {
      setEditingService(null);
      setServiceName("");
      setServiceDuration("30min");
      setServicePrice("");
    }
    setShowServiceModal(true);
  };

  const saveService = async () => {
    try {
      const serviceData = {
        name: serviceName,
        duration: serviceDuration,
        price: `R$ ${servicePrice}`,
      };

      if (editingService) {
        await updateService(editingService.id, serviceData);
      } else {
        await createService(serviceData);
      }
      await fetchData();
      setShowServiceModal(false);
    } catch (error) {
      console.error("Erro ao salvar serviço:", error);
    }
  };

  const deleteService = async (id: number) => {
    try {
      await apiDeleteService(id);
      await fetchData();
    } catch (error) {
      console.error("Erro ao excluir serviço:", error);
    }
  };

  const openBarberModal = (barber?: Barber) => {
    if (barber) {
      setEditingBarber(barber);
      setBarberName(barber.name);
      setBarberSpecialty(barber.specialty || "");
      setBarberEmail(barber.email);
      setBarberPassword("");
    } else {
      setEditingBarber(null);
      setBarberName("");
      setBarberSpecialty("");
      setBarberEmail("");
      setBarberPassword("");
    }
    setShowBarberModal(true);
  };

  const saveBarber = async () => {
    try {
      if (editingBarber) {
        const updateData: { name: string; specialty: string; email: string; password?: string } = {
          name: barberName,
          specialty: barberSpecialty,
          email: barberEmail,
        };
        if (barberPassword) {
          updateData.password = barberPassword;
        }
        await updateBarber(editingBarber.id, updateData);
      } else {
        await createBarber({
          name: barberName,
          specialty: barberSpecialty,
          email: barberEmail,
          password: barberPassword,
        });
      }
      await fetchData();
      setShowBarberModal(false);
    } catch (error) {
      console.error("Erro ao salvar barbeiro:", error);
    }
  };

  const deleteBarber = async (id: number) => {
    try {
      await apiDeleteBarber(id);
      await fetchData();
    } catch (error) {
      console.error("Erro ao excluir barbeiro:", error);
    }
  };

  const averagePrice =
    services.length === 0
      ? 0
      : Math.round(
          services.reduce(
            (sum, s) => sum + Number(s.price.replace(/[^\d]/g, "")),
            0
          ) / services.length
        );

  if (loading) {
    return (
      <div className="min-h-screen bg-neutral-50">
        <Header isDashboardPage={true} onLogout={handleLogout} />
        <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
          <p className="text-neutral-600">Carregando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      <Header
        isDashboardPage={true}
        onLogout={handleLogout}
        onOpenAgendaGeral={() => setShowAgendaGeral(true)}
      />

      <Dialog open={showAgendaGeral} onOpenChange={setShowAgendaGeral}>
        <DialogContent className="max-w-7xl h-[85vh] flex flex-col p-0">
          <DialogHeader className="px-6 py-4 border-b border-neutral-200 bg-white">
            <DialogTitle>Agenda Geral</DialogTitle>
            <DialogDescription>
              Visualização completa dos agendamentos
            </DialogDescription>
          </DialogHeader>

          <div className="flex-1 overflow-auto p-6 bg-neutral-50">
            <div className="max-w-6xl mx-auto">
              <Card className="p-6 border-neutral-200 bg-white shadow-sm">
                <AdminAgenda />
              </Card>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <div className="min-h-[calc(100vh-4rem)] bg-neutral-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-neutral-900 mb-2">Painel de Administração</h1>
            <p className="text-neutral-600">
              Gerenciar serviços, preços e equipe
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <Card className="p-6 border-neutral-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-neutral-600 mb-1">Total de Serviços</p>
                  <p className="text-neutral-900">{services.length}</p>
                </div>
                <div className="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center">
                  <Scissors className="w-6 h-6 text-amber-600" />
                </div>
              </div>
            </Card>

            <Card className="p-6 border-neutral-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-neutral-600 mb-1">Barbeiros Ativos</p>
                  <p className="text-neutral-900">{barbers.length}</p>
                </div>
                <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                  <Clock className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </Card>

            <Card className="p-6 border-neutral-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-neutral-600 mb-1">
                    Preço Médio do Serviço
                  </p>
                  <p className="text-neutral-900">R$ {averagePrice}</p>
                </div>
                <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </Card>
          </div>

          <Card className="p-6">
            <Tabs defaultValue="services">
              <TabsList className="mb-6">
                <TabsTrigger value="services">Serviços</TabsTrigger>
                <TabsTrigger value="barbers">Barbeiros</TabsTrigger>
              </TabsList>

              <TabsContent value="services">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-neutral-900">Serviços</h2>
                  <Button
                    onClick={() => openServiceModal()}
                    className="bg-amber-600 hover:bg-amber-700 gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    Adicionar Serviço
                  </Button>
                </div>

                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome</TableHead>
                      <TableHead>Duração</TableHead>
                      <TableHead>Preço</TableHead>
                      <TableHead className="text-right">Ações</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {services.map((s) => (
                      <TableRow key={s.id}>
                        <TableCell>{s.name}</TableCell>
                        <TableCell>{s.duration}</TableCell>
                        <TableCell className="text-amber-600">
                          {s.price}
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex justify-end gap-2">
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => openServiceModal(s)}
                            >
                              <Edit className="w-4 h-4" />
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="text-red-600 hover:bg-red-50"
                              onClick={() => deleteService(s.id)}
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TabsContent>

              <TabsContent value="barbers">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-neutral-900">Barbeiros</h2>
                  <Button
                    onClick={() => openBarberModal()}
                    className="bg-amber-600 hover:bg-amber-700 gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    Adicionar Barbeiro
                  </Button>
                </div>

                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nome</TableHead>
                      <TableHead>Especialidade</TableHead>
                      <TableHead>E-mail</TableHead>
                      <TableHead className="text-right">Ações</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {barbers.map((b) => (
                      <TableRow key={b.id}>
                        <TableCell>{b.name}</TableCell>
                        <TableCell>{b.specialty}</TableCell>
                        <TableCell>{b.email}</TableCell>
                        <TableCell className="text-right">
                          <div className="flex justify-end gap-2">
                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() => openBarberModal(b)}
                            >
                              <Edit className="w-4 h-4" />
                            </Button>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="text-red-600 hover:bg-red-50"
                              onClick={() => deleteBarber(b.id)}
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TabsContent>
            </Tabs>
          </Card>

          <Dialog open={showServiceModal} onOpenChange={setShowServiceModal}>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>
                  {editingService ? "Editar Serviço" : "Novo Serviço"}
                </DialogTitle>
                <DialogDescription>Defina os dados do serviço</DialogDescription>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label className="mb-1 block">Nome</Label>
                  <Input
                    value={serviceName}
                    onChange={(e) => setServiceName(e.target.value)}
                  />
                </div>
                <div>
                  <Label className="mb-1 block">Duração</Label>
                  <select
                    className="w-full h-10 rounded-md border border-input bg-background px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    value={serviceDuration}
                    onChange={(e) => setServiceDuration(e.target.value)}
                  >
                    <option value="30min">30min</option>
                    <option value="1h">1h</option>
                    <option value="1h30min">1h30min</option>
                  </select>
                </div>
                <div>
                  <Label className="mb-1 block">Preço</Label>
                  <Input
                    type="number"
                    value={servicePrice}
                    onChange={(e) => setServicePrice(e.target.value)}
                  />
                </div>
              </div>
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setShowServiceModal(false)}
                >
                  Cancelar
                </Button>
                <Button
                  className="bg-amber-600 hover:bg-amber-700"
                  onClick={saveService}
                  disabled={!serviceName || !servicePrice}
                >
                  Salvar
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          <Dialog open={showBarberModal} onOpenChange={setShowBarberModal}>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>
                  {editingBarber ? "Editar Barbeiro" : "Novo Barbeiro"}
                </DialogTitle>
                <DialogDescription>
                  Defina os dados de acesso do barbeiro
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label className="mb-1 block">Nome</Label>
                  <Input
                    value={barberName}
                    onChange={(e) => setBarberName(e.target.value)}
                  />
                </div>
                <div>
                  <Label className="mb-1 block">Especialidade</Label>
                  <Input
                    value={barberSpecialty}
                    onChange={(e) => setBarberSpecialty(e.target.value)}
                  />
                </div>
                <div>
                  <Label className="mb-1 block">E-mail</Label>
                  <Input
                    type="email"
                    value={barberEmail}
                    onChange={(e) => setBarberEmail(e.target.value)}
                  />
                </div>
                <div>
                  <Label className="mb-1 block">
                    {editingBarber ? "Nova Senha (deixe vazio para manter)" : "Senha"}
                  </Label>
                  <Input
                    type="password"
                    value={barberPassword}
                    onChange={(e) => setBarberPassword(e.target.value)}
                  />
                </div>
              </div>
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setShowBarberModal(false)}
                >
                  Cancelar
                </Button>
                <Button
                  className="bg-amber-600 hover:bg-amber-700"
                  onClick={saveBarber}
                  disabled={
                    !barberName ||
                    !barberSpecialty ||
                    !barberEmail ||
                    (!editingBarber && !barberPassword)
                  }
                >
                  Salvar
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {showLogoutModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
          <div className="bg-white w-full max-w-md rounded-2xl shadow-xl p-8 animate-fadeIn">
            <h2 className="text-2xl font-semibold text-[#1A1A1A] text-center mb-4">
              Você saiu!
            </h2>

            <p className="text-gray-600 text-center mb-8">
              Logout realizado com sucesso.
            </p>

            <Button
              onClick={() => navigate("/")}
              className="w-full bg-[#E67E22] hover:bg-[#D35400] text-white text-lg py-6 rounded-xl"
            >
              OK
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
