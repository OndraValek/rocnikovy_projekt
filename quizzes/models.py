from django.db import models
from django.db.models import Avg, Count, Max
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
        help_text=_('Vložte iframe kód pro H5P test (starší způsob)')
    )
    h5p_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Cesta k H5P obsahu'),
        help_text=_('Relativní cesta k rozbalenému H5P obsahu (např. h5p/quiz-1/)')
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
    
    def get_user_statistics(self, user):
        """
        Vrátí statistiky pro konkrétního uživatele u tohoto testu.
        
        Returns:
            dict: {
                'attempt_count': int,
                'average_score': float nebo None,
                'last_attempt': QuizAttempt nebo None,
                'last_score': int nebo None,
                'last_date': datetime nebo None,
                'grade': int nebo None
            }
        """
        attempts = self.attempts.filter(user=user, completed_at__isnull=False)
        
        stats = {
            'attempt_count': attempts.count(),
            'average_score': None,
            'last_attempt': None,
            'last_score': None,
            'last_date': None,
            'grade': None
        }
        
        if attempts.exists():
            # Průměrné skóre
            avg = attempts.aggregate(Avg('score'))['score__avg']
            stats['average_score'] = round(avg, 1) if avg else None
            
            # Poslední pokus
            last_attempt = attempts.order_by('-completed_at').first()
            if last_attempt:
                stats['last_attempt'] = last_attempt
                stats['last_score'] = last_attempt.score
                stats['last_date'] = last_attempt.completed_at
                if last_attempt.score is not None:
                    stats['grade'] = self.calculate_grade(last_attempt.score)
        
        return stats
    
    @staticmethod
    def calculate_grade(score_percentage):
        """
        Vypočítá známku podle procentuálního skóre.
        
        Args:
            score_percentage: Procentuální skóre (0-100)
        
        Returns:
            int: Známka (1-5) nebo None pokud score není validní
        """
        if score_percentage is None:
            return None
        
        if score_percentage >= 85:
            return 1
        elif score_percentage >= 70:
            return 2
        elif score_percentage >= 55:
            return 3
        elif score_percentage >= 40:
            return 4
        else:
            return 5


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
    
    @property
    def grade(self):
        """Vrátí známku pro tento pokus."""
        if self.score is not None:
            return Quiz.calculate_grade(self.score)
        return None


class H5PUserData(models.Model):
    """Ukládání stavu uživatele v H5P obsahu (pro h5p-standalone)."""
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='h5p_user_data',
        verbose_name=_('Uživatel')
    )
    content_id = models.CharField(
        max_length=100,
        verbose_name=_('ID H5P obsahu'),
        help_text=_('Unikátní identifikátor H5P obsahu')
    )
    data = models.JSONField(
        verbose_name=_('Data stavu'),
        help_text=_('JSON data s uloženým stavem uživatele')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Aktualizováno')
    )
    
    class Meta:
        verbose_name = _('H5P uživatelská data')
        verbose_name_plural = _('H5P uživatelská data')
        unique_together = [['user', 'content_id']]
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user} - {self.content_id}"

