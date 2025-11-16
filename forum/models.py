from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class ForumThread(models.Model):
    """Diskusní vlákno k okruhu."""
    topic = models.ForeignKey(
        'subjects.Topic',
        on_delete=models.CASCADE,
        related_name='forum_threads',
        verbose_name=_('Okruh')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Nadpis')
    )
    slug = models.SlugField(
        max_length=200,
        editable=False
    )
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='forum_threads',
        verbose_name=_('Autor')
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name=_('Připnuto')
    )
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_('Zamčeno')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Počet zobrazení')
    )
    
    class Meta:
        verbose_name = _('Diskusní vlákno')
        verbose_name_plural = _('Diskusní vlákna')
        ordering = ['-is_pinned', '-updated_at']
    
    def __str__(self):
        return f"{self.topic.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_last_post(self):
        """Vrátí poslední příspěvek ve vlákně."""
        return self.posts.order_by('-created_at').first()
    
    def get_post_count(self):
        """Vrátí počet příspěvků ve vlákně."""
        return self.posts.count()


class ForumPost(models.Model):
    """Příspěvek v diskusním vlákně."""
    thread = models.ForeignKey(
        ForumThread,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Vlákno')
    )
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='forum_posts',
        verbose_name=_('Autor')
    )
    content = models.TextField(
        verbose_name=_('Obsah')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(
        default=False,
        verbose_name=_('Upraveno')
    )
    
    class Meta:
        verbose_name = _('Příspěvek')
        verbose_name_plural = _('Příspěvky')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Příspěvek od {self.author} v {self.thread.title}"
    
    def save(self, *args, **kwargs):
        # Aktualizovat updated_at vlákna při vytvoření nového příspěvku
        super().save(*args, **kwargs)
        if self.thread:
            self.thread.updated_at = self.created_at
            self.thread.save(update_fields=['updated_at'])

