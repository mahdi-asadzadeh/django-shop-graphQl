from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, GalleryProduct

@receiver([post_save, post_delete], sender=Product)
@receiver([post_save, post_delete], sender=GalleryProduct)
def cache_update(sender, **kwargs):
	cache.delete('products')