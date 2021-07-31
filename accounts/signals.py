from django.db.models.signals import post_save
from .models import Profile, User

def save_profile(sender, **kwargs):
	if kwargs['created']:
		Profile.objects.create(user=kwargs['instance'])
		
post_save.connect(save_profile, sender=User)