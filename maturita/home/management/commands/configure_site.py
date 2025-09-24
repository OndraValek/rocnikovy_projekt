from django.core.management.base import BaseCommand

from wagtail.models import Page, Site


class Command(BaseCommand):
    help = "Configure default Wagtail Site to point to Home page and publish it."

    def handle(self, *args, **options):
        # Find an existing Home page (depth=2 created by initial migration)
        home_page = (
            Page.objects.type("home.HomePage").order_by("path").first()
        )

        if not home_page:
            self.stderr.write(
                self.style.ERROR("Home page (home.HomePage) not found.")
            )
            return

        # Ensure page is published
        if not home_page.live:
            revision = home_page.save_revision()
            revision.publish()
            self.stdout.write(self.style.SUCCESS("Published Home page."))
        else:
            self.stdout.write("Home page already published.")

        # Configure default site
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            site = Site(is_default_site=True)

        site.hostname = "127.0.0.1"
        site.port = 8000
        site.root_page = home_page
        site.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Site configured: host={site.hostname}:{site.port}, root='{home_page.title}'"
            )
        )


