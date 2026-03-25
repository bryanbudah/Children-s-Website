from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Child, Sponsor

admin.site.register(Child)
admin.site.register(Sponsor)