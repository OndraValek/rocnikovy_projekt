from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Material


@login_required
def material_detail(request, material_id):
    """Detail materiálu."""
    material = get_object_or_404(Material, id=material_id, is_published=True)
    context = {
        'material': material,
    }
    return render(request, 'materials/material_detail.html', context)

