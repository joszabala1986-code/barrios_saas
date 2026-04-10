from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

# -------------------------
# MODELO BARRIO
# -------------------------

class Barrio(models.Model):
    PLAN_CHOICES = (
        ('mensual', 'Mensual'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    )
    
    nombre = models.CharField(max_length=100)
    cbu = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)

    # 👉 CONTRATO GENERAL DEL BARRIO
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)

    # ✅ NUEVO: fecha de vencimiento de la cuota
    fecha_vencimiento = models.DateField(null=True, blank=True)

    # 🏦 DATOS BANCARIOS PARA TRANSFERENCIAS
    titular_cuenta = models.CharField(max_length=150, blank=True, null=True, default="Asociación Vecinal")
    cuit = models.CharField(max_length=20, blank=True, null=True, default="30-12345678-9")
    banco = models.CharField(max_length=100, blank=True, null=True, default="Banco Nación")

    # 🆕 DATOS DE SUSCRIPCIÓN
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='mensual')
    precio_suscripcion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_inicio_suscripcion = models.DateField(null=True, blank=True)
    
    # 👤 RESPONSABLE DEL BARRIO
    responsable = models.CharField(max_length=150, blank=True, null=True, default="Administrador")

    def marcar_pagado(self):
        """Renueva la suscripción por 30 días (para plan mensual)"""
        if self.fecha_vencimiento:
            self.fecha_vencimiento += timedelta(days=30)
        else:
            self.fecha_vencimiento = timezone.now().date() + timedelta(days=30)
        
        # Actualizar fecha de inicio si es la primera vez
        if not self.fecha_inicio_suscripcion:
            self.fecha_inicio_suscripcion = timezone.now().date()
        
        self.save()

    def dias_restantes(self):
        """Calcula los días restantes de suscripción"""
        if self.fecha_vencimiento:
            return (self.fecha_vencimiento - timezone.now().date()).days
        return None
    
    def renovar_suscripcion(self, periodo='mensual'):
        """Renueva la suscripción según el período elegido"""
        hoy = timezone.now().date()
        
        if periodo == 'mensual':
            dias = 30
        elif periodo == 'semestral':
            dias = 180
        elif periodo == 'anual':
            dias = 365
        else:
            dias = 30
        
        self.fecha_vencimiento = hoy + timedelta(days=dias)
        self.fecha_inicio_suscripcion = hoy
        self.save()

    def __str__(self):
        return self.nombre


# -------------------------
# USUARIO PERSONALIZADO
# -------------------------

class Usuario(AbstractUser):

    ROLES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Administrador Barrio'),
        ('propietario', 'Propietario'),
    )

    rol = models.CharField(max_length=20, choices=ROLES)
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, null=True, blank=True)
    celular = models.CharField(max_length=20, blank=True)

    @property
    def nombre_completo(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username


# -------------------------
# MODELO PROPIEDAD
# -------------------------

class Propiedad(models.Model):
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)
    numero_lote = models.CharField(max_length=50)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    # 👉 NUEVO CAMPO
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)

    def __str__(self):
        return f"Lote {self.numero_lote} - {self.barrio.nombre}"


# -------------------------
# MODELO DEUDA
# -------------------------

class Deuda(models.Model):

    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
    )

    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=150)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"{self.concepto} - {self.propiedad}"


# -------------------------
# MODELO PAGO
# -------------------------

class Pago(models.Model):

    ESTADOS = (
        ('pendiente_validacion', 'Pendiente Validación'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )

    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE)
    comprobante = models.URLField()
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='pendiente_validacion')

    def __str__(self):
        return f"Pago - {self.deuda}"


# -------------------------
# CONTRATO
# -------------------------

class ContratoBarrio(models.Model):
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)
    archivo = models.CharField(max_length=500)  # ✅ Guarda el path, no el archivo
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrato {self.barrio.nombre}"


# -------------------------
# COMUNICADOS
# -------------------------

class Comunicado(models.Model):
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)
    mensaje = models.TextField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)  # ⚠️ Debe tener null=True
    
    def __str__(self):
        return f"Comunicado para {self.barrio.nombre} - {self.fecha}"


# -------------------------
# SUSCRIPCIÓN (mantener por compatibilidad)
# -------------------------

class SuscripcionBarrio(models.Model):
    barrio = models.OneToOneField("Barrio", on_delete=models.CASCADE)
    plan = models.CharField(max_length=50, default="basico")
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.barrio.nombre} - {self.plan}"


# -------------------------
# FACTURA
# -------------------------

class Factura(models.Model):
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    archivo = models.URLField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "facturas"


# -------------------------
# PERSONAL DE SEGURIDAD
# -------------------------
from django.conf import settings

class Seguridad(models.Model):
    barrio = models.ForeignKey('Barrio', on_delete=models.CASCADE)
    nombre_apellido = models.CharField(max_length=150)
    dni = models.CharField(max_length=20)
    edad = models.IntegerField()
    fecha_ingreso = models.DateField()
    foto_dni = models.ImageField(upload_to='dni_seguridad/', blank=True, null=True)

    # usuario para login
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_apellido} - {self.barrio.nombre}"


# -------------------------
# REGISTRO DE INGRESOS / EGRESOS
# -------------------------
class Movimiento(models.Model):
    TIPO_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )

    barrio = models.ForeignKey('Barrio', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    fecha_hora = models.DateTimeField()
    patente = models.CharField(max_length=20)
    nombre_apellido = models.CharField(max_length=150)
    dni = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True, null=True)

    registrado_por = models.ForeignKey(Seguridad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.nombre_apellido} - {self.fecha_hora}"
    

# -------------------------
# PAGO ADELANTADO
# -------------------------
class PagoAdelantado(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    meses = models.JSONField()  # lista de números: [3, 4, 5]
    anio = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    comprobante = models.URLField(null=True, blank=True)
    estado = models.CharField(max_length=30, choices=[
        ('pendiente_validacion', 'Pendiente Validación'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ], default='pendiente_validacion')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def meses_nombres(self):
        nombres = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                   'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        return [nombres[m-1] for m in self.meses]

    def __str__(self):
        return f"Adelanto Lote {self.propiedad.numero_lote} — {self.meses}"