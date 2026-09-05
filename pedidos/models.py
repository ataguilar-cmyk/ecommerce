from django.db import models
from django.core.exceptions import validationError
# Create your models here.
from django.db import models


#Django ORM- Crear
def validar_precio_positivo(value):
    if value <= 0:
        raise ValidationError('El precio debe ser un número mayor a cero.')

class PaqueteTuristico(models.Model):
    CATEGORIAS = [
        ('PLAYA', 'Playa'),
        ('AVENTURA', 'Aventura'),
        ('CULTURAL', 'Cultural'),
    ]
    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    disponible = models.BooleanField(default=True)

# Soporte para archivos multimedia (Media Files)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]
    cliente_nombre = models.CharField(max_length=100)
    paquete = models.ForeignKey(PaqueteTuristico, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente_nombre} ({self.estado})"

        