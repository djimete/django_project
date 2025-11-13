from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Responsable

@receiver(post_save, sender=User)
def create_responsable_profile(sender, instance, created, **kwargs):
    if created:
        # Si vous voulez que seuls les utilisateurs du groupe 'Responsable' aient un profil
        if instance.groups.filter(name='Responsable').exists():
            Responsable.objects.create(user=instance)
        # Sinon, retirez le test ci-dessus pour créer un Responsable pour tout utilisateur
