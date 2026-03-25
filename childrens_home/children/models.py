from django.db import models
from django.contrib.auth.models import User

class Child(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    story = models.TextField()
    photo = models.ImageField(upload_to='children/')
    is_sponsored = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Sponsor(models.Model):   # 👈 NOW OUTSIDE
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} sponsoring {self.child}"