from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class Subject(ClusterableModel):
    """Maturitní předmět."""
    name = models.CharField(
        max_length=200,
        verbose_name=_('Název předmětu'),
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_('URL slug')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Popis')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Předmět')
        verbose_name_plural = _('Předměty')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Topic(ClusterableModel):
    """Maturitní okruh v rámci předmětu."""
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name=_('Předmět')
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_('Název okruhu')
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('URL slug')
    )
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_('Popis okruhu'),
        features=['bold', 'italic', 'link', 'ol', 'ul']
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Pořadí'),
        help_text=_('Pořadí zobrazení okruhu')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Okruh')
        verbose_name_plural = _('Okruhy')
        ordering = ['order', 'name']
        unique_together = [['subject', 'slug']]
    
    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class SubjectPage(Page):
    """Wagtail stránka pro předmět."""
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_('Popis předmětu'),
        features=['bold', 'italic', 'link', 'ol', 'ul']
    )
    subject = models.OneToOneField(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='page',
        verbose_name=_('Předmět')
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('subject'),
    ]
    
    subpage_types = ['subjects.TopicPage']
    
    class Meta:
        verbose_name = _('Stránka předmětu')
        verbose_name_plural = _('Stránky předmětů')


class TopicPage(Page):
    """Wagtail stránka pro okruh s materiály, testy a fórem."""
    
    # StreamField pro flexibilní obsah
    content = StreamField([
        ('paragraph', blocks.RichTextBlock(
            label=_('Odstavec'),
            features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3']
        )),
        ('h5p_content', blocks.RawHTMLBlock(
            label=_('H5P obsah'),
            help_text=_('Vložte iframe kód pro H5P obsah')
        )),
        ('image', ImageChooserBlock(label=_('Obrázek'))),
        ('document', DocumentChooserBlock(label=_('Dokument'))),
        ('video', blocks.URLBlock(
            label=_('Video URL'),
            help_text=_('URL videa (YouTube, Vimeo, atd.)')
        )),
    ], blank=True, use_json_field=True, verbose_name=_('Obsah'))
    
    topic = models.OneToOneField(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='page',
        verbose_name=_('Okruh')
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('topic'),
        FieldPanel('content'),
    ]
    
    parent_page_types = ['subjects.SubjectPage']
    subpage_types = []
    
    class Meta:
        verbose_name = _('Stránka okruhu')
        verbose_name_plural = _('Stránky okruhů')

