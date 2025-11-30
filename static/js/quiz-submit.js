/**
 * JavaScript pro odeslání výsledků H5P testu
 */

// Globální proměnná pro uložení výsledků z xAPI
window.h5pLastResults = null;

// Funkce pro extrakci skóre z textu
function extractScoreFromText(text) {
    if (!text) return null;
    
    console.log('extractScoreFromText volána, délka textu:', text.length);
    
    // Různé patterny pro různé formáty - zkusit všechny možné varianty
    const patterns = [
        /got\s+(\d+)\s+of\s+(\d+)\s+correct/i,           // "You got 1 of 5 correct"
        /(\d+)\s+of\s+(\d+)\s+correct/i,                  // "1 of 5 correct"
        /(\d+)\s+of\s+(\d+)/i,                            // "1 of 5"
        /(\d+)\s*\/\s*(\d+)/,                             // "1/5"
        /score[:\s]+(\d+)\s*\/\s*(\d+)/i,                // "Score: 1/5"
        /(\d+)\s*z\s*(\d+)/i,                             // "1 z 5" (česky)
        /(\d+)\s+ze\s+(\d+)/i,                            // "1 ze 5" (česky)
        /(\d+)\s+out\s+of\s+(\d+)/i,                      // "1 out of 5"
        /(\d+)\s+correct\s+out\s+of\s+(\d+)/i,           // "1 correct out of 5"
    ];
    
    for (let i = 0; i < patterns.length; i++) {
        const pattern = patterns[i];
        const match = text.match(pattern);
        if (match) {
            const score = parseInt(match[1]);
            const maxScore = parseInt(match[2]);
            console.log('Pattern', i, 'match:', match[0], 'score:', score, 'maxScore:', maxScore);
            if (!isNaN(score) && !isNaN(maxScore) && score >= 0 && maxScore > 0 && score <= maxScore) {
                console.log('extractScoreFromText našel:', score, '/', maxScore, 'pattern:', pattern);
                return {
                    score: score,
                    max_score: maxScore
                };
            }
        }
    }
    
    // Zkusit najít čísla, která vypadají jako skóre (např. "1" a "5" blízko sebe)
    const numberPairs = text.match(/(\d+)\s*(?:of|z|ze|\/|out\s+of)\s*(\d+)/gi);
    if (numberPairs) {
        console.log('numberPairs nalezeny:', numberPairs);
        for (let pair of numberPairs) {
            const match = pair.match(/(\d+)\s*(?:of|z|ze|\/|out\s+of)\s*(\d+)/i);
            if (match) {
                const score = parseInt(match[1]);
                const maxScore = parseInt(match[2]);
                if (!isNaN(score) && !isNaN(maxScore) && score >= 0 && maxScore > 0 && score <= maxScore) {
                    console.log('extractScoreFromText našel z numberPairs:', score, '/', maxScore);
                    return {
                        score: score,
                        max_score: maxScore
                    };
                }
            }
        }
    }
    
    // Zkusit najít všechna čísla v textu a zkontrolovat, jestli některá vypadají jako skóre
    // Toto použijeme jen jako poslední možnost a s přísnějšími kontrolami
    const allNumbers = text.match(/\d+/g);
    if (allNumbers && allNumbers.length >= 2) {
        console.log('Všechna čísla v textu:', allNumbers);
        // Zkusit najít dvojice čísel, která by mohla být skóre
        // Ale jen pokud jsou blízko sebe a obsahují klíčová slova
        for (let i = 0; i < allNumbers.length - 1; i++) {
            const num1 = parseInt(allNumbers[i]);
            const num2 = parseInt(allNumbers[i + 1]);
            if (!isNaN(num1) && !isNaN(num2) && num1 >= 0 && num2 > 0 && num1 <= num2 && num2 <= 100) {
                // Zkontrolovat, jestli jsou tato čísla blízko sebe v textu
                const index1 = text.indexOf(allNumbers[i]);
                const index2 = text.indexOf(allNumbers[i + 1], index1);
                if (index2 !== -1 && index2 - index1 < 30) {
                    // Zkontrolovat, jestli mezi nimi jsou klíčová slova (of, /, correct, atd.)
                    const textBetween = text.substring(index1, index2 + allNumbers[i + 1].length).toLowerCase();
                    const hasKeywords = /of|correct|score|z|ze|\//.test(textBetween);
                    
                    if (hasKeywords) {
                        // Jsou blízko sebe a obsahují klíčová slova, pravděpodobně je to skóre
                        console.log('Možné skóre nalezeno (s klíčovými slovy):', num1, '/', num2, 'text:', textBetween);
                        return {
                            score: num1,
                            max_score: num2
                        };
                    }
                }
            }
        }
    }
    
    console.log('extractScoreFromText nenašel žádné skóre');
    return null;
}

