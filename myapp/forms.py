from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'preparation_time',
                  'image']  # добавлено поле 'image' для загрузки изображения
