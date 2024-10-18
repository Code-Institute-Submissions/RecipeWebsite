from django.views.generic import (
    CreateView, ListView, DetailView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin
)

from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages

from .models import Recipe
from .forms import RecipeForm


class Recipes(ListView):
    """View all recipes"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query) |
                Q(cuisine_types__icontains=query)
            )
        else:
            recipes = self.model.objects.all()
        return recipes


class RecipeDetail(DetailView):
    """View a single recipe"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"


class AddRecipe(LoginRequiredMixin, CreateView):
    """Add recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request,
                         'The recipe has been added to the website.')
        return super(AddRecipe, self).form_valid(form)


class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a recipe"""
    template_name = 'recipes/edit_recipe.html'
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'

    def test_func(self):
        """Check if the current user is the creator of the recipe"""
        recipe = self.get_object()
        return self.request.user == recipe.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'The recipe has been edited.')
        return super(EditRecipe, self).form_valid(form)

    def handle_no_permission(self):
        """Redirect to home page if user is not authorized"""
        return redirect('index')


class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a recipe"""
    model = Recipe
    success_url = '/recipes/'

    def test_func(self):
        return self.request.user == self.get_object().user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         'The recipe has been deleted from the website.')
        return response
