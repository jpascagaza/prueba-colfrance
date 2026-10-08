from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AlertaForm,
    CancelarParadaForm,
    ParadaForm,
    UsuarioForm,
)
from .models import Alerta, Parada


def es_operario(user):
    return user.groups.filter(name="Operario").exists()


def es_supervisor(user):
    return user.groups.filter(name="Supervisor").exists()


def es_jefe(user):
    return user.groups.filter(name="Jefe").exists()


@login_required
def inicio(request):

    usuario = request.user

    if es_operario(usuario):
        alertas = (
            Alerta.objects
            .filter(usuario=usuario)
            .select_related("maquina", "usuario")
            .order_by("-fecha")
        )

        paradas = []

    elif es_supervisor(usuario) or es_jefe(usuario):
        alertas = (
            Alerta.objects
            .select_related("maquina", "usuario")
            .order_by("-fecha")
        )

        paradas = (
            Parada.objects
            .select_related(
                "maquina",
                "usuario",
                "cancelada_por",
            )
            .order_by("-inicio")
        )

    else:
        return HttpResponseForbidden(
            "El usuario no tiene un rol asignado."
        )

    contexto = {
        "alertas": alertas,
        "paradas": paradas,
        "alerta_form": AlertaForm(),
        "parada_form": ParadaForm(),
        "cancelar_form": CancelarParadaForm(),

        "es_operario": es_operario(usuario),
        "es_supervisor": es_supervisor(usuario),
        "es_jefe": es_jefe(usuario),
    }

    return render(
        request,
        "tasks/inicio.html",
        contexto,
    )


@login_required
def crear_alerta(request):

    if not es_operario(request.user):
        return HttpResponseForbidden(
            "Solo un operario puede registrar alertas."
        )

    if request.method != "POST":
        return redirect("inicio")

    form = AlertaForm(request.POST)

    if form.is_valid():

        alerta = form.save(commit=False)

        alerta.usuario = request.user

        alerta.save()

    return redirect("inicio")


@login_required
def editar_alerta(request, alerta_id):

    if not es_supervisor(request.user):
        return HttpResponseForbidden(
            "No tiene permisos para editar alertas."
        )

    alerta = get_object_or_404(
        Alerta,
        pk=alerta_id,
    )

    if request.method != "POST":
        return redirect("inicio")

    form = AlertaForm(
        request.POST,
        instance=alerta,
    )

    if form.is_valid():
        form.save()

    return redirect("inicio")


@login_required
def crear_parada(request):

    if not es_supervisor(request.user):
        return HttpResponseForbidden(
            "Solo un supervisor puede registrar paradas."
        )

    if request.method != "POST":
        return redirect("inicio")

    form = ParadaForm(request.POST)

    if form.is_valid():

        parada = form.save(commit=False)

        parada.usuario = request.user

        parada.save()

    return redirect("inicio")


@login_required
def cancelar_parada(request, parada_id):

    if not es_jefe(request.user):
        return HttpResponseForbidden(
            "Solo un jefe puede cancelar paradas."
        )

    parada = get_object_or_404(
        Parada,
        pk=parada_id,
    )

    # Evita modificar una cancelación existente.
    if parada.cancelada:
        return redirect("inicio")

    if request.method != "POST":
        return redirect("inicio")

    form = CancelarParadaForm(request.POST)

    if form.is_valid():

        parada.cancelada = True
        parada.cancelada_por = request.user
        parada.fecha_cancelacion = timezone.now()
        parada.motivo_cancelacion = (
            form.cleaned_data["motivo_cancelacion"]
        )

        parada.save(
            update_fields=[
                "cancelada",
                "cancelada_por",
                "fecha_cancelacion",
                "motivo_cancelacion",
            ]
        )

    return redirect("inicio")
@login_required
def usuarios(request):
    if not es_jefe(request.user):
        return HttpResponseForbidden(
            "Solo un jefe puede administrar usuarios."
        )

    from django.contrib.auth.models import User

    usuarios = (
        User.objects
        .prefetch_related("groups")
        .order_by("username")
    )

    return render(
        request,
        "tasks/usuarios.html",
        {
            "usuarios": usuarios,
            "usuario_form": UsuarioForm(),
        },
    )


@login_required
def crear_usuario(request):
    if not es_jefe(request.user):
        return HttpResponseForbidden(
            "Solo un jefe puede crear usuarios."
        )

    if request.method != "POST":
        return redirect("usuarios")

    form = UsuarioForm(request.POST)

    if form.is_valid():
        form.save()

    return redirect("usuarios")