import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myFirstDjangoApp.settings')
django.setup()

from django.contrib.auth.models import User
from myApp.models import Responsable

user = User.objects.get(username='responsable')
responsable, created = Responsable.objects.get_or_create(user=user)

if created:
    print("Responsable créé :", responsable)
else:
    print("Responsable existant :", responsable)
