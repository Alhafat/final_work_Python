from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    steps = models.TextField()  # Добавлено поле steps
    preparation_time = models.CharField(max_length=20)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Удаляем изображение перед удалением объекта
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f' self: {self.name}'


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'recipe: {self.recipe}, category: {self.category}'
