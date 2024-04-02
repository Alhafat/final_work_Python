from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    steps = models.TextField()
    preparation_time = models.CharField(max_length=20)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True, verbose_name='Image')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Recipe: {self.recipe.title}, Category: {self.category.name}'