// MutationObserver pro sledování změn v DOM
let scoreObserver = null;
function startScoreObserver() {
    if (scoreObserver) return; // Už běží
    
    // Také naslouchat na postMessage z iframe
    window.addEventListener('message', function(event) {
        // Zkontrolovat, jestli je zpráva z H5P iframe
        if (event.data && typeof event.data === 'object') {
            // Zkusit získat skóre z různých formátů zpráv
            if (event.data.type === 'h5p-score' || event.data.score !== undefined) {
                const score = event.data.score;
                const maxScore = event.data.maxScore || event.data.max_score || 100;
                if (score !== null && score !== undefined) {
                    window.h5pLastResults = {
                        score: score,
                        max_score: maxScore
                    };
                    console.log('H5P výsledky získány z postMessage:', window.h5pLastResults);
                }
            }
            
            // Zkusit získat text z zprávy
            if (event.data.text || event.data.content) {
                const text = event.data.text || event.data.content || '';
                const results = extractScoreFromText(text);
                if (results) {
                    window.h5pLastResults = results;
                    console.log('H5P výsledky získány z postMessage text:', results);
                }
            }
        }
    });
    
    scoreObserver = new MutationObserver(function(mutations) {
        // Zkusit získat skóre při každé změně
        const h5pContainer = document.getElementById('h5p-container') || document.querySelector('.h5p-container');
        if (h5pContainer) {
            // Zkusit různé způsoby získání textu
            const texts = [
                h5pContainer.innerText || '',
                h5pContainer.textContent || '',
                h5pContainer.innerHTML || ''
            ];
            
            for (let text of texts) {
                if (text && text.length > 0) {
                    const results = extractScoreFromText(text);
                    if (results) {
                        window.h5pLastResults = results;
                        console.log('H5P výsledky získány z MutationObserver:', results);
                        // Můžeme zastavit observer, protože jsme našli výsledky
                        if (scoreObserver) {
                            scoreObserver.disconnect();
                            scoreObserver = null;
                        }
                        return;
                    }
                }
            }
            
            // Také zkusit prohledat všechny potomky
            const allText = h5pContainer.innerText || h5pContainer.textContent || '';
            if (allText && allText.length > 0) {
                const results = extractScoreFromText(allText);
                if (results) {
                    window.h5pLastResults = results;
                    console.log('H5P výsledky získány z MutationObserver (všechny potomky):', results);
                    if (scoreObserver) {
                        scoreObserver.disconnect();
                        scoreObserver = null;
                    }
                    return;
                }
            }
            
            // Zkusit najít iframe a poslat mu zprávu
            const iframes = h5pContainer.querySelectorAll('iframe');
            for (let iframe of iframes) {
                try {
                    iframe.contentWindow.postMessage({type: 'get-score'}, '*');
                    iframe.contentWindow.postMessage({type: 'get-text'}, '*');
                } catch (e) {
                    // Ignorovat CORS chyby
                }
            }
        }
        
        // Také zkusit prohledat celý dokument při změně
        const bodyText = document.body.innerText || document.body.textContent || '';
        if (bodyText && bodyText.length > 0) {
            const results = extractScoreFromText(bodyText);
            if (results) {
                window.h5pLastResults = results;
                console.log('H5P výsledky získány z MutationObserver (celý dokument):', results);
                if (scoreObserver) {
                    scoreObserver.disconnect();
                    scoreObserver = null;
                }
            }
        }
    });
    
    // Sledovat celý dokument, ne jen H5P kontejner
    scoreObserver.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true
    });
    console.log('MutationObserver spuštěn pro sledování H5P výsledků (celý dokument)');
}

