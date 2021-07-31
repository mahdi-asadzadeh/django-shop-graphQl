from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Article

@receiver([post_save, post_delete], sender=Article)
def cache_update(sender, **kwargs):
	cache.delete('articles')