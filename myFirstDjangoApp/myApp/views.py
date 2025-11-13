from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.conf import settings
import os

from .models import Etudiant, Filiere, ContenuPedagogique  # ajoute d'autres modèles si nécessaire
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


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)

            if user.groups.filter(name='responsable').exists():
                return redirect('espace_responsable')
            elif user.groups.filter(name='etudiant').exists():
                return redirect('espace_etudiant')
            elif user.is_superuser:
                return redirect('admin:index')
            else:
                return redirect('home')

        messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')

    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


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
# Administration
# =========================
@login_required
@allowed_users(allowed_users=['admin'])
def liste_filieres(request):
    filieres = Filiere.objects.all()
    return render(request, 'administration/liste_filieres.html', {'filieres': filieres})


@login_required
@allowed_users(allowed_users=['admin'])
def ajouter_filiere(request):
    form = FiliereForm()
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Filière ajoutée avec succès.")
            return redirect('liste_filieres')
    return render(request, 'administration/ajouter_filiere.html', {'form': form})


@login_required
@allowed_users(allowed_users=['admin'])
def ajouter_etudiant(request):
    form = EtudiantForm()
    filieres = Filiere.objects.all()
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            new_etudiant = form.save(commit=False)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.create_user(username=username, password=password)
            group = Group.objects.get(name='etudiant')
            user.groups.add(group)
            new_etudiant.user = user
            new_etudiant.save()
            messages.success(request, f"L'étudiant {new_etudiant.firstname} {new_etudiant.lastname} a été ajouté.")
            return redirect('liste_filieres')
    return render(request, 'administration/ajouter_etudiant.html', {'form': form, 'filieres': filieres})


@login_required
@allowed_users(allowed_users=['admin'])
def etudiants_par_filiere(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    etudiants = Etudiant.objects.filter(filiere=filiere)
    return render(request, 'administration/etudiants_par_filiere.html', {'filiere': filiere, 'etudiants': etudiants})


@login_required
@allowed_users(allowed_users=['admin'])
def details(request, id):
    etudiant = get_object_or_404(Etudiant, id=id)
    form = UpdateEtudiantForm(instance=etudiant)
    if request.method == 'POST':
        form = UpdateEtudiantForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "Informations de l'étudiant mises à jour avec succès.")
            return redirect('details', id=etudiant.id)
    return render(request, 'administration/details.html', {'formulaire': form, 'etudiant': etudiant})


@login_required
@allowed_users(allowed_users=['admin'])
def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    filiere_id = etudiant.filiere.id if etudiant.filiere else None
    etudiant.delete()
    messages.success(request, f"L'étudiant {etudiant.firstname} {etudiant.lastname} a été supprimé.")
    if filiere_id:
        return redirect('etudiants_par_filiere', filiere_id=filiere_id)
    return redirect('liste_filieres')


# =========================
# Responsable / Formations
# =========================
@login_required
@allowed_users(allowed_users=['responsable', 'admin'])
def espace_responsable(request):
    return render(request, 'formations/espace_responsable.html')


@login_required
@allowed_users(allowed_users=['responsable', 'admin'])
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
@allowed_users(allowed_users=['responsable', 'admin'])
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
@allowed_users(allowed_users=['responsable', 'admin'])
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
@allowed_users(allowed_users=['responsable', 'admin'])
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
