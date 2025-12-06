from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.conf import settings
from django.urls import reverse
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
    
    def get_context_data(self, **kwargs):
        """Přidá informace pro h5p-standalone."""
        context = super().get_context_data(**kwargs)
        material = self.object
        
        # Přidat informace pro h5p-standalone
        if material.h5p_path:
            # Cesta k H5P adresáři (H5P Standalone Player si přidá h5p.json sám)
            context['h5p_json_path'] = f"{settings.MEDIA_URL}{material.h5p_path}"
            # Content ID pro API endpointy (použijeme material ID)
            context['h5p_content_id'] = f"material-{material.id}"
            # API endpointy
            context['h5p_user_data_url'] = reverse('quizzes:h5p_user_data', kwargs={'content_id': f"material-{material.id}"})
            context['h5p_xapi_url'] = reverse('quizzes:h5p_xapi')
            # Cesty k h5p-standalone souborům
            context['h5p_player_js'] = '/static/h5p-player/main.bundle.js'
            context['h5p_frame_js'] = '/static/h5p-player/frame.bundle.js'
            context['h5p_frame_css'] = '/static/h5p-player/h5p.css'
        
        return context

