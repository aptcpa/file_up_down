from django.db import models

# Create your models here.
class Users(models.Model):
	user=models.CharField(max_length=10,unique=True)
	password=models.CharField(max_length=30)