from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """Domovská stránka."""
    body = RichTextField(blank=True, features=['bold', 'italic', 'link', 'ol', 'ul', 'h2', 'h3'])
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "Domovská stránka"

