from django.http import HttpResponseForbidden
from myapp.models import Recipe, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from myapp.models import Recipe
from myapp.forms import RecipeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def home(request):
    recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'home.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def my_view(request):
    # Some logic
    messages.success(request, 'Рецепт успешно изменен.')
    return redirect('home')


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            return redirect('home')
    else:
        form = RecipeForm()

    return render(request, 'recipe_form.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if not can_edit_recipe(request, recipe_id):
        return HttpResponseForbidden("You are not allowed to edit this recipe.")
    # if request.user != recipe.author:
    #     messages.error(request, 'Вы не имеете права на редактирование этого рецепта.')
    #     return redirect('recipe_detail', recipe_id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рецепт успешно отредактирован.')
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'edit_recipe.html', {'form': form})


def search(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'recipes': recipes})


def category_search(request, category_id):
    category = Category.objects.get(pk=category_id)
    recipes = category.recipe_set.all()
    return render(request, 'category_search_results.html', {'recipes': recipes, 'category': category})


def registration(request):
    # логика регистрации пользователя
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Дополнительные действия после успешной регистрации, например, перенаправление на страницу входа
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully!')
                return redirect('home')  # Перенаправляем пользователя на главную страницу
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    django_logout(request)
    # Дополнительные действия после выхода пользователя, например, перенаправление на главную страницу
    return redirect('home')


class EditRecipeView(PermissionRequiredMixin, UpdateView):
    model = Recipe
    template_name = 'edit_recipe.html'
    form_class = RecipeForm
    success_url = '/'

    # Установите необходимые права доступа для этого представления
    permission_required = 'myapp.change_recipe'  # Изменение рецепта

    def has_permission(self):
        # Проверьте, является ли текущий пользователь автором рецепта
        recipe = self.get_object()
        return self.request.user == recipe.author


class DeleteRecipeView(PermissionRequiredMixin, DeleteView):
    model = Recipe
    success_url = '/'
    template_name = 'delete_recipe.html'

    # Установите необходимые права доступа для этого представления
    permission_required = 'myapp.delete_recipe'  # Удаление рецепта

    def has_permission(self):
        # Проверьте, является ли текущий пользователь автором рецепта
        recipe = self.get_object()
        return self.request.user == recipe.author


def delete_file(file_path):
    # Определите функцию для удаления файла из файловой системы
    if os.path.exists(file_path):
        os.remove(file_path)


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if not can_delete_recipe(request, recipe_id):
        return HttpResponseForbidden("You are not allowed to delete this recipe.")
    # if request.user != recipe.author:
    #     messages.error(request, 'Вы не имеете права на удаление этого рецепта.')
    #     return redirect('recipe_detail', recipe_id=recipe_id)

    if request.method == 'POST':
        if recipe.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(recipe.image))
            recipe.image.delete()
            delete_file(image_path)
        recipe.delete()
        messages.success(request, 'Рецепт успешно удален.')
        return redirect('home')
    return render(request, 'delete_recipe.html', {'recipe': recipe})


@user_passes_test(lambda u: u.is_authenticated)
def can_edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return request.user == recipe.author


@user_passes_test(lambda u: u.is_authenticated)
def can_delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return request.user == recipe.author
