from .models import Barrio

class BarrioMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.barrio = None

        if request.user.is_authenticated:
            request.barrio = request.user.barrio

        response = self.get_response(request)

        return response