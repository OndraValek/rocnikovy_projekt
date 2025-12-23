from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
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
    classes = models.ManyToManyField(
        'accounts.StudentClass',
        related_name='subjects',
        blank=True,
        verbose_name=_('Třídy'),
        help_text=_('Třídy, které mají přístup k tomuto předmětu')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Předmět')
        verbose_name_plural = _('Předměty')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_classes_display(self):
        """Zobrazit třídy přiřazené k předmětu."""
        classes = self.classes.all()
        if classes.exists():
            return ', '.join([str(c) for c in classes])
        return '-'
    get_classes_display.short_description = 'Třídy'


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


class Feedback(models.Model):
    """Připomínky/zpětná vazba na předměty a okruhy."""
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('subject', 'topic')},
        verbose_name=_('Typ obsahu')
    )
    object_id = models.PositiveIntegerField(verbose_name=_('ID objektu'))
    content_object = GenericForeignKey('content_type', 'object_id')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name=_('Autor')
    )
    text = models.TextField(
        verbose_name=_('Text připomínky'),
        help_text=_('Napište svou připomínku nebo zpětnou vazbu')
    )
    is_edited = models.BooleanField(
        default=False,
        verbose_name=_('Upraveno')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Vytvořeno'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Aktualizováno'))
    
    class Meta:
        verbose_name = _('Připomínka')
        verbose_name_plural = _('Připomínky')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        content_name = str(self.content_object) if self.content_object else f"{self.content_type} #{self.object_id}"
        author_name = self.author.get_full_name() or self.author.email
        return f"Připomínka od {author_name} na {content_name}"
    
    @property
    def author_name(self):
        """Vrátí jméno autora nebo email."""
        return self.author.get_full_name() or self.author.email
    
    @property
    def author_role(self):
        """Vrátí roli autora."""
        if hasattr(self.author, 'role'):
            role_map = {
                'student': 'Student',
                'teacher': 'Učitel',
                'admin': 'Administrátor'
            }
            return role_map.get(self.author.role, self.author.role)
        return ''


class CompletedTopic(models.Model):
    """Sledování dokončených okruhů studenty."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='completed_topics',
        verbose_name=_('Uživatel')
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='completed_by',
        verbose_name=_('Okruh')
    )
    completed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Dokončeno')
    )
    
    class Meta:
        verbose_name = _('Dokončený okruh')
        verbose_name_plural = _('Dokončené okruhy')
        unique_together = [['user', 'topic']]
        indexes = [
            models.Index(fields=['user', 'topic']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.topic.name}"


class CompletedMaterial(models.Model):
    """Sledování dokončených materiálů studenty."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='completed_materials',
        verbose_name=_('Uživatel')
    )
    material = models.ForeignKey(
        'materials.Material',
        on_delete=models.CASCADE,
        related_name='completed_by',
        verbose_name=_('Materiál')
    )
    completed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Dokončeno')
    )
    
    class Meta:
        verbose_name = _('Dokončený materiál')
        verbose_name_plural = _('Dokončené materiály')
        unique_together = [['user', 'material']]
        indexes = [
            models.Index(fields=['user', 'material']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.material.title}"


class CompletedQuiz(models.Model):
    """Sledování dokončených testů studenty."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='completed_quizzes',
        verbose_name=_('Uživatel')
    )
    quiz = models.ForeignKey(
        'quizzes.Quiz',
        on_delete=models.CASCADE,
        related_name='completed_by',
        verbose_name=_('Test')
    )
    completed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Dokončeno')
    )
    
    class Meta:
        verbose_name = _('Dokončený test')
        verbose_name_plural = _('Dokončené testy')
        unique_together = [['user', 'quiz']]
        indexes = [
            models.Index(fields=['user', 'quiz']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.quiz.title}"

