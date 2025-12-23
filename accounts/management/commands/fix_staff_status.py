"""
Management command pro opravu is_staff statusu pro učitele a adminy.
Nastaví is_staff=True pro všechny uživatele s rolí učitele nebo admina.
"""
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Nastaví is_staff=True pro všechny učitele a adminy'

    def handle(self, *args, **options):
        # Najít všechny učitele a adminy bez is_staff=True
        teachers = User.objects.filter(role=User.Role.TEACHER, is_staff=False)
        admins = User.objects.filter(role=User.Role.ADMIN, is_staff=False)
        
        teacher_count = teachers.count()
        admin_count = admins.count()
        
        # Nastavit is_staff=True
        teachers.update(is_staff=True)
        admins.update(is_staff=True)
        
        # Nastavit is_staff=False pro studenty (pokud nejsou superuser)
        students = User.objects.filter(role=User.Role.STUDENT, is_staff=True).exclude(is_superuser=True)
        student_count = students.count()
        students.update(is_staff=False)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Opraveno: {teacher_count} učitelů, {admin_count} adminů nastaveno is_staff=True. '
                f'{student_count} studentů nastaveno is_staff=False.'
            )
        )

