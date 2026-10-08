from django.db import models
from django.contrib.auth.models import User


class Maquina(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Alerta(models.Model):
    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.PROTECT
    )
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.maquina} - {self.descripcion[:50]}"


class Parada(models.Model):
    maquina = models.ForeignKey(
        Maquina,
        on_delete=models.PROTECT
    )
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    motivo = models.TextField()
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="paradas_registradas"
    )

    # Información de cancelación
    cancelada = models.BooleanField(default=False)
    cancelada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="paradas_canceladas"
    )
    fecha_cancelacion = models.DateTimeField(
        null=True,
        blank=True
    )
    motivo_cancelacion = models.TextField(
        blank=True
    )

    @property
    def duracion_minutos(self):
        """
        Calcula la duración total de la parada en minutos.
        También funciona cuando la parada cruza la medianoche.
        """
        diferencia = self.fin - self.inicio
        return int(diferencia.total_seconds() / 60)

    def __str__(self):
        return f"{self.maquina} - {self.inicio}"