from django.urls import path
from . import views


urlpatterns = [
    path("", views.inicio, name="inicio"),

    path(
        "alertas/crear/",
        views.crear_alerta,
        name="crear_alerta",
    ),

    path(
        "alertas/<int:alerta_id>/editar/",
        views.editar_alerta,
        name="editar_alerta",
    ),

    path(
        "paradas/crear/",
        views.crear_parada,
        name="crear_parada",
    ),

    path(
        "paradas/<int:parada_id>/cancelar/",
        views.cancelar_parada,
        name="cancelar_parada",
    ),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
]