from django.db import models

# Create your models here.
from django.db import models

#管理员
class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name