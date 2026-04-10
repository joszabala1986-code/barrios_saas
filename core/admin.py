from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Barrio, Usuario, Propiedad, Deuda, Pago
from .models import ContratoBarrio


class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('rol', 'barrio')
        }),
    )


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Barrio)
admin.site.register(Propiedad)
admin.site.register(Deuda)
admin.site.register(Pago)
admin.site.register(ContratoBarrio)
