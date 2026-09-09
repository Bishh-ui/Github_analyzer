// Theme Management with Chart Synchronization
const Theme = {
    DARK: 'dark',
    LIGHT: 'light',
    
    init() {
        this.loadTheme();
        this.setupToggle();
    },
    
    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || this.DARK;
        this.applyTheme(savedTheme, false);
    },
    
    applyTheme(theme, animate = true) {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        const icon = document.querySelector('#theme-toggle i');
        if (icon) {
            icon.className = theme === this.DARK ? 'fas fa-sun' : 'fas fa-moon';
        }

        // Refresh Chart.js palette if charts are rendered
        if (window.AppCharts && typeof window.AppCharts.refreshTheme === 'function') {
            window.AppCharts.refreshTheme();
        }
    },
    
    toggle() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || this.DARK;
        const newTheme = currentTheme === this.DARK ? this.LIGHT : this.DARK;
        this.applyTheme(newTheme, true);
    },
    
    setupToggle() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    Theme.init();
});
