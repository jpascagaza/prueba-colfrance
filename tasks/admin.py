from django.contrib import admin
from .models import Maquina, Alerta, Parada


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("id", "maquina", "usuario", "fecha", "descripcion")
    list_filter = ("maquina", "usuario", "fecha")
    search_fields = ("descripcion",)


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "maquina",
        "usuario",
        "inicio",
        "fin",
        "duracion",
        "cancelada",
    )
    list_filter = ("maquina", "usuario", "cancelada")

    @admin.display(description="Duración (min)")
    def duracion(self, obj):
        return obj.duracion_minutos
