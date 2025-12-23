from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Rozšířený uživatelský model s rolemi."""
    
    class Role(models.TextChoices):
        STUDENT = 'student', _('Student')
        TEACHER = 'teacher', _('Učitel')
        ADMIN = 'admin', _('Administrátor')
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name=_('Role')
    )
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    class_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Třída'),
        help_text=_('Např. 4.A, 4.B')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('Uživatel')
        verbose_name_plural = _('Uživatelé')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email
    
    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
    
    @property
    def is_teacher(self):
        """Vrátí True, pokud je uživatel učitel nebo admin."""
        return self.role == self.Role.TEACHER or self.role == self.Role.ADMIN or self.is_superuser
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
    
    def save(self, *args, **kwargs):
        """
        Přepsat save metodu, aby automaticky nastavila is_staff a is_active podle role.
        """
        # Před uložením nastavit is_staff a is_active podle role
        if self.role in [self.Role.TEACHER, self.Role.ADMIN] or self.is_superuser:
            self.is_staff = True
            self.is_active = True  # Učitelé a admini musí být aktivní pro přístup do Wagtail
        elif self.role == self.Role.STUDENT and not self.is_superuser:
            self.is_staff = False
            # Studenti mohou být aktivní (pro přístup do aplikace)
        
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """Rozšířený profil uživatele."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Uživatel')
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('O mně')
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name=_('Profilový obrázek')
    )
    favorite_topics = models.ManyToManyField(
        'subjects.Topic',
        blank=True,
        related_name='favorited_by',
        verbose_name=_('Oblíbené okruhy')
    )
    
    class Meta:
        verbose_name = _('Profil uživatele')
        verbose_name_plural = _('Profily uživatelů')
    
    def __str__(self):
        return f"Profil uživatele {self.user}"


class StudentClass(models.Model):
    """Třída/skupina studentů spravovaná učitelem."""
    name = models.CharField(
        max_length=100,
        verbose_name=_('Název třídy'),
        help_text=_('Např. 4.A, Skupina A, Třída 2024')
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_classes',
        limit_choices_to={'role': User.Role.TEACHER},
        verbose_name=_('Učitel'),
        help_text=_('Učitel, který spravuje tuto třídu')
    )
    students = models.ManyToManyField(
        User,
        related_name='student_classes',
        limit_choices_to={'role': User.Role.STUDENT},
        blank=True,
        verbose_name=_('Studenti'),
        help_text=_('Studenti v této třídě')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Popis'),
        help_text=_('Volitelný popis třídy')
    )
    school_year = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Školní rok'),
        help_text=_('Např. 2024/2025')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Třída')
        verbose_name_plural = _('Třídy')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.teacher.get_full_name() or self.teacher.email})"
    
    def get_student_count(self):
        """Vrátí počet studentů ve třídě."""
        return self.students.count()
    
    get_student_count.short_description = _('Počet studentů')
