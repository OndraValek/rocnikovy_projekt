from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.static import static

from subjects.urls import api_urlpatterns

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('accounts/', include('allauth.urls')),
    # API endpointy pro dynamické načítání úloh (před subjects, aby se neshodovaly)
    path('api/', include(api_urlpatterns)),
    # Materials, quizzes a forum musí být před subjects, aby se jejich URL patterns neshodovaly
    path('', include('materials.urls')),
    path('', include('quizzes.urls')),
    path('', include('forum.urls')),
    path('', include('subjects.urls')),
    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

