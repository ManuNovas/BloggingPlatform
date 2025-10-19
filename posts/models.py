from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    category = models.CharField(max_length=32)
    tags = ArrayField(models.CharField(max_length=32))
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
