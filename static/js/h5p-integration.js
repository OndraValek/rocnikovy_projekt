/**
 * H5P Integration - JavaScript pro zachycení výsledků z H5P testů
 * 
 * Tento skript naslouchá na H5P postMessage události a ukládá výsledky
 * do Django aplikace přes API endpoint.
 */

(function() {
    'use strict';

    // Konfigurace
    const H5P_CONFIG = {
        apiEndpoint: '/api/h5p/results/',  // API endpoint pro ukládání výsledků
        csrfToken: getCookie('csrftoken'),  // CSRF token pro Django
    };

    /**
     * Získat CSRF token z cookies
     */
    function getCookie(name) {
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

    /**
     * Získat quiz ID z URL nebo data atributu
     */
    function getQuizId() {
        // Zkus získat z data atributu
        const quizElement = document.querySelector('[data-quiz-id]');
        if (quizElement) {
            return quizElement.getAttribute('data-quiz-id');
        }
        
        // Zkus získat z URL
        const urlMatch = window.location.pathname.match(/\/quizzes\/(\d+)\//);
        if (urlMatch) {
            return urlMatch[1];
        }
        
        return null;
    }

    /**
     * Získat attempt ID z URL nebo data atributu
     */
    function getAttemptId() {
        const attemptElement = document.querySelector('[data-attempt-id]');
        if (attemptElement) {
            return attemptElement.getAttribute('data-attempt-id');
        }
        
        const urlMatch = window.location.pathname.match(/\/attempts\/(\d+)\//);
        if (urlMatch) {
            return urlMatch[1];
        }
        
        return null;
    }

    /**
     * Odeslat výsledky na server
     */
    async function sendResults(quizId, attemptId, results) {
        if (!quizId) {
            console.warn('H5P Integration: Quiz ID není k dispozici');
            return;
        }

        const payload = {
            quiz_id: quizId,
            attempt_id: attemptId,
            score: results.score,
            max_score: results.maxScore,
            time_spent: results.timeSpent,
            answers: results.answers,
            completed: results.completed
        };

        try {
            const response = await fetch(H5P_CONFIG.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': H5P_CONFIG.csrfToken
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const data = await response.json();
                console.log('H5P Integration: Výsledky uloženy', data);
                
                // Zobrazit notifikaci
                showNotification('Výsledky byly uloženy', 'success');
            } else {
                console.error('H5P Integration: Chyba při ukládání výsledků', response);
                showNotification('Chyba při ukládání výsledků', 'error');
            }
        } catch (error) {
            console.error('H5P Integration: Chyba při odesílání výsledků', error);
            showNotification('Chyba při ukládání výsledků', 'error');
        }
    }

    /**
     * Zobrazit notifikaci
     */
    function showNotification(message, type) {
        // Jednoduchá notifikace - můžeš použít Bootstrap toast nebo jiný systém
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);
        
        // Automaticky odstranit po 5 sekundách
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    /**
     * Zpracovat H5P postMessage událost
     */
    function handleH5PMessage(event) {
        // H5P posílá výsledky přes postMessage
        // Struktura závisí na typu H5P obsahu
        
        if (event.data && event.data.context === 'h5p') {
            const data = event.data;
            
            // Různé typy H5P událostí
            if (data.event === 'xAPI' && data.statement) {
                // xAPI statement - standardní formát pro vzdělávací obsah
                const statement = data.statement;
                
                if (statement.verb && statement.verb.id === 'http://adlnet.gov/expapi/verbs/completed') {
                    // Test byl dokončen
                    const results = {
                        score: statement.result?.score?.scaled ? 
                            Math.round(statement.result.score.scaled * 100) : null,
                        maxScore: statement.result?.score?.max || 100,
                        timeSpent: statement.result?.duration ? 
                            statement.result.duration.replace('PT', '').replace('S', '') : null,
                        answers: statement.result?.response || null,
                        completed: true
                    };
                    
                    const quizId = getQuizId();
                    const attemptId = getAttemptId();
                    
                    if (quizId) {
                        sendResults(quizId, attemptId, results);
                    }
                }
            } else if (data.event === 'resize') {
                // H5P změnil velikost - můžeš upravit iframe
                const iframe = event.source.frameElement;
                if (iframe && data.height) {
                    iframe.style.height = data.height + 'px';
                }
            }
        }
    }

    /**
     * Inicializace
     */
    function init() {
        // Naslouchat na postMessage události z H5P iframe
        window.addEventListener('message', handleH5PMessage, false);
        
        console.log('H5P Integration: Inicializováno');
    }

    // Spustit po načtení DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

