from django.http import HttpResponse
from django.shortcuts import redirect

# -----------------------------
# Vérifie si l'utilisateur n'est pas connecté
# -----------------------------
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # redirection si déjà connecté
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# -----------------------------
# Vérifie le groupe d'un utilisateur
# -----------------------------
def allowed_users(allowed_users=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = request.user.groups.all()
            if groups.exists():
                group = groups[0].name
            else:
                group = None  # Aucun groupe attribué

            if group in allowed_users:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Vous n'êtes pas autorisés à voir cette page")
        return wrapper_func
    return decorator


# -----------------------------
# Accès uniquement pour les étudiants
# -----------------------------
def students_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = request.user.groups.all()
        if groups.exists():
            group = groups[0].name
        else:
            group = None

        if group == 'etudiant':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')  # redirection si ce n'est pas un étudiant
    return wrapper_func


# -----------------------------
# Accès uniquement pour l'admin
# -----------------------------
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        groups = request.user.groups.all()
        if groups.exists():
            group = groups[0].name
        else:
            group = None

        if group == 'admin_filiere':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Vous n'êtes pas autorisés à voir cette page")
    return wrapper_func
