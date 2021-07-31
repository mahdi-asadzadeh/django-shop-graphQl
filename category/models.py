from django.db import models


class Category(models.Model):
    parent = models.ForeignKey("self" , null=True , blank=True , on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name