// Funkce pro získání CSRF tokenu
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

// Funkce pro získání výsledků z H5P
function getH5PResults() {
    try {
        console.log('Zkouším získat H5P výsledky...');
        
        // 1. Zkusit použít uložené výsledky z xAPI (nejspolehlivější)
        if (window.h5pLastResults) {
            console.log('H5P výsledky získány z cache (xAPI/interval):', window.h5pLastResults);
            return window.h5pLastResults;
        }
        
        // 1.5. Zkusit získat instanci různými způsoby
        let h5pInstance = window.h5pInstance;
        console.log('window.h5pInstance:', h5pInstance);
        
        // Zkusit získat instanci z kontejneru
        if (!h5pInstance) {
            const container = document.getElementById('h5p-container');
            if (container && container.h5pInstance) {
                h5pInstance = container.h5pInstance;
                console.log('H5P instance nalezena v kontejneru:', h5pInstance);
            }
        }
        
        // Zkusit získat instanci z H5P objektu
        if (!h5pInstance && window.H5P && window.H5P.instances && window.H5P.instances.length > 0) {
            h5pInstance = window.H5P.instances[0];
            console.log('H5P instance nalezena v H5P.instances:', h5pInstance);
        }
        
        if (h5pInstance) {
            console.log('h5pInstance existuje, metody:', Object.keys(h5pInstance));
            if (h5pInstance.contentInstance) {
                const content = h5pInstance.contentInstance;
                console.log('contentInstance existuje, metody:', Object.keys(content));
                console.log('Zkouším získat z contentInstance při volání...');
            
            // Zkusit getScore
            if (content.getScore && typeof content.getScore === 'function') {
                try {
                    const score = content.getScore();
                    const maxScore = content.getMaxScore ? content.getMaxScore() : 100;
                    if (score !== null && score !== undefined) {
                        console.log('H5P výsledky získány z getScore() při volání:', score, maxScore);
                        return {
                            score: score,
                            max_score: maxScore
                        };
                    }
                } catch (e) {
                    console.log('getScore() vyhodila chybu:', e);
                }
            }
            
            // Zkusit getXAPIData
            if (content.getXAPIData && typeof content.getXAPIData === 'function') {
                try {
                    const xapiData = content.getXAPIData();
                    console.log('getXAPIData() výsledek:', xapiData);
                    if (xapiData && xapiData.statement && xapiData.statement.result && xapiData.statement.result.score) {
                        const scoreData = xapiData.statement.result.score;
                        const rawScore = scoreData.raw;
                        const maxScore = scoreData.max || 100;
                        if (rawScore !== null && rawScore !== undefined) {
                            console.log('H5P výsledky získány z getXAPIData() při volání:', rawScore, maxScore);
                            return {
                                score: rawScore,
                                max_score: maxScore
                            };
                        }
                    }
                } catch (e) {
                    console.log('getXAPIData() vyhodila chybu:', e);
                }
            }
            }
        }
        
        // 2. Zkusit získat z H5P instance API (pokud ještě nemáme výsledky)
        if (h5pInstance) {
            console.log('Zkouším získat z h5pInstance přímo...');
            // Zkusit různé způsoby získání výsledků
            console.log('h5pInstance.getScore:', typeof h5pInstance.getScore);
            if (typeof h5pInstance.getScore === 'function') {
                const score = h5pInstance.getScore();
                const maxScore = h5pInstance.getMaxScore ? h5pInstance.getMaxScore() : 100;
                if (score !== null && score !== undefined) {
                    console.log('H5P výsledky získány z instance.getScore():', score, maxScore);
                    return {
                        score: score,
                        max_score: maxScore
                    };
                }
            }
            
            // Zkusit získat z H5P content instance
            if (h5pInstance.contentInstance) {
                const content = h5pInstance.contentInstance;
                if (content.getScore && typeof content.getScore === 'function') {
                    const score = content.getScore();
                    const maxScore = content.getMaxScore ? content.getMaxScore() : 100;
                    if (score !== null && score !== undefined) {
                        console.log('H5P výsledky získány z contentInstance.getScore():', score, maxScore);
                        return {
                            score: score,
                            max_score: maxScore
                        };
                    }
                }
            }
        }
        
        // 3. Zkusit najít text v celém dokumentu (nejspolehlivější pro Single Choice Set)
        const bodyText = document.body.innerText || document.body.textContent || '';
        console.log('Prohledávám body text, délka:', bodyText.length);
        
        const bodyResults = extractScoreFromText(bodyText);
        if (bodyResults) {
            console.log('H5P výsledky získány z body textu:', bodyResults);
            return bodyResults;
        }
        
        // 4. Zkusit najít v H5P kontejneru
        const h5pContainer = document.getElementById('h5p-container') || document.querySelector('.h5p-container');
        if (h5pContainer) {
            const containerText = h5pContainer.innerText || h5pContainer.textContent || '';
            console.log('Prohledávám H5P kontejner, délka:', containerText.length);
            
            const containerResults = extractScoreFromText(containerText);
            if (containerResults) {
                console.log('H5P výsledky získány z kontejneru:', containerResults);
                return containerResults;
            }
        }
        
        // 5. Zkusit najít všechny elementy s textem obsahujícím "correct" nebo "of"
        const allElements = document.querySelectorAll('*');
        console.log('Prohledávám', allElements.length, 'elementů...');
        
        for (let elem of allElements) {
            const text = elem.textContent || elem.innerText || '';
            // Hledat text obsahující "correct" nebo "of" nebo čísla s lomítkem
            if (text && (text.toLowerCase().includes('correct') || text.toLowerCase().includes('of') || /\d+\s*\/\s*\d+/.test(text))) {
                const elemResults = extractScoreFromText(text);
                if (elemResults) {
                    console.log('H5P výsledky získány z elementu:', elemResults, 'text:', text.substring(0, 100));
                    return elemResults;
                }
            }
        }
        
        // 6. Zkusit najít text přímo v celém dokumentu pomocí innerHTML (zachytí i skrytý text)
        const allHTML = document.documentElement.innerHTML || '';
        const htmlResults = extractScoreFromText(allHTML);
        if (htmlResults) {
            console.log('H5P výsledky získány z innerHTML:', htmlResults);
            return htmlResults;
        }
        
        // 7. Zkusit najít v iframe (pokud H5P běží v iframe)
        const iframes = document.querySelectorAll('iframe');
        console.log('Prohledávám', iframes.length, 'iframe...');
        for (let iframe of iframes) {
            try {
                // Zkusit získat text z iframe (může selhat kvůli CORS)
                const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
                if (iframeDoc) {
                    const iframeText = iframeDoc.body?.innerText || iframeDoc.body?.textContent || '';
                    const iframeResults = extractScoreFromText(iframeText);
                    if (iframeResults) {
                        console.log('H5P výsledky získány z iframe:', iframeResults);
                        return iframeResults;
                    }
                }
            } catch (e) {
                // CORS nebo jiná chyba - zkusit postMessage
                console.log('Nelze přistupovat k iframe přímo, zkouším postMessage:', e.message);
                try {
                    // Zkusit poslat zprávu do iframe a počkat na odpověď
                    if (iframe.contentWindow) {
                        // Požádat iframe o výsledky
                        iframe.contentWindow.postMessage({action: 'getScore', action: 'getResults'}, '*');
                        console.log('Poslán postMessage do iframe pro získání výsledků');
                    }
                } catch (e2) {
                    console.log('Nelze použít postMessage:', e2.message);
                }
            }
        }
        
        // Naslouchat na odpovědi z iframe
        if (!window.h5pMessageListener) {
            window.h5pMessageListener = function(event) {
                console.log('PostMessage přijato:', event.data, 'origin:', event.origin);
                // Zkontrolovat, jestli je to odpověď na naši žádost
                if (event.data && (event.data.score !== undefined || event.data.results)) {
                    const score = event.data.score || event.data.results?.score;
                    const maxScore = event.data.maxScore || event.data.results?.maxScore || 100;
                    if (score !== null && score !== undefined) {
                        window.h5pLastResults = {
                            score: score,
                            max_score: maxScore
                        };
                        console.log('H5P výsledky získány z postMessage:', window.h5pLastResults);
                    }
                }
                // Také zkusit získat text z event.data, pokud obsahuje text
                if (event.data && typeof event.data === 'string') {
                    const textResults = extractScoreFromText(event.data);
                    if (textResults) {
                        window.h5pLastResults = textResults;
                        console.log('H5P výsledky získány z postMessage textu:', textResults);
                    }
                }
            };
            window.addEventListener('message', window.h5pMessageListener);
            console.log('Naslouchám na postMessage odpovědi z iframe');
        }
        
        // Také zkusit poslat zprávu do iframe s žádostí o text
        for (let iframe of iframes) {
            try {
                if (iframe.contentWindow) {
                    iframe.contentWindow.postMessage({action: 'getText', action: 'getContent'}, '*');
                    console.log('Poslán postMessage do iframe pro získání textu');
                }
            } catch (e) {
                console.log('Nelze poslat postMessage:', e);
            }
        }
        
        // 8. Zkusit najít pomocí různých selektorů, které H5P používá
        const possibleSelectors = [
            '.h5p-results',
            '.h5p-score',
            '.h5p-feedback',
            '[class*="result"]',
            '[class*="score"]',
            '[class*="feedback"]',
            '.h5p-content',
            '#h5p-container *'
        ];
        
        for (let selector of possibleSelectors) {
            try {
                const elements = document.querySelectorAll(selector);
                for (let elem of elements) {
                    const text = elem.textContent || elem.innerText || '';
                    const results = extractScoreFromText(text);
                    if (results) {
                        console.log('H5P výsledky získány z selektoru', selector, ':', results);
                        return results;
                    }
                }
            } catch (e) {
                // Ignorovat chyby
            }
        }
        
        // 9. Zkusit získat z viditelného textu na stránce pomocí Range API
        const selection = window.getSelection();
        if (selection && selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const rangeText = range.toString();
            const rangeResults = extractScoreFromText(rangeText);
            if (rangeResults) {
                console.log('H5P výsledky získány z selection:', rangeResults);
                return rangeResults;
            }
        }
        
        // 10. Zkusit najít všechny viditelné elementy a zkontrolovat jejich text
        const visibleElements = Array.from(document.querySelectorAll('*')).filter(el => {
            const style = window.getComputedStyle(el);
            return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        });
        
        console.log('Prohledávám', visibleElements.length, 'viditelných elementů...');
        for (let elem of visibleElements) {
            const text = elem.textContent || elem.innerText || '';
            // Hledat text, který obsahuje "correct", "of", nebo čísla s lomítkem
            if (text && text.length < 200 && (text.toLowerCase().includes('correct') || text.toLowerCase().includes('of') || /\d+\s*\/\s*\d+/.test(text))) {
                console.log('Kontroluji element s textem:', text.substring(0, 100));
                const elemResults = extractScoreFromText(text);
                if (elemResults) {
                    console.log('H5P výsledky získány z viditelného elementu:', elemResults, 'text:', text);
                    return elemResults;
                }
            }
        }
        
        // 11. Zkusit najít text pomocí getSelection() - možná je text vybrán
        try {
            const selection = window.getSelection();
            if (selection && selection.toString().length > 0) {
                const selectedText = selection.toString();
                console.log('Zkouším získat z výběru:', selectedText);
                const selectionResults = extractScoreFromText(selectedText);
                if (selectionResults) {
                    console.log('H5P výsledky získány z výběru:', selectionResults);
                    return selectionResults;
                }
            }
        } catch (e) {
            console.log('getSelection selhalo:', e);
        }
        
        // 12. Zkusit najít všechny elementy, které obsahují čísla a klíčová slova
        const allElementsWithNumbers = Array.from(document.querySelectorAll('*')).filter(el => {
            const text = el.textContent || el.innerText || '';
            return text && /\d+/.test(text) && (text.toLowerCase().includes('correct') || text.toLowerCase().includes('of') || text.toLowerCase().includes('score'));
        });
        
        console.log('Našel jsem', allElementsWithNumbers.length, 'elementů s čísly a klíčovými slovy');
        for (let elem of allElementsWithNumbers) {
            const text = elem.textContent || elem.innerText || '';
            console.log('Kontroluji element:', text.substring(0, 150));
            const elemResults = extractScoreFromText(text);
            if (elemResults) {
                console.log('H5P výsledky získány z elementu s čísly:', elemResults, 'text:', text);
                return elemResults;
            }
        }
        
        // 13. Zkusit použít uložené výsledky z MutationObserver (pokud byly zachyceny)
        if (window.h5pLastResults) {
            console.log('Používám uložené výsledky z MutationObserver:', window.h5pLastResults);
            return window.h5pLastResults;
        }
        
        // 14. Zkusit najít text pomocí getAllTextNodes - získat všechny textové uzly
        function getAllTextNodes(node) {
            let textNodes = [];
            if (node.nodeType === 3) { // Text node
                textNodes.push(node);
            } else {
                for (let child of node.childNodes) {
                    textNodes = textNodes.concat(getAllTextNodes(child));
                }
            }
            return textNodes;
        }
        
        const allTextNodes = getAllTextNodes(document.body);
        console.log('Našel jsem', allTextNodes.length, 'textových uzlů');
        for (let textNode of allTextNodes) {
            const text = textNode.textContent || '';
            // Hledat text, který obsahuje "correct", "of", nebo čísla s lomítkem
            if (text && (text.toLowerCase().includes('correct') || text.toLowerCase().includes('of') || /\d+\s*\/\s*\d+/.test(text))) {
                console.log('Kontroluji textový uzel:', text.substring(0, 100));
                const nodeResults = extractScoreFromText(text);
                if (nodeResults) {
                    console.log('H5P výsledky získány z textového uzlu:', nodeResults, 'text:', text);
                    return nodeResults;
                }
            }
        }
        
        // 15. Zkusit najít text v parent elementech textových uzlů (možná je text rozdělený)
        for (let textNode of allTextNodes) {
            if (textNode.parentElement) {
                const parentText = textNode.parentElement.textContent || textNode.parentElement.innerText || '';
                if (parentText && parentText.length < 200 && (parentText.toLowerCase().includes('correct') || parentText.toLowerCase().includes('of'))) {
                    console.log('Kontroluji parent element textového uzlu:', parentText.substring(0, 100));
                    const parentResults = extractScoreFromText(parentText);
                    if (parentResults) {
                        console.log('H5P výsledky získány z parent elementu:', parentResults, 'text:', parentText);
                        return parentResults;
                    }
                }
            }
        }
        
        console.log('Nelze získat výsledky z H5P, použijeme null');
        console.log('Debug: body text obsahuje:', (document.body.innerText || '').substring(0, 500));
        console.log('Debug: window.h5pInstance:', window.h5pInstance);
        console.log('Debug: window.h5pLastResults:', window.h5pLastResults);
        return null;
    } catch (e) {
        console.error('Chyba při získávání výsledků:', e);
        return null;
    }
}

