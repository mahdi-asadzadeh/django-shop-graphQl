from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models


User = get_user_model()


class CommentManager(models.Manager):
    def filter_by_instance(self , instance):
        comment_for_model = ContentType.objects.get_for_model(instance)
        object_id = instance.id
        qs = self.filter(content_type=comment_for_model , object_id=object_id , parent=None)
        return qs 


class Comment(models.Model):
    RATE_CHOICES = (
        ('5', 'excellent'),
        ('4', 'very good'),
        ('3', 'good'),
        ('2', 'bad'),
        ('1', 'very bad')
    )
    parent = models.ForeignKey("self" , null=True , blank=True , on_delete=models.CASCADE, related_name='children')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE , related_name="post", null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')    

    rate = models.CharField(choices=RATE_CHOICES, max_length=1)
    body = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()


def save_comment(sender, **kwargs):
	cache.clear()

post_save.connect(save_comment, sender=Comment)


def delete_comment(sender, **kwargs):
	cache.clear()

post_delete.connect(delete_comment, sender=Comment)
