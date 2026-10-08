# Sistema de Alertas y Paradas de Máquinas

Aplicación web desarrollada en Django como solución a la prueba técnica de Alimentos Colfrance.

El sistema permite registrar y gestionar alertas y paradas de máquinas, aplicando permisos según el rol del usuario.

## Tecnologías utilizadas

- Python
- Django 5.2.18
- SQLite
- HTML5
- CSS3
- Django Authentication
- Django Groups para manejo de roles

## Funcionalidades

### Operario

- Iniciar sesión.
- Registrar alertas de máquinas.
- Consultar únicamente las alertas registradas por él mismo.
- No puede editar alertas.
- No puede registrar paradas.
- No puede cancelar paradas.
- No puede administrar usuarios.

### Supervisor

- Iniciar sesión.
- Consultar todas las alertas.
- Editar máquina y descripción de las alertas.
- Registrar paradas de máquinas.
- Consultar las paradas registradas.
- No puede cancelar paradas.
- No puede administrar usuarios.

### Jefe

- Iniciar sesión.
- Consultar todas las alertas.
- Consultar todas las paradas.
- Cancelar paradas indicando el motivo.
- Consultar quién, cuándo y por qué se canceló una parada.
- No puede editar alertas.
- No puede registrar paradas.
- Puede administrar usuarios y asignarles un rol.

## Reglas de negocio

- La descripción de una alerta no puede estar vacía.
- El motivo de una parada no puede estar vacío.
- El motivo de cancelación no puede estar vacío.
- La fecha/hora de finalización de una parada debe ser posterior a la fecha/hora de inicio.
- La duración de una parada se calcula automáticamente en minutos.
- El cálculo permite paradas que atraviesan la medianoche. Por ejemplo, de 23:50 a 00:20 corresponde a 30 minutos.
- Una parada cancelada permanece registrada.
- La cancelación conserva el usuario que la realizó, la fecha y hora y el motivo.
- Una parada que ya fue cancelada no puede volver a cancelarse ni sobrescribir la información de la primera cancelación.
- Las restricciones de permisos se validan en el backend y no solamente en la interfaz.

## Estructura principal

```text
DJANGO/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── tasks/
│   ├── migrations/
│   ├── templates/
│   │   └── tasks/
│   │       ├── inicio.html
│   │       ├── login.html
│   │       └── usuarios.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore