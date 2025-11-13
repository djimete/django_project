from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_users=[]):  # FOR ADMIN PAGE
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = request.user.groups.all()
            if groups.exists():
                group = groups[0].name
            else:
                group = None  # ou un groupe par défaut

            if group in allowed_users:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Vous n\'êtes pas autorisés à voir cette page')
        return wrapper_func
    return decorator


def students_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = request.user.groups.all()
        if groups.exists():
            group = groups[0].name
        else:
            group = None  # ou un groupe par défaut

        if group == 'etudiant':
            return redirect('main')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func
