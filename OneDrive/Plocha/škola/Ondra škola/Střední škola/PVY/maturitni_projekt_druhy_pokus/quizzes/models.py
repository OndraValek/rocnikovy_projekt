from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from modelcluster.models import ClusterableModel


class Quiz(ClusterableModel):
    """Test/kvíz připojený k okruhu."""
    topic = models.ForeignKey(
        'subjects.Topic',
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name=_('Okruh')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Název testu')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Popis')
    )
    
    # H5P integrace
    h5p_embed_code = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('H5P embed kód'),
        help_text=_('Vložte iframe kód pro H5P test')
    )
    
    # Alternativně: vlastní otázky (pro budoucí rozšíření)
    # questions = models.ManyToManyField('Question', blank=True)
    
    # Metadata
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_quizzes',
        verbose_name=_('Autor')
    )
    time_limit = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Časový limit (minuty)'),
        help_text=_('Prázdné = bez limitu')
    )
    max_attempts = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Maximální počet pokusů')
    )
    passing_score = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Procentuální úspěšnost pro úspěch'),
        help_text=_('0-100')
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Publikováno')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Test')
        verbose_name_plural = _('Testy')
        ordering = ['topic', 'created_at']
    
    def __str__(self):
        return f"{self.topic.name} - {self.title}"


class QuizAttempt(models.Model):
    """Pokus studenta o vyplnění testu."""
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name=_('Test')
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name=_('Uživatel')
    )
    score = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Skóre (%)')
    )
    is_passed = models.BooleanField(
        default=False,
        verbose_name=_('Úspěšně dokončeno')
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Dokončeno')
    )
    # Pro uložení odpovědí (JSON)
    answers_data = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_('Data odpovědí')
    )
    
    class Meta:
        verbose_name = _('Pokus o test')
        verbose_name_plural = _('Pokusy o testy')
        ordering = ['-started_at']
        unique_together = [['quiz', 'user', 'started_at']]  # Aby se dalo mít více pokusů
    
    def __str__(self):
        return f"{self.user} - {self.quiz.title} ({self.started_at})"
    
    def calculate_score(self):
        """Vypočítá skóre a označí jako úspěšné, pokud je dosaženo passing_score."""
        # Tato metoda by měla být implementována podle typu testu
        # Pro H5P testy se skóre může získat z H5P API
        if self.score is not None:
            self.is_passed = self.score >= self.quiz.passing_score
            self.save()
        return self.score

