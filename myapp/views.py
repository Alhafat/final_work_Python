import os
from myapp.models import Recipe, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from myapp.models import Recipe
from myapp.forms import RecipeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os


def home(request):
    recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'home.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


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


@login_required
def edit_recipe(request, recipe_id):
    # Получаем объект рецепта по его идентификатору или возвращаем ошибку 404, если рецепт не найден
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Получаем путь к старому изображению рецепта
    old_image_path = os.path.join(settings.MEDIA_ROOT, str(recipe.image))

    if request.method == 'POST':

        # Создаем форму рецепта на основе полученных данных из POST-запроса
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        # Проверяем, была ли форма заполнена корректно
        if form.is_valid():

            # Сохраняем данные из формы в переменную new_recipe, но пока не сохраняем в базу данных
            new_recipe = form.save(commit=False)

            # Проверяем, было ли передано новое изображение
            if old_image_path in request.FILES:
                # Если изображение было передано в запросе, удаляем старое изображение (если есть)
                if recipe.image:
                    recipe.image.delete()
                    delete_file(old_image_path)

            # Сохранение изменений в рецепте, включая фото
            new_recipe.save()

            # Перенаправляем пользователя на страницу с деталями рецепта
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        # Если метод запроса не POST, создаем пустую форму на основе текущего рецепта
        form = RecipeForm(instance=recipe)

    # Отображаем шаблон страницы редактирования рецепта с заполненной формой
    return render(request, 'edit_recipe.html', {'form': form})


def delete_file(file_path):
    # Определите функцию для удаления файла из файловой системы
    if os.path.exists(file_path):
        os.remove(file_path)


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        # Удаляем фото перед удалением рецепта
        if recipe.image:
            # Получаем путь к файлу изображения
            image_path = os.path.join(settings.MEDIA_ROOT, str(recipe.image))
            recipe.image.delete()  # Удаление только фото, не всего объекта
            # Удаляем файл из файловой системы
            delete_file(image_path)
        recipe.delete()  # Удаление всего рецепта
        return redirect('home')
    return render(request, 'delete_recipe.html', {'recipe': recipe})
