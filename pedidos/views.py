from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.response import Response

from pedidos.dao.vuelasdao import PaqueteTuristicoDAO, ReservaDAO
from pedidos.serializers import PaqueteTuristicoSerializer, ReservaSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def es_operador(user):
    """Verifica si el usuario autenticado pertenece al grupo 'Operador' o es Staff/Admin"""
    return user.is_authenticated and (user.groups.filter(name='Operador').exists() or user.is_staff)


# ==========================================
# 1. VISTAS WEB (HTML)
# ==========================================

def catalogo_view(request):
    """Muestra el catálogo de paquetes al cliente utilizando el DAO"""
    paquetes = PaqueteTuristicoDAO.obtener_disponibles()
    return render(request, 'mainvista/catalogo.html', {'paquetes': paquetes})

@login_required
@user_passes_test(es_operador, login_url='/admin/login/')
def reservas_view(request):
    """Muestra las reservas activas al Operador utilizando el DAO"""
    reservas_activas = ReservaDAO.obtener_activas()
    return render(request, 'mainvista/reservas.html', {'reservas': reservas_activas})

def crear_reserva_action(request):
    """Procesa el formulario web de una nueva reserva"""
    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente_nombre', '').strip()
        paquete_id = request.POST.get('paquete_id')

        if cliente_nombre and paquete_id:
            reserva = ReservaDAO.crear_reserva_con_paquete(cliente_nombre, int(paquete_id))
            if reserva:
                messages.success(request, f"¡Reserva registrada a nombre de {cliente_nombre}!")
            else:
                messages.error(request, "Ocurrió un problema al registrar el paquete.")
        else:
            messages.error(request, "Por favor ingresa tu nombre para procesar la reserva.")

    return redirect('catalogo')

@login_required
@user_passes_test(es_operador, login_url='/admin/login/')
def cambiar_estado_action(request, reserva_id):
    """Actualiza el estado de una reserva desde la vista web"""
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        ReservaDAO.cambiar_estado(reserva_id, nuevo_estado)
    return redirect('reservas')

def login_view(request):
    """Muestra y procesa el formulario de inicio de sesión"""
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('catalogo')
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
        paquetes = PaqueteTuristicoDAO.obtener_todos()
        serializer = PaqueteTuristicoSerializer(paquetes, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PaqueteTuristicoSerializer(data=request.data)
        if serializer.is_valid():
            paquete = PaqueteTuristicoDAO.crear(serializer.validated_data)
            return Response(PaqueteTuristicoSerializer(paquete).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        paquete = PaqueteTuristicoDAO.actualizar(pk, request.data)
        if paquete is None:
            return Response({'detail': 'Paquete no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PaqueteTuristicoSerializer(paquete).data)

    def destroy(self, request, pk=None):
        eliminado = PaqueteTuristicoDAO.eliminar(pk)
        if not eliminado:
            return Response({'detail': 'Paquete no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservaViewSet(viewsets.ViewSet):

    def list(self, request):
        reservas = ReservaDAO.obtener_todos()
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

    def create(self, request):
        cliente_nombre = request.data.get('cliente_nombre')
        paquete_id = request.data.get('paquete_id')

        if not cliente_nombre or not paquete_id:
            return Response(
                {"error": "Se requieren cliente_nombre y paquete_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        reserva = ReservaDAO.crear_reserva_con_paquete(cliente_nombre, int(paquete_id))
        if reserva:
            serializer = ReservaSerializer(reserva)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "Paquete no encontrado o no disponible"},
            status=status.HTTP_404_NOT_FOUND
        )

    def update(self, request, pk=None):
        nuevo_estado = request.data.get('estado')
        reserva = ReservaDAO.cambiar_estado(pk, nuevo_estado)
        if reserva is None:
            return Response({'detail': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ReservaSerializer(reserva).data)

    def destroy(self, request, pk=None):
        eliminado = ReservaDAO.eliminar(pk)
        if not eliminado:
            return Response({'detail': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)