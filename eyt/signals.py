from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlayerProfile, CoachProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'player':
            PlayerProfile.objects.create(
                user=instance,
                rating=0,  # Default rating value
                specialization='Unknown'  # Default specialization
            )
        elif instance.role == 'coach':
            CoachProfile.objects.create(
                user=instance,
                specialization='General',
                experience_years=0,  # Default experience value
                availability='Unknown'  # Default availability
            )