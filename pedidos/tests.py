from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PaqueteTuristico, Reserva
from pedidos.dao.vuelasdao import PaqueteTuristicoDAO, ReservaDAO


class SmokeTests(TestCase):
    def setUp(self):
        """Configuración de datos iniciales para la prueba"""
        self.paquete = PaqueteTuristico.objects.create(
            nombre="Tulum Playa",
            destino="Quintana Roo",
            precio=5000.00,
            categoria="PLAYA",
            disponible=True
        )
        self.user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='password123'
        )

    def test_creacion_paquete(self):
        """Verifica que el paquete se guarde correctamente en la base de datos"""
        self.assertEqual(PaqueteTuristico.objects.count(), 1)
        self.assertEqual(self.paquete.nombre, "Tulum Playa")

    def test_creacion_reserva(self):
        """Verifica la creación de una reserva asociada a un cliente y paquete"""
        reserva = Reserva.objects.create(
            cliente_nombre="Yuri Paez",
            paquete=self.paquete,
            estado="PENDIENTE",
            total=5000.00
        )
        self.assertEqual(Reserva.objects.count(), 1)
        self.assertEqual(reserva.cliente_nombre, "Yuri Paez")

    def test_acceso_admin_importar_csv(self):
        """Verifica que la vista del cargue masivo responda correctamente (HTTP 200)"""
        self.client.login(username='admin_test', password='password123')
        response = self.client.get('/admin/pedidos/paqueteturistico/importar-csv/')
        self.assertEqual(response.status_code, 200)


class ViajesTestCase(TestCase):
    def setUp(self):
        self.paquete = PaqueteTuristico.objects.create(
            nombre="Cancún Todo Incluido",
            destino="Quintana Roo",
            precio=5000.00,
            disponible=True,
            categoria="PLAYA"
        )

    def test_crear_reserva_dao(self):
        reserva = ReservaDAO.crear_reserva_con_paquete("Carlos", self.paquete.id)
        self.assertIsNotNone(reserva)
        self.assertEqual(reserva.cliente_nombre, "Carlos")
        self.assertEqual(reserva.total, 5000.00)

    def test_cambiar_estado_dao(self):
        reserva = ReservaDAO.crear_reserva_con_paquete("Ana", self.paquete.id)
        reserva_actualizada = ReservaDAO.cambiar_estado(reserva.id, "CONFIRMADA")
        self.assertEqual(reserva_actualizada.estado, "CONFIRMADA")

    def test_api_list_paquetes(self):
        response = self.client.get('/api/paquetes/')
        self.assertEqual(response.status_code, 200)

    def test_crear_reserva_action_web(self):
        datos = {'cliente_nombre': 'Yuri', 'paquete_id': self.paquete.id}
        response = self.client.post(reverse('crear_reserva'), datos)
        self.assertRedirects(response, reverse('catalogo'))
        self.assertEqual(Reserva.objects.count(), 1)