from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Etudiant, Filiere, Cours, Exercice, EmploiDuTemps, ContenuPedagogique

# ===========================
# Formulaire d'inscription utilisateur + étudiant
# ===========================
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=255, required=True)
    lastname = forms.CharField(max_length=255, required=True)
    telephone = forms.CharField(max_length=20, required=True)
    date_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'firstname', 'lastname', 'telephone', 'date_naissance', 'profile_picture'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

# ===========================
# Formulaire pour créer un étudiant (admin)
# ===========================
class EtudiantForm(ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'firstname', 'lastname', 'telephone',
            'date_naissance', 'filiere', 'profile_picture',
            'bulletin', 'diplome'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

# ===========================
# Formulaire pour mettre à jour un étudiant (admin)
# ===========================
class UpdateEtudiantForm(ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'firstname', 'lastname', 'telephone',
            'date_naissance', 'filiere', 'profile_picture',
            'bulletin', 'diplome'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

# ===========================
# Formulaires Responsable / Formations
# ===========================
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['titre', 'filiere', 'fichier']

class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['titre', 'filiere', 'fichier']

class EmploiDuTempsForm(forms.ModelForm):
    class Meta:
        model = EmploiDuTemps
        fields = ['titre', 'filiere', 'fichier']

class ContenuPedagogiqueForm(forms.ModelForm):
    class Meta:
        model = ContenuPedagogique
        fields = ['titre', 'fichier']

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['nom', 'description']