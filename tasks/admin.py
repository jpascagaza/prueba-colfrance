from django.contrib import admin
from .models import Task  # <-- Debe coincidir exactamente con el nombre de la clase

admin.site.register(Task)
