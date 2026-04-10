from django.shortcuts import redirect

def admin_barrio_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        # ✅ Permitir admin Y superadmin
        if request.user.rol not in ['admin', 'superadmin']:
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return wrapper