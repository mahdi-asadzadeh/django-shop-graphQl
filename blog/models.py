import os

from django.db import models
from django.contrib.auth import get_user_model
from django.http import response
from django.utils.html import format_html
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.conf import settings

from taggit.managers import TaggableManager



User = get_user_model()


def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_gallery_image_path(instance, filename):
	name, ext = get_filename_ext(filename)
	try:
		latest_id = Article.objects.latest('pk').id
	except Article.DoesNotExist:
		latest_id = 0
	latest_id +=1
	final_name = f"{instance.slug}-{latest_id}{ext}"
	return f"articles/images/{final_name}"


class Article(models.Model):
	CHOICES_STATUS = (
		('p', 'publish'),
		('d', 'draft'),
	)
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True, max_length=200)
	image = models.ImageField(upload_to=upload_gallery_image_path, null=True, blank=True)
	body = models.TextField()
	iframe = models.TextField(null=True, blank=True)
	create = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	status = models.CharField(choices=CHOICES_STATUS, max_length=1)

	numbers_rating = models.FloatField(default=0)
	scope_avrage = models.FloatField(default=0)

	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

	tags = TaggableManager()

	def image_tag(self):
		return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.image.url))

	image_tag.short_description = 'image'

	def __str__(self):
		return f'{self.name} - {self.slug}'
	
	@property
	def get_tags(self):
		return self.tags.all()
	
	@property
	def visit(self):
		settings.REDIS.hsetnx('article_visit', self.id, 0)
		return settings.REDIS.hget('article_visit', self.id)

	class Meta:
		ordering = ['-create']
		

def save_article(sender, **kwargs):
	cache.clear()

post_save.connect(save_article, sender=Article)


def delete_article(sender, **kwargs):
	cache.clear()

post_delete.connect(delete_article, sender=Article)
