"""
ASGI config for maturitni_projekt project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maturitni_projekt.settings.dev')

application = get_asgi_application()

