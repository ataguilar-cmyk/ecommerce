from django.db import models
from django.core.exceptions import ValidationError


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
    #Aqui vamoa a crear la relación del nombre con el precio, la relacioón del foreignKey
    precio = models.DecimalField(max_digits=8,
                                 decimal_places=2, validators=[validar_precio_positivo])

    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    disponible = models.BooleanField(default=True)

    # Soporte para archivos multimedia (Media Files)
    imagen = models.ImageField(upload_to='paquetes/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]
    cliente_nombre = models.CharField(max_length=100)
#Aqui vamos a agregar la relación
    paquete = models.ForeignKey(
        PaqueteTuristico,
        on_delete=models.CASCADE,
        related_name='reservas',
        null=True,
        blank=True
    )


    paquete = models.ForeignKey(PaqueteTuristico, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente_nombre} ({self.estado})"