from django.db import models
from django.contrib.auth.models import User

# ==========================
# Filière
# ==========================
class Filiere(models.Model):
    FILIERES = [
        ('APD', 'APD'),
        ('DBE', 'DBE'),
        ('DFE', 'DFE'),
        ('RSIOT', 'RSIOT'),
    ]
    nom = models.CharField(max_length=50, choices=FILIERES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

# ==========================
# Étudiant
# ==========================
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    diplome = models.CharField(max_length=255, null=True, blank=True) 
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default.png')
    bulletin = models.FileField(upload_to='bulletins/', blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def get_cours(self):
        return Cours.objects.filter(filiere=self.filiere)

    def get_exercices(self):
        return Exercice.objects.filter(filiere=self.filiere)

    def get_emplois_du_temps(self):
        return EmploiDuTemps.objects.filter(filiere=self.filiere)

    def get_documents(self):
        return Document.objects.all()

# ==========================
# Responsable
# ==========================
class Responsable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True)
    departement = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

# ==========================
# Documents génériques
# ==========================
class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ==========================
# Cours / Exercice / Emploi du temps / Contenu pédagogique
# ==========================
class Cours(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='cours/')
    responsable = models.ForeignKey('Responsable', on_delete=models.SET_NULL, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.filiere})"

class Exercice(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='exercices/')
    responsable = models.ForeignKey('Responsable', on_delete=models.SET_NULL, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.filiere})"

class EmploiDuTemps(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='emplois/')
    responsable = models.ForeignKey('Responsable', on_delete=models.SET_NULL, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.filiere}"

class ContenuPedagogique(models.Model):
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='contenus/')
    responsable = models.ForeignKey('Responsable', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
