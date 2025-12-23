#!/usr/bin/env python
"""
Skript pro kontrolu OAuth callback URLs
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maturitni_projekt.settings.dev')
django.setup()

from django.contrib.sites.models import Site
from django.urls import reverse
from django.test import RequestFactory

site = Site.objects.get(pk=1)
print("=" * 70)
print("OAUTH CALLBACK URLS - KONTROLA")
print("=" * 70)
print(f"\nSite domain: {site.domain}")
print(f"Site name: {site.name}\n")

rf = RequestFactory()
request = rf.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'
request.META['SERVER_NAME'] = 'localhost'
request.META['SERVER_PORT'] = '8000'

providers = ['github', 'google', 'microsoft']

print("Tyto URL musí být nastavené v OAuth aplikacích:\n")
for provider in providers:
    try:
        callback_path = f'/accounts/{provider}/login/callback/'
        full_url = f'http://localhost:8000{callback_path}'
        print(f"✅ {provider.upper()}:")
        print(f"   {full_url}\n")
    except Exception as e:
        print(f"❌ {provider.upper()}: Chyba - {e}\n")

print("=" * 70)
print("INSTRUKCE:")
print("=" * 70)
print("\n1. GitHub: https://github.com/settings/developers")
print("   → Klikněte na vaši OAuth aplikaci")
print("   → V poli 'Authorization callback URL' zadejte:")
print("   → http://localhost:8000/accounts/github/login/callback/")
print("\n2. Google: https://console.cloud.google.com/apis/credentials")
print("   → Klikněte na vaši OAuth 2.0 Client ID")
print("   → V sekci 'Authorized redirect URIs' přidejte:")
print("   → http://localhost:8000/accounts/google/login/callback/")
print("\n3. Microsoft: https://portal.azure.com/")
print("   → Najděte vaši App Registration")
print("   → V sekci 'Redirect URIs' přidejte:")
print("   → http://localhost:8000/accounts/microsoft/login/callback/")
print("\n" + "=" * 70)

