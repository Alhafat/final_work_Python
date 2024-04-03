from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Recipe)
admin.site.register(models.Category)
admin.site.register(models.RecipeCategory)