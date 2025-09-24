from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class SubjectIndexPage(Page):
	intro = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel("intro"),
	]

	template = "subjects/subject_index_page.html"


class SubjectPage(Page):
	description = RichTextField(blank=True)

	# Example: later we can add a StreamField for materials, or a relation to Material objects
	content_panels = Page.content_panels + [
		FieldPanel("description"),
	]

	template = "subjects/subject_page.html"
