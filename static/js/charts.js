/**
 * GitHub Analytics Pro - Modern Charting Engine (Chart.js 4.x)
 */

const AppCharts = {
    instances: {},

    getThemeColors() {
        const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
        return {
            isDark,
            text: isDark ? '#f8fafc' : '#0f172a',
            textSecondary: isDark ? '#94a3b8' : '#475569',
            grid: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)',
            tooltipBg: isDark ? 'rgba(17, 24, 39, 0.95)' : 'rgba(255, 255, 255, 0.95)',
            tooltipBorder: isDark ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 0, 0, 0.12)',
            cardBg: isDark ? '#111827' : '#ffffff',
            primary: '#38bdf8',
            primaryAlpha: 'rgba(56, 189, 248, 0.18)',
            emerald: '#10b981',
            emeraldAlpha: 'rgba(16, 185, 129, 0.18)',
            purple: '#8b5cf6',
            purpleAlpha: 'rgba(139, 92, 246, 0.18)',
            amber: '#f59e0b'
        };
    },

    languageColors: {
        'JavaScript': '#f1e05a',
        'TypeScript': '#3178c6',
        'Python': '#3572A5',
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'Java': '#b07219',
        'C++': '#f34b7d',
        'C#': '#178600',
        'C': '#555555',
        'Go': '#00ADD8',
        'Rust': '#dea584',
        'PHP': '#4F5D95',
        'Ruby': '#701516',
        'Swift': '#F05138',
        'Kotlin': '#A97BFF',
        'Shell': '#89e051',
        'Dart': '#00B4AB',
        'Vue': '#41b883',
        'Unknown': '#64748b'
    },

    getLanguageColor(lang) {
        return this.languageColors[lang] || `hsl(${Math.abs(this.hashCode(lang)) % 360}, 70%, 55%)`;
    },

    hashCode(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        return hash;
    },

    /**
     * Create or update Contribution Timeline
     */
    createTimeline(canvasId, timelineData) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !timelineData) return null;

        const ctx = canvas.getContext('2d');
        const theme = this.getThemeColors();

        if (this.instances[canvasId]) {
            this.instances[canvasId].destroy();
        }

        // Clean and sort quarters/periods
        const labels = Object.keys(timelineData);
        const values = Object.values(timelineData);

        // Linear gradient fill
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, theme.emeraldAlpha);
        gradient.addColorStop(1, 'rgba(16, 185, 129, 0)');

        this.instances[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Commits',
                    data: values,
                    borderColor: theme.emerald,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.35,
                    borderWidth: 2.5,
                    pointBackgroundColor: theme.cardBg,
                    pointBorderColor: theme.emerald,
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.text,
                        bodyColor: theme.textSecondary,
                        borderColor: theme.tooltipBorder,
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: (context) => ` ${context.parsed.y} commits recorded`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: theme.grid, drawBorder: false },
                        ticks: { color: theme.textSecondary, font: { family: 'Plus Jakarta Sans', size: 11 } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: theme.grid, drawBorder: false },
                        ticks: { color: theme.textSecondary, font: { family: 'JetBrains Mono', size: 11 } }
                    }
                }
            }
        });

        return this.instances[canvasId];
    },

    /**
     * Create Doughnut Language Breakdown
     */
    createLanguageDoughnut(canvasId, languageData) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !languageData || Object.keys(languageData).length === 0) return null;

        const ctx = canvas.getContext('2d');
        const theme = this.getThemeColors();

        if (this.instances[canvasId]) {
            this.instances[canvasId].destroy();
        }

        const labels = Object.keys(languageData);
        const values = Object.values(languageData);
        const backgroundColors = labels.map(l => this.getLanguageColor(l));

        this.instances[canvasId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: backgroundColors,
                    borderColor: theme.cardBg,
                    borderWidth: 2,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '68%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: theme.textSecondary,
                            boxWidth: 12,
                            boxHeight: 12,
                            padding: 10,
                            font: { family: 'Plus Jakarta Sans', size: 11 }
                        }
                    },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.text,
                        bodyColor: theme.textSecondary,
                        borderColor: theme.tooltipBorder,
                        borderWidth: 1,
                        padding: 10
                    }
                }
            }
        });

        return this.instances[canvasId];
    },

    /**
     * Re-render all active charts when theme toggles
     */
    refreshTheme() {
        const dataElement = document.getElementById('github-data');
        if (!dataElement) return;

        try {
            const data = JSON.parse(dataElement.textContent);
            if (!data) return;

            // Update Timeline
            const history = data.stats?.commit_history;
            if (history) {
                this.createTimeline('contributionTimeline', history);
                this.createTimeline('commitsTimeline', history);
            }

            // Update Languages
            if (data.languages) {
                if (data.languages.by_repos) {
                    this.createLanguageDoughnut('languageByRepos', data.languages.by_repos);
                    this.createLanguageDoughnut('reposPerLanguage', data.languages.by_repos);
                }
                if (data.languages.by_stars) {
                    this.createLanguageDoughnut('languageByStars', data.languages.by_stars);
                    this.createLanguageDoughnut('starsPerLanguage', data.languages.by_stars);
                }
                if (data.languages.by_commits) {
                    this.createLanguageDoughnut('languageByCommits', data.languages.by_commits);
                    this.createLanguageDoughnut('commitsPerLanguage', data.languages.by_commits);
                }
            }
        } catch (e) {
            console.warn('Could not refresh chart theme:', e);
        }
    }
};

window.AppCharts = AppCharts;