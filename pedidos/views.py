from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response

from pedidos.dao.vuelasdao import PaqueteTuristicoDAO, ReservaDAO
from pedidos.serializers import PaqueteTuristicoSerializer, ReservaSerializer

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# ==========================================
# 1. VISTAS WEB (HTML)
# ==========================================

def menu_view(request):
    """Muestra el catálogo de paquetes al cliente utilizando el DAO"""
    paquetes = PaqueteTuristicoDAO.obtener_disponibles()
    return render(request, 'mainvista/menu.html', {'paquetes': paquetes})

def cocina_view(request):
    """Muestra las reservas activas al Operador utilizando el DAO"""
    reservas = ReservaDAO.obtener_todos()
    return render(request, 'mainvista/cocina.html', {'reservas': reservas})

def crear_reserva_action(request):
    """Procesa el formulario web de una nueva reserva"""
    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente_nombre')
        paquete_id = request.POST.get('paquete_id')
        ReservaDAO.crear_reserva_con_paquete(cliente_nombre, paquete_id)
    return redirect('cocina')

def cambiar_estado_action(request, reserva_id):
    """Actualiza el estado de una reserva desde la vista web"""
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        ReservaDAO.cambiar_estado(reserva_id, nuevo_estado)
    return redirect('cocina')


# ... (tus imports y vistas existentes se quedan igual) ...

def login_view(request):
    """Muestra y procesa el formulario de inicio de sesión"""
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('menu')
        error = 'Usuario o contraseña incorrectos'
    return render(request, 'mainvista/login.html', {'error': error})

def logout_view(request):
    """Cierra la sesión del usuario"""
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def perfil_view(request):
    """Muestra el perfil del usuario autenticado y sus reservas"""
    mis_reservas = ReservaDAO.obtener_por_cliente(request.user.username)
    return render(request, 'mainvista/perfil.html', {'reservas': mis_reservas})

# ==========================================
# 2. VISTAS API REST (JSON)
# ==========================================

class PaqueteTuristicoViewSet(viewsets.ViewSet):

    def list(self, request):
        """Consultas: GET /api/paquetes/"""
        paquetes = PaqueteTuristicoDAO.obtener_todos()
        serializer = PaqueteTuristicoSerializer(paquetes, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Altas: POST /api/paquetes/"""
        serializer = PaqueteTuristicoSerializer(data=request.data)
        if serializer.is_valid():
            paquete = PaqueteTuristicoDAO.crear(serializer.validated_data)
            return Response(PaqueteTuristicoSerializer(paquete).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Cambios: PUT /api/paquetes/{id}/"""
        paquete = PaqueteTuristicoDAO.actualizar(pk, request.data)
        if paquete is None:
            return Response({'detail': 'Paquete no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PaqueteTuristicoSerializer(paquete).data)

    def destroy(self, request, pk=None):
        """Bajas: DELETE /api/paquetes/{id}/"""
        eliminado = PaqueteTuristicoDAO.eliminar(pk)
        if not eliminado:
            return Response({'detail': 'Paquete no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservaViewSet(viewsets.ViewSet):

    def list(self, request):
        """Consultas: GET /api/reservas/"""
        reservas = ReservaDAO.obtener_todos()
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Altas: POST /api/reservas/"""
        cliente_nombre = request.data.get('cliente_nombre')
        paquete_id = request.data.get('paquete_id') or request.data.get('paquete')
        reserva = ReservaDAO.crear_reserva_con_paquete(cliente_nombre, paquete_id)
        if reserva is None:
            return Response({'detail': 'Paquete no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ReservaSerializer(reserva).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Cambios: PUT /api/reservas/{id}/ (cambia el estado)"""
        nuevo_estado = request.data.get('estado')
        reserva = ReservaDAO.cambiar_estado(pk, nuevo_estado)
        if reserva is None:
            return Response({'detail': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ReservaSerializer(reserva).data)

    def destroy(self, request, pk=None):
        """Bajas: DELETE /api/reservas/{id}/"""
        eliminado = ReservaDAO.eliminar(pk)
        if not eliminado:
            return Response({'detail': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)