from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.documents.models import Document
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class MaterialType(models.TextChoices):
    PDF = 'pdf', _('PDF dokument')
    VIDEO = 'video', _('Video')
    LINK = 'link', _('Odkaz')
    H5P = 'h5p', _('H5P interaktivní obsah')
    TEXT = 'text', _('Textový materiál')
    IMAGE = 'image', _('Obrázek')


class Material(ClusterableModel):
    """Výukový materiál připojený k okruhu."""
    topic = models.ForeignKey(
        'subjects.Topic',
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name=_('Okruh')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Název materiálu')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Popis')
    )
    material_type = models.CharField(
        max_length=20,
        choices=MaterialType.choices,
        verbose_name=_('Typ materiálu')
    )
    
    # Pro PDF dokumenty
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materials',
        verbose_name=_('Dokument')
    )
    
    # Pro obrázky
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materials',
        verbose_name=_('Obrázek')
    )
    
    # Pro odkazy a H5P
    external_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Externí URL'),
        help_text=_('URL pro video, odkaz nebo H5P obsah')
    )
    
    # Pro H5P embed kód
    h5p_embed_code = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('H5P embed kód'),
        help_text=_('Vložte iframe kód pro H5P obsah')
    )
    
    # Pro textové materiály
    content = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Textový obsah')
    )
    
    # Metadata
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_materials',
        verbose_name=_('Autor')
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Pořadí')
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Publikováno')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Materiál')
        verbose_name_plural = _('Materiály')
        ordering = ['topic', 'order', 'title']
    
    def __str__(self):
        return f"{self.topic.name} - {self.title}"
    
    def get_url(self):
        """Vrátí URL materiálu podle typu."""
        if self.material_type == MaterialType.PDF and self.document:
            return self.document.url
        elif self.material_type == MaterialType.LINK and self.external_url:
            return self.external_url
        elif self.material_type == MaterialType.VIDEO and self.external_url:
            return self.external_url
        elif self.material_type == MaterialType.H5P and self.h5p_embed_code:
            return None  # H5P se zobrazuje přes embed
        return None

