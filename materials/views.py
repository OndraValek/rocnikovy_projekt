from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Material


class MaterialDetailView(LoginRequiredMixin, DetailView):
    """Detail materiálu."""
    model = Material
    template_name = 'materials/material_detail.html'
    context_object_name = 'material'
    pk_url_kwarg = 'material_id'
    
    def get_queryset(self):
        """Filtruje pouze publikované materiály."""
        return Material.objects.filter(is_published=True)

