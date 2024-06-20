from django.views.generic import ListView
from recipes.models import Recipe

class index(ListView):
    template_name = 'home/base.html'
    model = Recipe
    context_object_name = 'recipes'

    def get_queryset(self):
        return self.model.objects.all()[:3]