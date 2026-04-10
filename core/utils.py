# utils.py — CORREGIDO
from supabase import create_client
from django.conf import settings
import uuid
import mimetypes

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# ✅ Bucket PÚBLICO — comprobantes de pago
def subir_comprobante(file):
    extension = file.name.split('.')[-1].lower()
    nombre_archivo = f"{uuid.uuid4()}.{extension}"
    content_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'

    supabase.storage.from_('comprobantes').upload(
        nombre_archivo,
        file.read(),
        file_options={"content-type": content_type}
    )

    # URL pública directa — sin .url al final
    url = f"{settings.SUPABASE_URL}/storage/v1/object/public/comprobantes/{nombre_archivo}"
    return url


# ✅ Bucket PRIVADO — contratos (solo admin puede generar URL firmada)
def subir_contrato(file):
    extension = file.name.split('.')[-1].lower()
    nombre_archivo = f"contratos/{uuid.uuid4()}.{extension}"
    content_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'

    supabase.storage.from_('contratos-privados').upload(
        nombre_archivo,
        file.read(),
        file_options={"content-type": content_type}
    )

    # Guardamos solo el path, NO url pública
    return nombre_archivo


# ✅ Genera URL firmada temporal (60 min) para ver contrato
def url_firmada_contrato(path, segundos=3600):
    result = supabase.storage.from_('contratos-privados').create_signed_url(
        path, segundos
    )
    return result.get('signedURL') or result.get('signedUrl')

# ✅ Bucket PÚBLICO — facturas del barrio
def subir_factura(file):
    extension = file.name.split('.')[-1].lower()
    nombre_archivo = f"facturas/{uuid.uuid4()}.{extension}"
    content_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'

    supabase.storage.from_('comprobantes').upload(
        nombre_archivo,
        file.read(),
        file_options={"content-type": content_type}
    )

    url = f"{settings.SUPABASE_URL}/storage/v1/object/public/comprobantes/{nombre_archivo}"
    return url

def subir_comprobante_adelanto(file):
    extension = file.name.split('.')[-1].lower()
    nombre_archivo = f"adelantos/{uuid.uuid4()}.{extension}"
    content_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'

    supabase.storage.from_('comprobantes').upload(
        nombre_archivo,
        file.read(),
        file_options={"content-type": content_type}
    )

    return f"{settings.SUPABASE_URL}/storage/v1/object/public/comprobantes/{nombre_archivo}"