from django.db import models
from cloudinary.models import CloudinaryField

class TestImage(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image')