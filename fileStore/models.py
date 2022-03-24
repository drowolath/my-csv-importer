from django.db import models

class File(models.Model):
    path = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    complete = models.BooleanField(default=False)
