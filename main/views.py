from django.shortcuts import render

def home(request):
    """Hlavní stránka s maturitními otázkami"""
    return render(request, 'main/home.html')
