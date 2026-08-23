from typing import List, Optional
from paquetes.models import PaqueteTuristico, Reserva

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