// Globální funkce pro odeslání výsledků
function submitQuizResults(quizId, attemptId) {
    console.log('submitQuizResults volána', quizId, attemptId);
    
    const submitBtn = document.getElementById('submit-quiz-btn');
    const statusDiv = document.getElementById('submit-status');
    
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Odesílám...';
    }
    
    // Nejdřív zkusit získat z viditelného textu na stránce (nejjednodušší způsob)
    // Text "You got 1 of 5 correct" je viditelný, takže ho můžeme najít pomocí různých metod
    let visibleText = '';
    
    // Zkusit různé způsoby získání textu
    const textSources = [];
    
    // 1. Range API
    try {
        const range = document.createRange();
        range.selectNodeContents(document.body);
        const rangeText = range.toString();
        textSources.push({name: 'Range API', text: rangeText});
        console.log('Viditelný text získán pomocí Range API, délka:', rangeText.length);
    } catch (e) {
        console.log('Range API selhalo:', e);
    }
    
    // 2. innerText
    try {
        const innerText = document.body.innerText || '';
        textSources.push({name: 'innerText', text: innerText});
        console.log('Text získán pomocí innerText, délka:', innerText.length);
    } catch (e) {
        console.log('innerText selhalo:', e);
    }
    
    // 3. textContent
    try {
        const textContent = document.body.textContent || '';
        textSources.push({name: 'textContent', text: textContent});
        console.log('Text získán pomocí textContent, délka:', textContent.length);
    } catch (e) {
        console.log('textContent selhalo:', e);
    }
    
    // 4. innerHTML (zachytí i skrytý text)
    try {
        const innerHTML = document.body.innerHTML || '';
        textSources.push({name: 'innerHTML', text: innerHTML});
        console.log('Text získán pomocí innerHTML, délka:', innerHTML.length);
    } catch (e) {
        console.log('innerHTML selhalo:', e);
    }
    
    // 5. Zkusit získat text z H5P kontejneru přímo
    const h5pContainer = document.getElementById('h5p-container') || document.querySelector('.h5p-container');
    if (h5pContainer) {
        try {
            const containerText = h5pContainer.innerText || h5pContainer.textContent || h5pContainer.innerHTML || '';
            if (containerText.length > 0) {
                textSources.push({name: 'H5P container', text: containerText});
                console.log('Text získán z H5P kontejneru, délka:', containerText.length);
            }
        } catch (e) {
            console.log('Získání textu z H5P kontejneru selhalo:', e);
        }
    }
    
    // Prohledat všechny zdroje textu
    for (let source of textSources) {
        console.log('Hledám skóre v', source.name, ', prvních 500 znaků:', source.text.substring(0, 500));
        const results = extractScoreFromText(source.text);
        if (results) {
            console.log('H5P výsledky získány z', source.name, ':', results);
            // Pokračovat s odesláním
            const payload = {
                quiz_id: quizId,
                attempt_id: attemptId,
                score: results.score,
                max_score: results.max_score,
                completed: true
            };
            
            console.log('Odesílám payload:', payload);
            
            fetch('/api/h5p/results/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify(payload)
            }).then(function(response) {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error('HTTP error! status: ' + response.status);
                }
                return response.json();
            }).then(function(data) {
                console.log('Response data:', data);
                if (data.success) {
                    if (statusDiv) {
                        statusDiv.innerHTML = '<div class="alert alert-success">Výsledky byly úspěšně uloženy! Skóre: ' + (data.score !== null && data.score !== undefined ? data.score + '%' : 'N/A') + '</div>';
                    }
                    // Zůstat na stránce - nepřesměrovávat
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Výsledky odeslány';
                    }
                } else {
                    if (statusDiv) {
                        statusDiv.innerHTML = '<div class="alert alert-danger">Chyba: ' + (data.error || 'Nepodařilo se uložit výsledky') + '</div>';
                    }
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Odeslat výsledky testu';
                    }
                }
            }).catch(function(error) {
                console.error('Chyba při odesílání výsledků:', error);
                if (statusDiv) {
                    statusDiv.innerHTML = '<div class="alert alert-danger">Chyba při odesílání výsledků: ' + error.message + '. Zkuste to znovu.</div>';
                }
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Odeslat výsledky testu';
                }
            });
            return; // Ukončit funkci, protože jsme našli výsledky
        }
    }
    
    // Pokud jsme nenašli výsledky v žádném ze zdrojů, zkusit fallback metody
    console.log('Nenašli jsme výsledky v žádném ze zdrojů textu, zkouším fallback metody...');
    
    // Získat výsledky z H5P (fallback)
    const results = getH5PResults();
    console.log('Získané výsledky:', results);
    
    // Pokud nemůžeme získat výsledky z H5P API, zkusit použít ručně zadané skóre
    let scoreValue = null;
    let maxScoreValue = 100;
    
    if (results) {
        scoreValue = results.score;
        maxScoreValue = results.max_score || 100;
        console.log('Používám výsledky z H5P:', scoreValue, maxScoreValue);
    } else {
        // Zkusit získat ručně zadané skóre
        const manualScoreInput = document.getElementById('manual-score');
        if (manualScoreInput && manualScoreInput.value) {
            const manualScore = parseInt(manualScoreInput.value);
            if (!isNaN(manualScore) && manualScore >= 0 && manualScore <= 100) {
                scoreValue = manualScore;
                maxScoreValue = 100;
                console.log('Používám ručně zadané skóre:', scoreValue);
            } else {
                console.warn('Ručně zadané skóre není platné:', manualScoreInput.value);
            }
        }
        
        if (!scoreValue) {
            console.warn('Nepodařilo se získat výsledky z H5P a není zadané ruční skóre, odesílám bez skóre');
        }
    }
    
    const payload = {
        quiz_id: quizId,
        attempt_id: attemptId,
        score: scoreValue,
        max_score: maxScoreValue,
        completed: true
    };
    
    console.log('Odesílám payload:', payload);
    
    // Odeslat na API
    fetch('/api/h5p/results/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'include',
        body: JSON.stringify(payload)
    }).then(function(response) {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error('HTTP error! status: ' + response.status);
        }
        return response.json();
    }).then(function(data) {
        console.log('Response data:', data);
        if (data.success) {
            if (statusDiv) {
                const scoreText = data.score !== null && data.score !== undefined ? data.score + '%' : 'N/A (skóre se nepodařilo automaticky získat - zadej ho ručně příště)';
                const quizDetailUrl = '/quiz/' + quizId + '/';
                const message = data.score !== null && data.score !== undefined 
                    ? '<strong>Výsledky byly úspěšně uloženy!</strong><br>Skóre: ' + scoreText
                    : '<strong>Výsledky byly úspěšně uloženy!</strong><br>Skóre: ' + scoreText + '<br><small class="text-muted">V tabulce se zobrazí jako "V řešení". Pokud chceš zadat skóre, použij pole výše a odešli znovu.</small>';
                statusDiv.innerHTML = '<div class="alert alert-success">' +
                    message + '<br>' +
                    '<a href="' + quizDetailUrl + '" class="btn btn-sm btn-primary mt-2">Zobrazit výsledky v tabulce</a>' +
                    '</div>';
            }
            // Zůstat na stránce - nepřesměrovávat
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Výsledky odeslány';
            }
        } else {
            if (statusDiv) {
                statusDiv.innerHTML = '<div class="alert alert-danger">Chyba: ' + (data.error || 'Nepodařilo se uložit výsledky') + '</div>';
            }
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Odeslat výsledky testu';
            }
        }
    }).catch(function(error) {
        console.error('Chyba při odesílání výsledků:', error);
        if (statusDiv) {
            statusDiv.innerHTML = '<div class="alert alert-danger">Chyba při odesílání výsledků: ' + error.message + '. Zkuste to znovu.</div>';
        }
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Odeslat výsledky testu';
        }
    });
}

