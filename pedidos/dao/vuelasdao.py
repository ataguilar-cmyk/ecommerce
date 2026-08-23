from typing import List, Optional
from pedidos.models import PaqueteTuristico, Reserva


class PaqueteTuristicoDAO:
    """Capa DAO para operaciones de Paquetes Turísticos"""

    @staticmethod
    def obtener_todos() -> List[PaqueteTuristico]:
        return PaqueteTuristico.objects.all()

    @staticmethod
    def obtener_disponibles() -> List[PaqueteTuristico]:
        return PaqueteTuristico.objects.filter(disponible=True)

    @staticmethod
    def obtener_por_id(paquete_id: int) -> Optional[PaqueteTuristico]:
        try:
            return PaqueteTuristico.objects.get(id=paquete_id)
        except PaqueteTuristico.DoesNotExist:
            return None

    @staticmethod
    def crear(datos: dict) -> PaqueteTuristico:
        return PaqueteTuristico.objects.create(**datos)

    @staticmethod
    def actualizar(paquete_id: int, datos: dict) -> Optional[PaqueteTuristico]:
        paquete = PaqueteTuristicoDAO.obtener_por_id(paquete_id)
        if paquete:
            for campo, valor in datos.items():
                setattr(paquete, campo, valor)
            paquete.save()
        return paquete

    @staticmethod
    def eliminar(paquete_id: int) -> bool:
        paquete = PaqueteTuristicoDAO.obtener_por_id(paquete_id)
        if paquete:
            paquete.delete()
            return True
        return False


class ReservaDAO:
    """Capa DAO para operaciones de Reservas"""

    @staticmethod
    def obtener_todos() -> List[Reserva]:
        return Reserva.objects.all().order_by('-fecha')

    @staticmethod
    def crear_reserva_con_paquete(cliente_nombre: str, paquete_id: int) -> Optional[Reserva]:
        paquete = PaqueteTuristicoDAO.obtener_por_id(paquete_id)
        if paquete:
            return Reserva.objects.create(
                cliente_nombre=cliente_nombre,
                paquete=paquete,
                total=paquete.precio
            )
        return None

    @staticmethod
    def cambiar_estado(reserva_id: int, nuevo_estado: str) -> Optional[Reserva]:
        try:
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.estado = nuevo_estado
            reserva.save()
            return reserva
        except Reserva.DoesNotExist:
            return None

    @staticmethod
    def eliminar(reserva_id: int) -> bool:
        try:
            Reserva.objects.get(id=reserva_id).delete()
            return True
        except Reserva.DoesNotExist:
            return False