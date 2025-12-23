"""
Management command pro opravu is_staff statusu pro konkrétního uživatele.
"""
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Nastaví is_staff=True pro konkrétního uživatele podle emailu'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email uživatele')

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'Nalezen uživatel: {user.email}')
            self.stdout.write(f'Aktuální role: {user.role}')
            self.stdout.write(f'Aktuální is_staff: {user.is_staff}')
            self.stdout.write(f'Aktuální is_active: {user.is_active}')
            self.stdout.write(f'Aktuální is_superuser: {user.is_superuser}')
            
            # Nastavit is_staff a is_active podle role
            update_fields = []
            if user.role in [User.Role.TEACHER, User.Role.ADMIN] or user.is_superuser:
                if not user.is_staff:
                    user.is_staff = True
                    update_fields.append('is_staff')
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Nastaveno is_staff=True pro uživatele {user.email}')
                    )
                if not user.is_active:
                    user.is_active = True
                    update_fields.append('is_active')
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Nastaveno is_active=True pro uživatele {user.email}')
                    )
                if not update_fields:
                    self.stdout.write(
                        self.style.WARNING(f'Uživatel {user.email} již má správné nastavení (is_staff=True, is_active=True)')
                    )
            elif user.role == User.Role.STUDENT and not user.is_superuser:
                if user.is_staff:
                    user.is_staff = False
                    update_fields.append('is_staff')
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Nastaveno is_staff=False pro uživatele {user.email} (student)')
                    )
                if not update_fields:
                    self.stdout.write(
                        self.style.WARNING(f'Uživatel {user.email} již má správné nastavení (is_staff=False)')
                    )
            
            if update_fields:
                user.save(update_fields=update_fields)
            
            # Zobrazit finální stav
            user.refresh_from_db()
            self.stdout.write(f'\nFinální stav:')
            self.stdout.write(f'  Role: {user.role}')
            self.stdout.write(f'  is_staff: {user.is_staff}')
            self.stdout.write(f'  is_active: {user.is_active}')
            self.stdout.write(f'  is_superuser: {user.is_superuser}')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Uživatel s emailem {email} nebyl nalezen')
            )

