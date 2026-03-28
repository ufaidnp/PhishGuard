document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scan-form');
    const input = document.getElementById('url-input');
    const btn = document.getElementById('analyze-btn');
    
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const errorMsg = document.getElementById('error');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = input.value.trim();
        if (!url) return;

        // Reset UI
        errorMsg.classList.add('hidden');
        results.classList.add('hidden');
        loading.classList.remove('hidden');
        btn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred');
            }

            renderResults(data);
        } catch (err) {
            errorMsg.textContent = err.message;
            errorMsg.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
            btn.disabled = false;
        }
    });

    function renderResults(data) {
        const header = document.getElementById('result-header');
        const verdict = document.getElementById('verdict');
        const score = document.getElementById('confidence-score');
        const progress = document.getElementById('progress-fill');
        const details = document.getElementById('details-text');
        
        // Reset classes
        header.className = 'result-header';
        
        const isPhishing = data.result.toLowerCase() === 'phishing';
        const typeClass = isPhishing ? 'phishing' : 'legitimate';
        
        header.classList.add(typeClass);
        verdict.textContent = data.result;
        
        // Animate counter
        let currentScore = 0;
        const targetScore = Math.floor(data.confidence); // Round down for animation target
        
        const duration = 1000; // ms
        const frameRate = 16; // approx 60fps
        const totalFrames = duration / frameRate;
        const increment = targetScore / totalFrames;
        
        const interval = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(interval);
            }
            score.textContent = Math.floor(currentScore);
        }, frameRate);
        
        progress.style.width = `${data.confidence}%`;
        details.textContent = data.details || "Heuristic and algorithmic analysis complete.";

        // Render Features
        const urlFeatures = document.getElementById('url-features-list');
        urlFeatures.innerHTML = '';
        if (data.features) {
            const formatName = (str) => str.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            for (const [key, value] of Object.entries(data.features)) {
                if(key === 'domain_age' && value === -1) continue; // skip unknown age
                
                const li = document.createElement('li');
                li.innerHTML = `<span>${formatName(key)}</span> <span class="feature-value">${value}</span>`;
                urlFeatures.appendChild(li);
            }
        }

        // Render Content Heuristics
        const contentFeatures = document.getElementById('content-features-list');
        contentFeatures.innerHTML = '';
        if (data.html_analysis) {
            const formatName = (str) => str.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            
            if (data.html_analysis.fetch_error) {
                contentFeatures.innerHTML = '<li><span class="feature-value" style="color:var(--phish)">Could not fetch external content securely. This may indicate blocking mechanisms or a missing domain.</span></li>';
            } else {
                for (const [key, value] of Object.entries(data.html_analysis)) {
                    if (key === 'fetch_error') continue;
                    const li = document.createElement('li');
                    
                    // Format boolean/counts nicely
                    let displayValue = value;
                    if (key === 'has_login_form') displayValue = value ? 'Yes' : 'No';
                    
                    li.innerHTML = `<span>${formatName(key)}</span> <span class="feature-value">${displayValue}</span>`;
                    contentFeatures.appendChild(li);
                }
            }
        }

        results.classList.remove('hidden');
    }
});
