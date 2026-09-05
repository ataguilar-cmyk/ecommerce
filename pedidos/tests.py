from django.test import TestCase
from django.contrib.auth.models import User
from .models import PaqueteTuristico, Reserva


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