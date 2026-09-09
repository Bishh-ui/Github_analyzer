/**
 * GitHub Analytics Pro - Enhanced UI Features & Interactions
 */

// Auto-complete for GitHub usernames
class GitHubUserSearch {
    constructor() {
        this.input = document.getElementById('username-input');
        this.suggestionsEl = document.getElementById('suggestions');
        this.debounceTimer = null;
        
        if (this.input && this.suggestionsEl) {
            this.init();
        }
    }
    
    init() {
        this.input.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimer);
            const query = e.target.value.trim();
            
            if (query.length >= 2) {
                this.debounceTimer = setTimeout(() => this.search(query), 280);
            } else {
                this.hideSuggestions();
            }
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#search-form')) {
                this.hideSuggestions();
            }
        });
    }
    
    async search(query) {
        try {
            const response = await fetch(`/api/search/users?q=${encodeURIComponent(query)}`);
            if (!response.ok) return;
            const data = await response.json();
            
            if (data.results && data.results.length > 0) {
                this.showSuggestions(data.results);
            } else {
                this.hideSuggestions();
            }
        } catch (error) {
            this.hideSuggestions();
        }
    }
    
    showSuggestions(users) {
        this.suggestionsEl.innerHTML = users.slice(0, 6).map(user => `
            <div class="suggestion-item" data-username="${user.login}">
                <img src="${user.avatar_url}" alt="${user.login}" class="suggestion-avatar">
                <div class="suggestion-info">
                    <div class="suggestion-name">${user.name || user.login}</div>
                    <div class="suggestion-meta">@${user.login} • ${user.public_repos} repos</div>
                </div>
            </div>
        `).join('');
        
        this.suggestionsEl.classList.add('show');
        
        this.suggestionsEl.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                this.input.value = item.dataset.username;
                this.hideSuggestions();
                const form = document.getElementById('search-form');
                if (form) form.submit();
            });
        });
    }
    
    hideSuggestions() {
        if (this.suggestionsEl) {
            this.suggestionsEl.classList.remove('show');
            this.suggestionsEl.innerHTML = '';
        }
    }
}

// Data Exporter with feedback toasts
class DataExporter {
    static async exportData(username, format) {
        try {
            this.showNotification(`Preparing ${format.toUpperCase()} export...`, 'info');
            const response = await fetch(`/export/${format}/${username}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${username}_analytics.${format === 'markdown' ? 'md' : format}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showNotification(`Successfully exported ${format.toUpperCase()}!`, 'success');
            } else {
                throw new Error('Export request failed');
            }
        } catch (error) {
            this.showNotification('Export failed. Please try again.', 'error');
        }
    }
    
    static showNotification(message, type = 'info') {
        const existing = document.querySelectorAll('.toast-notification');
        existing.forEach(e => e.remove());

        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        const icon = type === 'success' ? 'check-circle text-success' : (type === 'error' ? 'exclamation-circle text-danger' : 'info-circle text-info');
        toast.innerHTML = `<i class="fas fa-${icon}"></i> <span>${message}</span>`;
        document.body.appendChild(toast);
        
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 250);
        }, 3200);
    }
}

// Smooth Number Counter Animation
class StatsAnimator {
    static animateValue(element, start, end, duration) {
        const isDecimal = end.toString().includes('.');
        const decimals = isDecimal ? (end.toString().split('.')[1] || '').length : 0;
        const range = end - start;
        const startTime = performance.now();
        
        function step(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease-out cubic formula
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = start + range * ease;
            element.textContent = isDecimal ? current.toFixed(decimals) : Math.round(current);
            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                element.textContent = isDecimal ? end.toFixed(decimals) : end;
            }
        }
        requestAnimationFrame(step);
    }
    
    static animateAllStats() {
        document.querySelectorAll('.metric-value').forEach(el => {
            const raw = el.textContent.trim();
            const val = parseFloat(raw);
            if (!isNaN(val) && val > 0) {
                el.textContent = '0';
                this.animateValue(el, 0, val, 900);
            }
        });
    }
}

// Real-time API Quota Monitor
class RateLimitMonitor {
    constructor(interval = 45000) {
        this.interval = interval;
        this.timer = null;
    }
    
    start() {
        this.update();
        this.timer = setInterval(() => this.update(), this.interval);
    }
    
    stop() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }
    
    async update() {
        try {
            const response = await fetch('/api/rate-limit');
            if (!response.ok) return;
            const data = await response.json();
            if (data.core) {
                this.updateDisplay(data.core);
            }
        } catch (e) {
            // Quietly ignore network failures in background
        }
    }
    
    updateDisplay(core) {
        // Update Navbar Status
        const navLabel = document.getElementById('nav-quota-label');
        if (navLabel) {
            navLabel.textContent = `API: ${core.remaining}/${core.limit}`;
        }
        
        // Update In-page progress bar if on profile page
        const progressBar = document.querySelector('.api-limits .progress-bar');
        if (progressBar) {
            const pct = Math.round((core.remaining / core.limit) * 100);
            progressBar.style.width = `${pct}%`;
        }
    }
}

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    new GitHubUserSearch();
    
    // Animate stats
    if (document.querySelector('.metric-value')) {
        StatsAnimator.animateAllStats();
    }
    
    // Intercept export clicks
    document.querySelectorAll('a[href^="/export/"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const url = new URL(btn.href);
            const parts = url.pathname.split('/');
            const format = parts[2];
            const username = parts[3];
            DataExporter.exportData(username, format);
        });
    });
    
    // Start Rate Limit heartbeat
    window.rateMonitor = new RateLimitMonitor(45000);
    window.rateMonitor.start();
});
