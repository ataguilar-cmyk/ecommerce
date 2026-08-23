from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/paquetes', views.PaqueteTuristicoViewSet, basename='api_paquetes')
router.register(r'api/reservas', views.ReservaViewSet, basename='api_reservas')

urlpatterns = [
    # Rutas Web (HTML)
    path('', views.menu_view, name='menu'),
    path('cocina/', views.cocina_view, name='cocina'),
    path('reserva/nueva/', views.crear_reserva_action, name='crear_reserva'),
    path('reserva/<int:reserva_id>/estado/', views.cambiar_estado_action, name='cambiar_estado'),
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),

    # Rutas API
    path('', include(router.urls)),

]