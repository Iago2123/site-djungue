from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('reservar/<int:pacote_id>/', views.realizar_reserva, name='realizar_reserva'),
]