from django.urls import path
from . import views

urlpatterns = [
    # Pages publiques
    path('register/', views.register, name='register'),
    path('register_admin/', views.register_admin, name='register_admin'),
    path('login/', views.loginPage, name='login'),  # correspond à loginPage dans views.py
    path('logout/', views.logout_view, name='logout'),

    # Pages générales
    path('', views.home, name='home'),

    # Espace étudiant
    path('espace_etudiant/', views.espace_etudiant, name='espace_etudiant'),

    # Espace Admin
    path('espace_admin/', views.espace_admin, name='espace_admin'),

    # Gestion Filières
    path('liste_filieres/', views.liste_filieres, name='liste_filieres'),
    path('ajouter_filiere/', views.ajouter_filiere, name='ajouter_filiere'),

    # Gestion Étudiants
    path('ajouter_etudiant/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('liste_etudiants/<int:filiere_id>/', views.liste_etudiants_par_filiere, name='liste_etudiants_par_filiere'),
    path('details_etudiant/<int:etudiant_id>/', views.details_etudiant, name='details_etudiant'),
    path('supprimer_etudiant/<int:etudiant_id>/', views.supprimer_etudiant, name='supprimer_etudiant'),

    # Espace Responsable / Formations
    path('espace_responsable/', views.espace_responsable, name='espace_responsable'),
    path('ajouter_cours/', views.ajouter_cours, name='ajouter_cours'),
    path('ajouter_exercice/', views.ajouter_exercice, name='ajouter_exercice'),
    path('ajouter_emploi_du_temps/', views.ajouter_emploi_du_temps, name='ajouter_emploi_du_temps'),
    path('upload_contenu_pedagogique/', views.upload_contenu_pedagogique, name='upload_contenu_pedagogique'),

    # Page succès
    path('success/', views.success_page, name='success'),
]
