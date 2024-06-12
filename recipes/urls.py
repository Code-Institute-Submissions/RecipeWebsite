from django.urls import path
from .views import AddRecipe, Recipes

urlpatterns = [
    path("add/", AddRecipe.as_view(), name="add_recipe"),
    path("", Recipes.as_view(), name="recipes"),
]