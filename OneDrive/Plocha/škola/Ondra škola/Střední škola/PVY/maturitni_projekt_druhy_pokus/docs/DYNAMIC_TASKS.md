# Dynamické načítání úloh z databáze

## Přehled

Systém pro dynamické načítání a zobrazování úloh (materiálů a testů) z databáze pomocí AJAX. Úlohy se načítají asynchronně bez obnovení stránky.

## Funkce

✅ **Dynamické načítání** - Úlohy se načítají z databáze přes API
✅ **Filtrování** - Podle typu (materiály/testy), typu materiálu, vyhledávání
✅ **Stránkování** - Automatické stránkování výsledků
✅ **Responzivní design** - Kartové zobrazení úloh
✅ **Informace o pokusech** - Zobrazuje počet pokusů a nejlepší skóre u testů

## API Endpointy

### 1. Všechny úlohy (materiály + testy)

**URL:** `/api/tasks/`

**Metoda:** GET

**Parametry:**
- `topic_id` (povinné) - ID okruhu
- `type` - `all`, `materials`, nebo `quizzes` (default: `all`)
- `search` - Vyhledávání v názvu a popisu
- `page` - Číslo stránky (default: 1)
- `per_page` - Počet na stránku (default: 10)

**Příklad:**
```
GET /api/tasks/?topic_id=1&type=all&search=programování&page=1&per_page=12
```

**Odpověď:**
```json
{
    "success": true,
    "tasks": [
        {
            "id": 1,
            "type": "material",
            "title": "Základy programování",
            "description": "...",
            "material_type": "PDF dokument",
            "url": "/materials/1/",
            "created_at": "15.11.2024"
        },
        {
            "id": 2,
            "type": "quiz",
            "title": "Test z programování",
            "description": "...",
            "time_limit": 30,
            "max_attempts": 3,
            "url": "/quiz/2/",
            "user_attempts": {
                "count": 1,
                "best_score": 85
            },
            "can_attempt": true,
            "created_at": "15.11.2024"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 12,
        "total_pages": 2,
        "total_count": 20,
        "has_next": true,
        "has_previous": false
    }
}
```

### 2. Pouze materiály

**URL:** `/api/materials/`

**Parametry:**
- `topic_id` (povinné)
- `material_type` - `pdf`, `video`, `h5p`, `text`, `image`, `link`
- `search` - Vyhledávání
- `page`, `per_page` - Stránkování

### 3. Pouze testy

**URL:** `/api/quizzes/`

**Parametry:**
- `topic_id` (povinné)
- `search` - Vyhledávání
- `page`, `per_page` - Stránkování

## Použití v JavaScriptu

### Základní použití

```javascript
const loader = new DynamicTasksLoader('container-id', {
    topicId: 1,
    apiEndpoint: '/api/tasks/',
    type: 'all',
    perPage: 12,
    showFilters: true,
    showPagination: true
});
```

### Možnosti konfigurace

- `topicId` - ID okruhu (povinné)
- `apiEndpoint` - URL API endpointu (default: `/api/tasks/`)
- `type` - `all`, `materials`, nebo `quizzes` (default: `all`)
- `perPage` - Počet úloh na stránku (default: 10)
- `showFilters` - Zobrazit filtry (default: true)
- `showPagination` - Zobrazit stránkování (default: true)

### Příklad v šabloně

```html
<div id="dynamic-tasks-container" data-topic-id="{{ topic.id }}"></div>

<script src="{% static 'js/dynamic-tasks.js' %}"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const container = document.getElementById('dynamic-tasks-container');
        const topicId = container.getAttribute('data-topic-id');
        
        const loader = new DynamicTasksLoader('dynamic-tasks-container', {
            topicId: topicId,
            apiEndpoint: '{% url "subjects:api_tasks" %}',
            type: 'all',
            perPage: 12,
            showFilters: true,
            showPagination: true
        });
    });
</script>
```

## Funkce

### Filtrování

- **Vyhledávání** - Automatické vyhledávání při psaní (debounce 500ms)
- **Typ úlohy** - Filtrovat materiály, testy, nebo všechny
- **Typ materiálu** - Filtrovat podle typu materiálu (PDF, video, H5P, atd.)

### Stránkování

- Automatické stránkování výsledků
- Navigace mezi stránkami
- Zobrazení celkového počtu úloh

### Zobrazení

- **Kartové zobrazení** - Každá úloha je zobrazena jako karta
- **Informace o testech** - Počet pokusů, nejlepší skóre, časový limit
- **Responzivní design** - 3 sloupce na desktopu, 2 na tabletu, 1 na mobilu

## Struktura souborů

- `subjects/api_views.py` - API endpointy
- `static/js/dynamic-tasks.js` - JavaScript třída pro načítání
- `templates/subjects/topic_detail.html` - Šablona s integrací
- `subjects/urls.py` - URL routing

## Bezpečnost

- Všechny API endpointy vyžadují přihlášení (`LoginRequiredMixin`)
- Filtrují pouze publikované materiály a testy
- Kontrolují oprávnění uživatele

## Budoucí vylepšení

- [ ] Uložení filtrů do localStorage
- [ ] Infinite scroll místo stránkování
- [ ] Drag & drop řazení
- [ ] Export výsledků
- [ ] Statistiky pro učitele

