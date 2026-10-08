from django import forms

from .models import Alerta, Parada


class AlertaForm(forms.ModelForm):

    class Meta:
        model = Alerta
        fields = ["maquina", "descripcion"]

        widgets = {
            "descripcion": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Describa la alerta..."
                }
            ),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion", "")

        if not descripcion.strip():
            raise forms.ValidationError(
                "La descripción no puede estar vacía."
            )

        return descripcion.strip()


class ParadaForm(forms.ModelForm):

    class Meta:
        model = Parada
        fields = [
            "maquina",
            "inicio",
            "fin",
            "motivo",
        ]

        widgets = {
            "inicio": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "fin": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "motivo": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Motivo de la parada..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["inicio"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]

        self.fields["fin"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]

    def clean_motivo(self):
        motivo = self.cleaned_data.get("motivo", "")

        if not motivo.strip():
            raise forms.ValidationError(
                "El motivo no puede estar vacío."
            )

        return motivo.strip()

    def clean(self):
        cleaned_data = super().clean()

        inicio = cleaned_data.get("inicio")
        fin = cleaned_data.get("fin")

        if inicio and fin and fin <= inicio:
            self.add_error(
                "fin",
                "La finalización debe ser posterior al inicio."
            )

        return cleaned_data


class CancelarParadaForm(forms.Form):

    motivo_cancelacion = forms.CharField(
        label="Motivo de cancelación",
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "placeholder": "Indique el motivo..."
            }
        ),
    )

    def clean_motivo_cancelacion(self):
        motivo = self.cleaned_data.get(
            "motivo_cancelacion",
            ""
        )

        if not motivo.strip():
            raise forms.ValidationError(
                "El motivo de cancelación no puede estar vacío."
            )

        return motivo.strip()

from django.contrib.auth.models import User, Group


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        min_length=6,
    )

    rol = forms.ModelChoiceField(
        label="Rol",
        queryset=Group.objects.filter(
            name__in=["Operario", "Supervisor", "Jefe"]
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password", "rol"]

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Ese nombre de usuario ya existe."
            )

        return username

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.set_password(
            self.cleaned_data["password"]
        )

        usuario.is_active = True

        if commit:
            usuario.save()

            usuario.groups.clear()
            usuario.groups.add(
                self.cleaned_data["rol"]
            )

        return usuario