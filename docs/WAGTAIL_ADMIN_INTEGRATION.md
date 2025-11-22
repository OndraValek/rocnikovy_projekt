# Integrace Django modelů do Wagtail Admin

Wagtail umožňuje spravovat Django modely přímo v Wagtail admin rozhraní. Existují dva hlavní způsoby:

## 1. Wagtail Snippets (jednodušší)

Pro jednoduché modely, které nejsou stránky (např. Quiz, Material, Subject).

### Jak to funguje:

1. Model musí dědit z `models.Model` (ne `Page`)
2. Zaregistruješ ho jako snippet v `wagtail_hooks.py`
3. Objeví se v Wagtail adminu v sekci "Snippets"

### Příklad pro Quiz:

Vytvoř soubor `quizzes/wagtail_hooks.py`:

```python
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import Quiz, QuizAttempt, H5PUserData


@register_snippet
class Quiz(models.Model):
    # ... existující model ...
    pass


# Nebo s vlastním ViewSet pro lepší kontrolu:
class QuizViewSet(SnippetViewSet):
    model = Quiz
    icon = "form"  # Ikona v menu
    menu_label = "Testy"  # Název v menu
    menu_order = 200  # Pořadí v menu
    add_to_admin_menu = True  # Zobrazit v hlavním menu


register_snippet(QuizViewSet)
```

## 2. Wagtail ModelAdmin (pokročilejší)

Pro plnou správu modelů s více možnostmi (filtry, vyhledávání, hromadné akce).

### Instalace:

1. Přidej do `INSTALLED_APPS` v `settings/base.py`:
```python
INSTALLED_APPS = [
    # ... existující ...
    'wagtail.contrib.modeladmin',  # ← přidej toto
    # ...
]
```

2. Vytvoř `quizzes/wagtail_hooks.py`:

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Quiz, QuizAttempt, H5PUserData, Subject, Topic


class QuizModelAdmin(ModelAdmin):
    model = Quiz
    menu_label = 'Testy'  # Název v menu
    menu_icon = 'form'  # Ikona
    menu_order = 200  # Pořadí
    add_to_settings_menu = False  # Ne v Settings, ale v hlavním menu
    list_display = ('title', 'topic', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'topic__subject', 'created_at')
    search_fields = ('title', 'description')
    list_export = ('title', 'topic', 'author', 'is_published')  # Export do CSV


class QuizAttemptModelAdmin(ModelAdmin):
    model = QuizAttempt
    menu_label = 'Pokusy o testy'
    menu_icon = 'clipboard-list'
    menu_order = 201
    list_display = ('user', 'quiz', 'score', 'is_passed', 'started_at')
    list_filter = ('is_passed', 'quiz__topic__subject', 'started_at')
    search_fields = ('user__email', 'quiz__title')


class H5PUserDataModelAdmin(ModelAdmin):
    model = H5PUserData
    menu_label = 'H5P uživatelská data'
    menu_icon = 'code'
    menu_order = 202
    list_display = ('user', 'content_id', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('user__email', 'content_id')


# Registrace
modeladmin_register(QuizModelAdmin)
modeladmin_register(QuizAttemptModelAdmin)
modeladmin_register(H5PUserDataModelAdmin)
```

## 3. Pro Materials, Subjects, Topics

Vytvoř `subjects/wagtail_hooks.py`:

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Subject, Topic


class SubjectModelAdmin(ModelAdmin):
    model = Subject
    menu_label = 'Předměty'
    menu_icon = 'folder'
    menu_order = 100
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')


class TopicModelAdmin(ModelAdmin):
    model = Topic
    menu_label = 'Okruhy'
    menu_icon = 'folder-open'
    menu_order = 101
    list_display = ('name', 'subject', 'slug', 'created_at')
    list_filter = ('subject',)
    search_fields = ('name', 'description')


modeladmin_register(SubjectModelAdmin)
modeladmin_register(TopicModelAdmin)
```

A `materials/wagtail_hooks.py`:

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Material


class MaterialModelAdmin(ModelAdmin):
    model = Material
    menu_label = 'Materiály'
    menu_icon = 'doc-full'
    menu_order = 150
    list_display = ('title', 'topic', 'material_type', 'author', 'created_at')
    list_filter = ('material_type', 'topic__subject', 'created_at')
    search_fields = ('title', 'description')


modeladmin_register(MaterialModelAdmin)
```

## 4. Pro Forum

Vytvoř `forum/wagtail_hooks.py`:

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import ForumThread, ForumPost


class ForumThreadModelAdmin(ModelAdmin):
    model = ForumThread
    menu_label = 'Diskusní vlákna'
    menu_icon = 'comments'
    menu_order = 300
    list_display = ('title', 'topic', 'author', 'is_pinned', 'is_locked', 'created_at')
    list_filter = ('is_pinned', 'is_locked', 'topic__subject', 'created_at')
    search_fields = ('title',)


class ForumPostModelAdmin(ModelAdmin):
    model = ForumPost
    menu_label = 'Příspěvky'
    menu_icon = 'comment'
    menu_order = 301
    list_display = ('thread', 'author', 'created_at')
    list_filter = ('thread__topic__subject', 'created_at')
    search_fields = ('content',)


modeladmin_register(ForumThreadModelAdmin)
modeladmin_register(ForumPostModelAdmin)
```

## Výhody Wagtail ModelAdmin:

✅ **Jednotné rozhraní** - vše v jednom Wagtail adminu
✅ **Lepší UX** - modernější design než Django Admin
✅ **Filtry a vyhledávání** - snadné hledání
✅ **Export** - možnost exportovat data do CSV
✅ **Hromadné akce** - možnost hromadných operací
✅ **Ikony a pořadí** - přizpůsobení menu

## Po implementaci:

1. Restartuj Django server
2. Jdi do Wagtail adminu (`/admin/`)
3. V levém menu uvidíš nové sekce:
   - Předměty
   - Okruhy
   - Materiály
   - Testy
   - Pokusy o testy
   - Diskusní vlákna
   - atd.

## Porovnání:

| Funkce | Django Admin | Wagtail Snippets | Wagtail ModelAdmin |
|--------|--------------|------------------|-------------------|
| Jednoduchost | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Možnosti | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Design | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Filtry | ✅ | ❌ | ✅ |
| Export | ❌ | ❌ | ✅ |
| Hromadné akce | ✅ | ❌ | ✅ |

## Doporučení:

- **Pro jednoduché modely**: Použij **Wagtail Snippets**
- **Pro složitější modely s filtry**: Použij **Wagtail ModelAdmin**

