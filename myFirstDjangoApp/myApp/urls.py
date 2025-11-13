from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------
    # Pages publiques
    # ----------------------------
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ----------------------------
    # Pages générales
    # ----------------------------
    path('', views.home, name='home'),

    # ----------------------------
    # Espace étudiant
    # ----------------------------
    path('espace_etudiant/', views.espace_etudiant, name='espace_etudiant'),

    # ----------------------------
    # Administration - Filières
    # ----------------------------
    path('administration/liste_filieres/', views.liste_filieres, name='liste_filieres'),
    path('administration/ajouter_filiere/', views.ajouter_filiere, name='ajouter_filiere'),

    # ----------------------------
    # Administration - Étudiants
    # ----------------------------
    path('administration/ajouter_etudiant/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('administration/etudiants_par_filiere/<int:filiere_id>/', views.etudiants_par_filiere, name='etudiants_par_filiere'),
    path('administration/details/<int:id>/', views.details, name='details'),
    path('administration/supprimer_etudiant/<int:etudiant_id>/', views.supprimer_etudiant, name='supprimer_etudiant'),

    # ----------------------------
    # Espace Responsable / Formations
    # ----------------------------
    path('formations/espace_responsable/', views.espace_responsable, name='espace_responsable'),
    path('formations/ajouter_cours/', views.ajouter_cours, name='ajouter_cours'),
    path('formations/ajouter_exercice/', views.ajouter_exercice, name='ajouter_exercice'),
    path('formations/ajouter_emploi_du_temps/', views.ajouter_emploi_du_temps, name='ajouter_emploi_du_temps'),
    path('formations/upload_contenu_pedagogique/', views.upload_contenu_pedagogique, name='upload_contenu_pedagogique'),

    # ----------------------------
    # Page de succès (optionnelle)
    # ----------------------------
    path('success/', views.success_page, name='success_page'),
]
