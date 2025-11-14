from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from .models import Etudiant, Filiere, Cours, Exercice, EmploiDuTemps, ContenuPedagogique
from .forms import (
    CreateUserForm, EtudiantForm, UpdateEtudiantForm,
    FiliereForm, CoursForm, ExerciceForm,
    EmploiDuTempsForm, ContenuPedagogiqueForm
)
from .decorators import unauthenticated_user, allowed_users

# =========================
# Pages publiques
# =========================
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        etudiant_form = EtudiantForm(request.POST, request.FILES)

        if user_form.is_valid() and etudiant_form.is_valid():
            user = user_form.save()
            group, _ = Group.objects.get_or_create(name='etudiant')
            user.groups.add(group)

            etudiant = etudiant_form.save(commit=False)
            etudiant.user = user
            etudiant.save()

            messages.success(request, "Compte créé avec succès ! Veuillez vous connecter.")
            return redirect('login')
    else:
        user_form = CreateUserForm()
        etudiant_form = EtudiantForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'etudiant_form': etudiant_form
    })


# ---------------------------
# Inscription Admin
# ---------------------------
@unauthenticated_user
def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Vérifier si le username existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect('register_admin')

        # Vérifier si l'email existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('register_admin')

        # Créer l'utilisateur admin
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Ajouter l'utilisateur dans le groupe admin_filiere
        group, _ = Group.objects.get_or_create(name='admin_filiere')
        user.groups.add(group)

        messages.success(request, "Compte administrateur créé avec succès.")
        return redirect('login')

    return render(request, 'register_admin.html')


# =========================
# Connexion
# =========================
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)

            # Redirection selon le groupe
            if user.groups.filter(name='admin_filiere').exists():
                return redirect("espace_admin")
            elif user.groups.filter(name='responsable').exists():
                return redirect("espace_responsable")
            elif user.groups.filter(name='etudiant').exists():
                return redirect("espace_etudiant")
            else:
                return redirect("home")

        messages.error(request, "Identifiants incorrects.")

    return render(request, "login.html")


# =========================
# Déconnexion
# =========================
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")


# =========================
# Pages générales
# =========================
@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def espace_etudiant(request):
    etudiant = get_object_or_404(Etudiant, user=request.user)
    return render(request, 'espace_etudiant.html', {'etudiant': etudiant})


# =========================
# Espace Admin
# =========================
@login_required
@allowed_users(['admin_filiere'])
def espace_admin(request):
    return render(request, 'admin/espace_admin.html')


# =========================
# Gestion Filières
# =========================
@login_required
@allowed_users(['admin_filiere'])
def liste_filieres(request):
    filieres = Filiere.objects.all()
    return render(request, 'admin/liste_filieres.html', {'filieres': filieres})


@login_required
@allowed_users(['admin_filiere'])
def ajouter_filiere(request):
    form = FiliereForm()
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Filière ajoutée avec succès.")
            return redirect('liste_filieres')
    return render(request, 'admin/ajouter_filiere.html', {'form': form})


# =========================
# Gestion Étudiants
# =========================
@login_required
@allowed_users(['admin_filiere'])
def ajouter_etudiant(request):
    form = EtudiantForm()
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if form.is_valid():
            user = User.objects.create_user(username=username, password=password)
            group, _ = Group.objects.get_or_create(name='etudiant')
            user.groups.add(group)

            etudiant = form.save(commit=False)
            etudiant.user = user
            etudiant.save()
            messages.success(request, f"Étudiant {etudiant.firstname} ajouté avec succès.")
            return redirect('liste_filieres')
    return render(request, 'admin/ajouter_etudiant.html', {'form': form})


@login_required
@allowed_users(['admin_filiere'])
def liste_etudiants_par_filiere(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    etudiants = Etudiant.objects.filter(filiere=filiere)
    return render(request, 'admin/liste_etudiants.html', {'filieres': filiere, 'etudiants': etudiants})


@login_required
@allowed_users(['admin_filiere'])
def details_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    form = UpdateEtudiantForm(instance=etudiant)
    if request.method == 'POST':
        form = UpdateEtudiantForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "Étudiant mis à jour avec succès.")
            return redirect('details_etudiant', etudiant_id=etudiant.id)
    return render(request, 'admin/details_etudiant.html', {'form': form, 'etudiant': etudiant})


@login_required
@allowed_users(['admin_filiere'])
def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    filiere_id = etudiant.filiere.id if etudiant.filiere else None
    etudiant.delete()
    messages.success(request, f"Étudiant {etudiant.firstname} supprimé.")
    if filiere_id:
        return redirect('liste_etudiants_par_filiere', filiere_id=filiere_id)
    return redirect('liste_filieres')


# =========================
# Responsable / Formations
# =========================
@login_required
@allowed_users(['responsable', 'admin_filiere'])
def espace_responsable(request):
    return render(request, 'formations/espace_responsable.html')


@login_required
@allowed_users(['responsable', 'admin_filiere'])
def ajouter_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST, request.FILES)
        if form.is_valid():
            cours = form.save(commit=False)
            cours.responsable = request.user.responsable
            cours.save()
            messages.success(request, "Cours ajouté avec succès.")
            return redirect('espace_responsable')
    else:
        form = CoursForm()
    return render(request, 'formations/ajouter_cours.html', {'form': form})


@login_required
@allowed_users(['responsable', 'admin_filiere'])
def ajouter_exercice(request):
    if request.method == 'POST':
        form = ExerciceForm(request.POST, request.FILES)
        if form.is_valid():
            exercice = form.save(commit=False)
            exercice.responsable = request.user.responsable
            exercice.save()
            messages.success(request, "Exercice ajouté avec succès.")
            return redirect('espace_responsable')
    else:
        form = ExerciceForm()
    return render(request, 'formations/ajouter_exercice.html', {'form': form})


@login_required
@allowed_users(['responsable', 'admin_filiere'])
def ajouter_emploi_du_temps(request):
    if request.method == 'POST':
        form = EmploiDuTempsForm(request.POST, request.FILES)
        if form.is_valid():
            emploi = form.save(commit=False)
            emploi.responsable = request.user.responsable
            emploi.save()
            messages.success(request, "Emploi du temps ajouté avec succès.")
            return redirect('espace_responsable')
    else:
        form = EmploiDuTempsForm()
    return render(request, 'formations/ajouter_emploi_du_temps.html', {'form': form})


@login_required
@allowed_users(['responsable', 'admin_filiere'])
def upload_contenu_pedagogique(request):
    if request.method == 'POST':
        form = ContenuPedagogiqueForm(request.POST, request.FILES)
        if form.is_valid():
            contenu = form.save(commit=False)
            contenu.responsable = request.user.responsable
            contenu.save()
            messages.success(request, "Contenu pédagogique uploadé avec succès.")
            return redirect('espace_responsable')
    else:
        form = ContenuPedagogiqueForm()

    contenus = ContenuPedagogique.objects.all()
    return render(request, "formations/upload_contenu_pedagogique.html", {'form': form, 'contenus': contenus})


@login_required
def success_page(request):
    return render(request, 'success.html')
