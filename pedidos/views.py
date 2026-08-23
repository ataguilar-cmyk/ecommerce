from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response

from pedidos.dao.viajesdao import PaqueteTuristicoDAO, ReservaDAO
from pedidos.serializers import PaqueteTuristicoSerializer, ReservaSerializer

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


# ======================================