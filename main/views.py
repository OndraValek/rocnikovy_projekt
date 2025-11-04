from django.shortcuts import render, get_object_or_404

def home(request):
    """Hlavní stránka s maturitními otázkami"""
    return render(request, 'main/home.html')

def topic_detail(request, topic_id):
    """Detailní stránka tématu"""
    # Prozatím pro téma 1-9: Základy informatiky, Programy a data, Informační systémy, Rastrová grafika, Vektorová grafika, Zpracování textů, Počítačové zpracování zvuku, Digitální video a multimediální prezentace
    if topic_id == 1:
        return render(request, 'main/informatics_detail.html')
    elif topic_id == 2:
        return render(request, 'main/programs_data_detail.html')
    elif topic_id == 3:
        return render(request, 'main/information_systems_detail.html')
    elif topic_id == 4:
        return render(request, 'main/raster_graphics_detail.html')
    elif topic_id == 5:
        return render(request, 'main/vector_graphics_detail.html')
    elif topic_id == 6:
        return render(request, 'main/text_processing_detail.html')
    elif topic_id == 8:
        return render(request, 'main/audio_processing_detail.html')
    elif topic_id == 9:
        return render(request, 'main/video_multimedia_detail.html')
    else:
        # Pro ostatní témata zatím 404
        from django.http import Http404
        raise Http404("Téma neexistuje")

