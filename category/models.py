from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.db import models


class Category(models.Model):
    parent = models.ForeignKey("self" , null=True , blank=True , on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name

def save_category(sender, **kwargs):
	cache.clear()

post_save.connect(save_category, sender=Category)


def delete_category(sender, **kwargs):
	cache.clear()

post_delete.connect(delete_category, sender=Category)
