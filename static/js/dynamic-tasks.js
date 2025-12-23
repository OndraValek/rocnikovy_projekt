/**
 * Dynamické načítání a zobrazování úloh z databáze
 */

class DynamicTasksLoader {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container s ID "${containerId}" nebyl nalezen`);
            return;
        }
        
        this.options = {
            topicId: options.topicId || null,
            apiEndpoint: options.apiEndpoint || '/api/tasks/',
            type: options.type || 'all', // 'materials', 'quizzes', 'all'
            perPage: options.perPage || 10,
            showFilters: options.showFilters !== false,
            showPagination: options.showPagination !== false,
            ...options
        };
        
        // Zkontrolovat, jestli je uživatel učitel/admin
        // Zkusit získat atribut z containeru
        let isTeacherAttr = this.container ? this.container.getAttribute('data-is-teacher') : null;
        let isStudentAttr = this.container ? this.container.getAttribute('data-is-student') : null;
        
        // Pokud není v containeru, zkusit najít dynamic-tasks-container
        if (!isTeacherAttr || !isStudentAttr) {
            const dynamicContainer = document.getElementById('dynamic-tasks-container');
            if (dynamicContainer) {
                if (!isTeacherAttr) {
                    isTeacherAttr = dynamicContainer.getAttribute('data-is-teacher');
                }
                if (!isStudentAttr) {
                    isStudentAttr = dynamicContainer.getAttribute('data-is-student');
                }
            }
        }
        
        this.isTeacher = isTeacherAttr === 'true';
        this.isStudent = isStudentAttr === 'true';
        
        this.currentPage = 1;
        this.currentFilters = {
            search: '',
            material_type: '',
            type: this.options.type
        };
        
        this.init();
    }
    
    init() {
        // Vytvořit UI
        this.createUI();
        
        // Načíst první stránku
        this.loadTasks();
        
        // Nastavit event listeners
        this.setupEventListeners();
    }
    
    createUI() {
        // Vytvořit filtry
        if (this.options.showFilters) {
            const filtersHTML = `
                <div class="mb-4">
                    <div class="row g-3">
                        <div class="col-md-4">
                            <input type="text" 
                                   id="task-search" 
                                   class="form-control" 
                                   placeholder="Vyhledat úlohy...">
                        </div>
                        <div class="col-md-3">
                            <select id="task-type-filter" class="form-select">
                                <option value="all">Všechny úlohy</option>
                                <option value="materials">Materiály</option>
                                <option value="quizzes">Testy</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <select id="material-type-filter" class="form-select" style="display: none;">
                                <option value="">Všechny typy</option>
                                <option value="pdf">PDF</option>
                                <option value="video">Video</option>
                                <option value="h5p">H5P</option>
                                <option value="text">Text</option>
                                <option value="image">Obrázek</option>
                                <option value="link">Odkaz</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <button id="task-load-btn" class="btn btn-primary w-100">
                                Načíst
                            </button>
                        </div>
                    </div>
                </div>
            `;
            this.container.insertAdjacentHTML('beforebegin', filtersHTML);
        }
        
        // Vytvořit container pro úlohy
        const tasksContainer = document.createElement('div');
        tasksContainer.id = 'tasks-container';
        tasksContainer.className = 'tasks-container';
        this.container.appendChild(tasksContainer);
        
        // Vytvořit container pro loading
        const loadingContainer = document.createElement('div');
        loadingContainer.id = 'tasks-loading';
        loadingContainer.className = 'text-center py-4';
        loadingContainer.style.display = 'none';
        loadingContainer.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Načítání...</span></div>';
        this.container.appendChild(loadingContainer);
        
        // Vytvořit container pro chyby
        const errorContainer = document.createElement('div');
        errorContainer.id = 'tasks-error';
        errorContainer.className = 'alert alert-danger';
        errorContainer.style.display = 'none';
        this.container.appendChild(errorContainer);
        
        // Vytvořit pagination
        if (this.options.showPagination) {
            const paginationContainer = document.createElement('nav');
            paginationContainer.id = 'tasks-pagination';
            paginationContainer.setAttribute('aria-label', 'Stránkování úloh');
            this.container.appendChild(paginationContainer);
        }
    }
    
    setupEventListeners() {
        // Vyhledávání
        const searchInput = document.getElementById('task-search');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.currentFilters.search = e.target.value;
                    this.currentPage = 1;
                    this.loadTasks();
                }, 500); // Debounce 500ms
            });
        }
        
        // Filtr typu
        const typeFilter = document.getElementById('task-type-filter');
        if (typeFilter) {
            typeFilter.addEventListener('change', (e) => {
                this.currentFilters.type = e.target.value;
                this.currentPage = 1;
                
                // Zobrazit/skrýt filtr typu materiálu
                const materialTypeFilter = document.getElementById('material-type-filter');
                if (materialTypeFilter) {
                    materialTypeFilter.style.display = 
                        e.target.value === 'materials' ? 'block' : 'none';
                }
                
                this.loadTasks();
            });
        }
        
        // Filtr typu materiálu
        const materialTypeFilter = document.getElementById('material-type-filter');
        if (materialTypeFilter) {
            materialTypeFilter.addEventListener('change', (e) => {
                this.currentFilters.material_type = e.target.value;
                this.currentPage = 1;
                this.loadTasks();
            });
        }
        
        // Tlačítko načíst
        const loadBtn = document.getElementById('task-load-btn');
        if (loadBtn) {
            loadBtn.addEventListener('click', () => {
                this.loadTasks();
            });
        }
    }
    
    async loadTasks() {
        if (!this.options.topicId) {
            this.showError('Topic ID není nastaven');
            return;
        }
        
        // Zobrazit loading
        this.showLoading(true);
        this.hideError();
        
        try {
            // Sestavit URL s parametry
            const params = new URLSearchParams({
                topic_id: this.options.topicId,
                type: this.currentFilters.type,
                page: this.currentPage,
                per_page: this.options.perPage,
            });
            
            if (this.currentFilters.search) {
                params.append('search', this.currentFilters.search);
            }
            
            if (this.currentFilters.material_type && this.currentFilters.type === 'materials') {
                params.append('material_type', this.currentFilters.material_type);
            }
            
            const url = `${this.options.apiEndpoint}?${params.toString()}`;
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.renderTasks(data.tasks || data.materials || data.quizzes || []);
                this.renderPagination(data.pagination);
            } else {
                throw new Error(data.error || 'Nepodařilo se načíst úlohy');
            }
            
        } catch (error) {
            console.error('Chyba při načítání úloh:', error);
            this.showError(`Chyba při načítání úloh: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }
    
    renderTasks(tasks) {
        const container = document.getElementById('tasks-container');
        if (!container) return;
        
        // Použít uložené hodnoty
        const isTeacher = this.isTeacher || false;
        const isStudent = this.isStudent || false;
        
        if (tasks.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <p class="mb-0">Žádné úlohy nenalezeny.</p>
                </div>
            `;
            return;
        }
        
        let html = '<div class="row g-3">';
        
        tasks.forEach(task => {
            if (task.type === 'material' || !task.type) {
                // Materiál
                const isCompleted = task.is_completed || false;
                html += `
                    <div class="col-md-6 col-lg-4">
                        <div class="card h-100 ${isCompleted ? 'task-completed' : ''}">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <div class="d-flex align-items-center gap-2">
                                        ${isStudent ? `
                                            <div class="form-check form-check-lg d-inline-flex align-items-center">
                                                <input class="form-check-input task-checkbox material-checkbox" 
                                                       type="checkbox" 
                                                       data-material-id="${task.id}"
                                                       id="material-checkbox-${task.id}"
                                                       ${isCompleted ? 'checked' : ''}
                                                       style="display: none;">
                                                <label class="form-check-label mb-0" for="material-checkbox-${task.id}" title="Označit jako dokončený">
                                                    <i class="bi ${isCompleted ? 'bi-check-circle-fill text-success' : 'bi-circle text-muted'}" style="font-size: 1.5rem;"></i>
                                                </label>
                                            </div>
                                        ` : ''}
                                        <h5 class="card-title mb-0">${this.escapeHtml(task.title)}</h5>
                                    </div>
                                    <span class="badge bg-secondary">${this.escapeHtml(task.material_type || task.material_type_display || 'Materiál')}</span>
                                </div>
                                ${task.description ? `<p class="card-text text-muted small">${this.escapeHtml(task.description.substring(0, 100))}${task.description.length > 100 ? '...' : ''}</p>` : ''}
                                <div class="mt-auto">
                                    <div class="d-flex gap-2">
                                        <a href="${task.url}" class="btn btn-sm btn-primary">Otevřít</a>
                                        ${isTeacher ? `
                                            <a href="/material/${task.id}/delete/" 
                                               class="btn btn-sm btn-danger" 
                                               onclick="return confirm('Opravdu chcete smazat materiál \\'${this.escapeHtml(task.title)}\\'? Tato akce je nevratná!');">
                                                <i class="bi bi-trash"></i> Smazat
                                            </a>
                                        ` : ''}
                                    </div>
                                    <small class="text-muted d-block mt-2">${task.created_at}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } else if (task.type === 'quiz') {
                // Test
                const attemptsInfo = task.user_attempts || {};
                const bestScore = attemptsInfo.best_score;
                const isCompleted = task.is_completed || false;
                
                html += `
                    <div class="col-md-6 col-lg-4">
                        <div class="card h-100 ${isCompleted ? 'task-completed' : ''}">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <div class="d-flex align-items-center gap-2">
                                        ${isStudent ? `
                                            <div class="form-check form-check-lg d-inline-flex align-items-center">
                                                <input class="form-check-input task-checkbox quiz-checkbox" 
                                                       type="checkbox" 
                                                       data-quiz-id="${task.id}"
                                                       id="quiz-checkbox-${task.id}"
                                                       ${isCompleted ? 'checked' : ''}
                                                       style="display: none;">
                                                <label class="form-check-label mb-0" for="quiz-checkbox-${task.id}" title="Označit jako dokončený">
                                                    <i class="bi ${isCompleted ? 'bi-check-circle-fill text-success' : 'bi-circle text-muted'}" style="font-size: 1.5rem;"></i>
                                                </label>
                                            </div>
                                        ` : ''}
                                        <h5 class="card-title mb-0">${this.escapeHtml(task.title)}</h5>
                                    </div>
                                    <span class="badge bg-primary">Test</span>
                                </div>
                                ${task.description ? `<p class="card-text text-muted small">${this.escapeHtml(task.description.substring(0, 100))}${task.description.length > 100 ? '...' : ''}</p>` : ''}
                                <div class="mt-2">
                                    ${task.time_limit ? `<small class="text-muted">⏱ ${task.time_limit} min</small><br>` : ''}
                                    ${bestScore !== null ? `
                                        <small class="text-muted">
                                            Nejlepší: ${bestScore}%
                                        </small>
                                    ` : ''}
                                </div>
                                <div class="mt-auto">
                                    <div class="d-flex gap-2">
                                        <a href="${task.url}" class="btn btn-sm btn-primary">Spustit test</a>
                                        ${isTeacher ? `
                                            <a href="/quiz/${task.id}/delete/" 
                                               class="btn btn-sm btn-danger" 
                                               onclick="return confirm('Opravdu chcete smazat test \\'${this.escapeHtml(task.title)}\\'? Tato akce je nevratná!');">
                                                <i class="bi bi-trash"></i> Smazat
                                            </a>
                                        ` : ''}
                                    </div>
                                    <small class="text-muted d-block mt-2">${task.created_at}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
        });
        
        html += '</div>';
        container.innerHTML = html;
        
        // Nastavit event listeners pro checkboxy (pouze pro studenty)
        if (isStudent) {
            this.setupCheckboxListeners();
        }
    }
    
    setupCheckboxListeners() {
        // Checkboxy pro materiály
        document.querySelectorAll('.material-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const materialId = parseInt(checkbox.getAttribute('data-material-id'));
                const completed = checkbox.checked;
                const card = checkbox.closest('.card');
                const icon = checkbox.nextElementSibling.querySelector('i');
                
                // Zobrazit loading stav
                const originalClass = icon.className;
                icon.className = 'bi bi-hourglass-split text-warning';
                checkbox.disabled = true;
                
                // Odeslat požadavek na API
                fetch('/api/completed-material/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        material_id: materialId,
                        completed: completed
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        if (completed) {
                            card.classList.add('task-completed');
                            icon.className = 'bi bi-check-circle-fill text-success';
                        } else {
                            card.classList.remove('task-completed');
                            icon.className = 'bi bi-circle text-muted';
                        }
                    } else {
                        checkbox.checked = !completed;
                        alert('Chyba: ' + (data.error || 'Nepodařilo se aktualizovat stav materiálu'));
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    checkbox.checked = !completed;
                    alert('Chyba při aktualizaci stavu materiálu');
                })
                .finally(() => {
                    checkbox.disabled = false;
                });
            });
        });
        
        // Checkboxy pro testy
        document.querySelectorAll('.quiz-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const quizId = parseInt(checkbox.getAttribute('data-quiz-id'));
                const completed = checkbox.checked;
                const card = checkbox.closest('.card');
                const icon = checkbox.nextElementSibling.querySelector('i');
                
                // Zobrazit loading stav
                const originalClass = icon.className;
                icon.className = 'bi bi-hourglass-split text-warning';
                checkbox.disabled = true;
                
                // Odeslat požadavek na API
                fetch('/api/completed-quiz/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        quiz_id: quizId,
                        completed: completed
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        if (completed) {
                            card.classList.add('task-completed');
                            icon.className = 'bi bi-check-circle-fill text-success';
                        } else {
                            card.classList.remove('task-completed');
                            icon.className = 'bi bi-circle text-muted';
                        }
                    } else {
                        checkbox.checked = !completed;
                        alert('Chyba: ' + (data.error || 'Nepodařilo se aktualizovat stav testu'));
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    checkbox.checked = !completed;
                    alert('Chyba při aktualizaci stavu testu');
                })
                .finally(() => {
                    checkbox.disabled = false;
                });
            });
        });
    }
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    renderPagination(pagination) {
        const container = document.getElementById('tasks-pagination');
        if (!container || !pagination) return;
        
        if (pagination.total_pages <= 1) {
            container.innerHTML = '';
            return;
        }
        
        let html = '<ul class="pagination justify-content-center">';
        
        // Předchozí
        html += `
            <li class="page-item ${!pagination.has_previous ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${pagination.page - 1}">Předchozí</a>
            </li>
        `;
        
        // Čísla stránek
        const startPage = Math.max(1, pagination.page - 2);
        const endPage = Math.min(pagination.total_pages, pagination.page + 2);
        
        if (startPage > 1) {
            html += `<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>`;
            if (startPage > 2) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }
        
        for (let i = startPage; i <= endPage; i++) {
            html += `
                <li class="page-item ${i === pagination.page ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `;
        }
        
        if (endPage < pagination.total_pages) {
            if (endPage < pagination.total_pages - 1) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
            html += `<li class="page-item"><a class="page-link" href="#" data-page="${pagination.total_pages}">${pagination.total_pages}</a></li>`;
        }
        
        // Další
        html += `
            <li class="page-item ${!pagination.has_next ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${pagination.page + 1}">Další</a>
            </li>
        `;
        
        html += '</ul>';
        container.innerHTML = html;
        
        // Event listeners pro pagination
        container.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = parseInt(link.getAttribute('data-page'));
                if (page && page !== this.currentPage) {
                    this.currentPage = page;
                    this.loadTasks();
                    // Scroll nahoru
                    this.container.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }
    
    showLoading(show) {
        const loading = document.getElementById('tasks-loading');
        if (loading) {
            loading.style.display = show ? 'block' : 'none';
        }
    }
    
    showError(message) {
        const error = document.getElementById('tasks-error');
        if (error) {
            error.textContent = message;
            error.style.display = 'block';
        }
    }
    
    hideError() {
        const error = document.getElementById('tasks-error');
        if (error) {
            error.style.display = 'none';
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Export pro použití v jiných skriptech
if (typeof window !== 'undefined') {
    window.DynamicTasksLoader = DynamicTasksLoader;
}

