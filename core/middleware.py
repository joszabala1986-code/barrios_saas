class BarrioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Seteamos el default
        request.barrio = None

        # Verificamos de forma segura
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Usamos getattr por si el campo 'barrio' no existe en el objeto user
                request.barrio = getattr(request.user, 'barrio', None)
            except Exception:
                request.barrio = None

        return self.get_response(request)