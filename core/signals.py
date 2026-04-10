from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pago

@receiver(post_save, sender=Pago)
def actualizar_deuda_si_pago_aprobado(sender, instance, created, **kwargs):
    if instance.estado == "aprobado":
        deuda = instance.deuda
        deuda.estado = "pagada"
        deuda.save()