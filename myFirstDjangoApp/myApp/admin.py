from django.contrib import admin
from .models import (
    Filiere, Etudiant, Responsable, Document, 
    Cours, Exercice, EmploiDuTemps, ContenuPedagogique
)

# -------------------
# Admin Filiere
# -------------------
@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)


# -------------------
# Admin Etudiant
# -------------------
@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'user', 'filiere')
    search_fields = ('firstname', 'lastname', 'user__username')
    list_filter = ('filiere',)


# -------------------
# Admin Responsable
# -------------------
@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('user', 'departement', 'telephone')


# -------------------
# Admin Document
# -------------------
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')


# -------------------
# Admin Cours / Exercice / Emploi / Contenu
# -------------------
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'filiere', 'date_ajout')


@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'filiere', 'date_ajout')


@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('titre', 'filiere', 'date_ajout')


@admin.register(ContenuPedagogique)
class ContenuPedagogiqueAdmin(admin.ModelAdmin):
    list_display = ('titre', 'uploaded_at')
