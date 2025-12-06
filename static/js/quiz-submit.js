/**
 * JavaScript pro odeslání výsledků H5P testu
 */

// Globální proměnná pro uložení výsledků z xAPI
window.h5pLastResults = null;

// Funkce pro extrakci skóre z textu
function extractScoreFromText(text) {
    if (!text) return null;
    
    console.log('extractScoreFromText volána, délka textu:', text.length);
    console.log('Hledám skóre v textu (prvních 500 znaků):', text.substring(0, 500));
    
    // Různé patterny pro různé formáty - UPŘEDNOSTNIT PŘESNĚJŠÍ PATTERNY
    // Důležité: zkusit nejdřív nejpřesnější patterny, které obsahují "correct" nebo "got"
    const patterns = [
        // Nejpřesnější patterny - obsahují "got" a "correct"
        /you\s+got\s+(\d+)\s+of\s+(\d+)\s+correct/i,      // "You got 1 of 5 correct" (case insensitive)
        /got\s+(\d+)\s+of\s+(\d+)\s+correct/i,            // "got 1 of 5 correct"
        /(\d+)\s+of\s+(\d+)\s+correct/i,                   // "1 of 5 correct"
        /(\d+)\s+correct\s+out\s+of\s+(\d+)/i,            // "1 correct out of 5"
        // Patterny s "of" (méně přesné, ale stále dobré)
        /(\d+)\s+of\s+(\d+)/i,                            // "1 of 5"
        /(\d+)\s+out\s+of\s+(\d+)/i,                      // "1 out of 5"
        // Patterny s lomítkem
        /(\d+)\s*\/\s*(\d+)/,                             // "1/5" nebo "3/5"
        /score[:\s]+(\d+)\s*\/\s*(\d+)/i,                // "Score: 1/5"
        // České varianty
        /(\d+)\s+z\s+(\d+)/i,                             // "1 z 5" (česky)
        /(\d+)\s+ze\s+(\d+)/i,                            // "1 ze 5" (česky)
    ];
    
    // Zkusit najít všechny shody a vybrat tu nejlepší
    let bestMatch = null;
    let bestPatternIndex = -1;
    
    for (let i = 0; i < patterns.length; i++) {
        const pattern = patterns[i];
        const match = text.match(pattern);
        if (match) {
            const score = parseInt(match[1]);
            const maxScore = parseInt(match[2]);
            console.log('Pattern', i, 'match:', match[0], 'score:', score, 'maxScore:', maxScore);
            
            // Validace: score musí být >= 0, maxScore > 0, score <= maxScore
            // A maxScore by mělo být rozumné (např. 1-100)
            if (!isNaN(score) && !isNaN(maxScore) && 
                score >= 0 && maxScore > 0 && score <= maxScore && 
                maxScore <= 100) {
                
                // Upřednostnit patterny s "correct" nebo "got" (první 4 patterny)
                if (i < 4 && (!bestMatch || bestPatternIndex >= 4)) {
                    bestMatch = {score: score, max_score: maxScore};
                    bestPatternIndex = i;
                    console.log('extractScoreFromText našel lepší match (pattern', i, '):', score, '/', maxScore);
                } else if (!bestMatch) {
                    bestMatch = {score: score, max_score: maxScore};
                    bestPatternIndex = i;
                    console.log('extractScoreFromText našel match (pattern', i, '):', score, '/', maxScore);
                }
            }
        }
    }
    
    if (bestMatch) {
        console.log('extractScoreFromText FINÁLNÍ výsledek:', bestMatch, 'pattern:', bestPatternIndex);
        return bestMatch;
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
    // DŮLEŽITÉ: Ignorovat procentuální hodnoty (např. "100%", "20%") - ty nejsou raw score
    const allNumbers = text.match(/\d+/g);
    if (allNumbers && allNumbers.length >= 2) {
        console.log('Všechna čísla v textu:', allNumbers);
        // Zkusit najít dvojice čísel, která by mohla být skóre
        // Ale jen pokud jsou blízko sebe a obsahují klíčová slova
        // A IGNOROVAT pokud je druhé číslo > 100 (pravděpodobně procenta)
        for (let i = 0; i < allNumbers.length - 1; i++) {
            const num1 = parseInt(allNumbers[i]);
            const num2 = parseInt(allNumbers[i + 1]);
            
            // Ignorovat pokud num2 > 100 (pravděpodobně procenta, ne max score)
            if (num2 > 100) {
                console.log('Ignoruji dvojici čísel (num2 > 100, pravděpodobně procenta):', num1, num2);
                continue;
            }
            
            if (!isNaN(num1) && !isNaN(num2) && num1 >= 0 && num2 > 0 && num1 <= num2 && num2 <= 100) {
                // Zkontrolovat, jestli jsou tato čísla blízko sebe v textu
                const index1 = text.indexOf(allNumbers[i]);
                const index2 = text.indexOf(allNumbers[i + 1], index1);
                if (index2 !== -1 && index2 - index1 < 30) {
                    // Zkontrolovat, jestli mezi nimi jsou klíčová slova (of, /, correct, atd.)
                    const textBetween = text.substring(index1, index2 + allNumbers[i + 1].length).toLowerCase();
                    const hasKeywords = /of|correct|score|z|ze|\//.test(textBetween);
                    
                    // IGNOROVAT pokud obsahuje "%" (procenta)
                    if (textBetween.includes('%')) {
                        console.log('Ignoruji dvojici čísel (obsahuje %):', textBetween);
                        continue;
                    }
                    
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
        const h5pContainerElement = document.getElementById('h5p-container') || document.querySelector('.h5p-container');
        if (h5pContainerElement) {
            // Zkusit různé způsoby získání textu
            const texts = [
                h5pContainerElement.innerText || '',
                h5pContainerElement.textContent || '',
                h5pContainerElement.innerHTML || ''
            ];
            
            for (let text of texts) {
                if (text && text.length > 0) {
                    const results = extractScoreFromText(text);
                    // Použít jen finální skóre (max_score > 1), ignorovat mezilehlé
                    if (results && results.max_score > 1) {
                        window.h5pLastResults = results;
                        console.log('H5P výsledky získány z MutationObserver (finální):', results);
                        // Můžeme zastavit observer, protože jsme našli finální výsledky
                        if (scoreObserver) {
                            scoreObserver.disconnect();
                            scoreObserver = null;
                        }
                        return;
                    }
                }
            }
            
            // Také zkusit prohledat všechny potomky
            const allText = h5pContainerElement.innerText || h5pContainerElement.textContent || '';
            if (allText && allText.length > 0) {
                const results = extractScoreFromText(allText);
                // Použít jen finální skóre (max_score > 1)
                if (results && results.max_score > 1) {
                    window.h5pLastResults = results;
                    console.log('H5P výsledky získány z MutationObserver (všechny potomky, finální):', results);
                    if (scoreObserver) {
                        scoreObserver.disconnect();
                        scoreObserver = null;
                    }
                    return;
                }
            }
            
            // Zkusit najít iframe a poslat mu zprávu
            const iframes = h5pContainerElement.querySelectorAll('iframe');
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
        // DŮLEŽITÉ: Použít jen pokud max_score > 1 (finální skóre), ne mezilehlé (max: 1)
        if (window.h5pLastResults && window.h5pLastResults.max_score > 1) {
            console.log('H5P výsledky získány z cache (xAPI/interval, finální):', window.h5pLastResults);
            return window.h5pLastResults;
        } else if (window.h5pLastResults && window.h5pLastResults.max_score <= 1) {
            console.log('Ignoruji mezilehlé výsledky z cache (max_score <= 1):', window.h5pLastResults);
            // Pokračovat s dalšími metodami
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
                    console.log('getScore() raw hodnoty:', {score, maxScore, scoreType: typeof score});
                    
                    // Zkontrolovat, jestli score není už procentuální hodnota (0-1) nebo procenta (0-100)
                    let finalScore = score;
                    let finalMaxScore = maxScore;
                    
                    // Pokud je score mezi 0 a 1, je to pravděpodobně procentuální hodnota (0.2 pro 20%)
                    if (score >= 0 && score <= 1 && maxScore === 1) {
                        // Je to procentuální hodnota, přepočítat na raw score
                        // Musíme zjistit skutečný maxScore z jiného zdroje
                        console.log('Score vypadá jako procentuální hodnota (0-1), zkusím získat skutečný maxScore');
                        // Zkusit získat z getXAPIData nebo z textu
                    } else if (score > 1 && score <= 100 && maxScore === 100) {
                        // Možná je to už procenta (0-100), ale potřebujeme raw score
                        console.log('Score vypadá jako procenta (0-100), zkusím získat raw score z jiného zdroje');
                    }
                    
                    if (score !== null && score !== undefined) {
                        console.log('H5P výsledky získány z getScore() při volání:', finalScore, finalMaxScore);
                        return {
                            score: finalScore,
                            max_score: finalMaxScore
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
        
        // 3. Zkusit najít text v H5P kontejneru (prioritně)
        const h5pContainerForText = document.getElementById('h5p-container') || document.querySelector('.h5p-container');
        if (h5pContainerForText) {
            // Zkusit získat jen viditelný text z H5P kontejneru
            const containerText = h5pContainerForText.innerText || h5pContainerForText.textContent || '';
            console.log('Prohledávám H5P kontejner text, délka:', containerText.length);
            console.log('H5P kontejner text (prvních 500 znaků):', containerText.substring(0, 500));
            
            const containerResults = extractScoreFromText(containerText);
            if (containerResults) {
                console.log('H5P výsledky získány z H5P kontejneru:', containerResults);
                return containerResults;
            }
        }
        
        // 4. Zkusit najít text v celém dokumentu (fallback)
        const bodyText = document.body.innerText || document.body.textContent || '';
        console.log('Prohledávám body text, délka:', bodyText.length);
        
        const bodyResults = extractScoreFromText(bodyText);
        if (bodyResults) {
            console.log('H5P výsledky získány z body textu:', bodyResults);
            return bodyResults;
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
    const h5pContainerForSubmit = document.getElementById('h5p-container') || document.querySelector('.h5p-container');
    if (h5pContainerForSubmit) {
        try {
            const containerText = h5pContainerForSubmit.innerText || h5pContainerForSubmit.textContent || h5pContainerForSubmit.innerHTML || '';
            if (containerText.length > 0) {
                textSources.push({name: 'H5P container', text: containerText});
                console.log('Text získán z H5P kontejneru, délka:', containerText.length);
            }
        } catch (e) {
            console.log('Získání textu z H5P kontejneru selhalo:', e);
        }
    }
    
    // Prohledat všechny zdroje textu - UPŘEDNOSTNIT H5P kontejner
    // Seřadit zdroje podle priority (H5P kontejner má nejvyšší prioritu)
    const priorityOrder = ['H5P container', 'innerText', 'textContent', 'Range API', 'innerHTML'];
    textSources.sort((a, b) => {
        const aIndex = priorityOrder.indexOf(a.name);
        const bIndex = priorityOrder.indexOf(b.name);
        if (aIndex === -1 && bIndex === -1) return 0;
        if (aIndex === -1) return 1;
        if (bIndex === -1) return -1;
        return aIndex - bIndex;
    });
    
    for (let source of textSources) {
        console.log('Hledám skóre v', source.name, ', prvních 500 znaků:', source.text.substring(0, 500));
        const results = extractScoreFromText(source.text);
        if (results) {
            console.log('H5P výsledky získány z', source.name, ':', results);
            const calculatedPercent = (results.score / results.max_score * 100).toFixed(2);
            console.log('Výpočet procent:', results.score, '/', results.max_score, '=', calculatedPercent + '%');
            
            // Ověřit, že skóre dává smysl
            if (results.score < 0 || results.score > results.max_score) {
                console.warn('Varování: Skóre neodpovídá max_score!', results);
                // Pokračovat s dalším zdrojem
                continue;
            }
            
            // Validace: max_score by mělo být rozumné (1-100)
            if (results.max_score < 1 || results.max_score > 100) {
                console.warn('Varování: max_score není v rozumném rozsahu!', results);
                // Pokračovat s dalším zdrojem
                continue;
            }
            
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
    // DŮLEŽITÉ: Prioritně použít finální skóre z xAPI (max_score > 1)
    const results = getH5PResults();
    console.log('Získané výsledky:', results);
    
    // Pokud nemůžeme získat výsledky z H5P API, zkusit použít ručně zadané skóre
    let scoreValue = null;
    let maxScoreValue = 100;
    
    if (results) {
        // Validace: Ignorovat mezilehlé výsledky (max_score <= 1)
        if (results.max_score <= 1) {
            console.warn('Ignoruji mezilehlé výsledky (max_score <= 1):', results);
            // Pokračovat s dalšími metodami
        } else {
            scoreValue = results.score;
            maxScoreValue = results.max_score || 100;
            console.log('Používám výsledky z H5P (finální):', {score: scoreValue, max_score: maxScoreValue, scoreType: typeof scoreValue});
            
            // Validace: zkontrolovat, že skóre dává smysl
            if (scoreValue < 0 || scoreValue > maxScoreValue) {
                console.error('VAROVÁNÍ: Skóre neodpovídá max_score!', {score: scoreValue, max_score: maxScoreValue});
                scoreValue = null; // Resetovat, zkusit další metody
            } else {
                // Výpočet procent pro kontrolu
                const calculatedPercent = maxScoreValue > 0 ? ((scoreValue / maxScoreValue) * 100).toFixed(2) : 'N/A';
                console.log('Výpočet procent:', scoreValue, '/', maxScoreValue, '=', calculatedPercent + '%');
            }
        }
    }
    
    if (!scoreValue) {
        // Pokud nemáme finální skóre, zkusit další metody
        console.log('Nemám finální skóre, zkouším další metody...');
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

