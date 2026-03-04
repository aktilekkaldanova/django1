from django.db import models
from django.contrib.auth.models import User

class Arcticles(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User)
