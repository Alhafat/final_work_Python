from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='recipe_add'),
    path('recipe/edit/<int:recipe_id>/', views.recipe_edit, name='edit_recipe'),  # Исправление здесь
    path('recipe/delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('registration/', views.registration, name='registration'),
    path('accounts/login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_search, name='category_search'),
]
