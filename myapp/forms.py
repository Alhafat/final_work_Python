from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'preparation_time', 'image']
