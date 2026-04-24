from django.db import models

class TestImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cloud_test/")