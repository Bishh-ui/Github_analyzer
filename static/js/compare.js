// Comparison Charts for GitHub Analytics

document.addEventListener('DOMContentLoaded', function() {
    const dataElement = document.getElementById('comparison-data');
    if (!dataElement) return;

    try {
        const comparisons = JSON.parse(dataElement.textContent);
        initializeComparisonCharts(comparisons);
    } catch (error) {
        console.error('Error parsing comparison data:', error);
    }
});

function initializeComparisonCharts(comparisons) {
    // Extract data for charts
    const usernames = comparisons.map(c => c.username);
    const colors = generateColors(usernames.length);

    // Repository Comparison Chart
    createRepoComparisonChart(comparisons, usernames, colors);

    // Social Reach Chart
    createSocialComparisonChart(comparisons, usernames, colors);

    // Advanced Metrics Chart
    createMetricsComparisonChart(comparisons, usernames, colors);

    // Language Diversity Chart
    createLanguageDiversityChart(comparisons, usernames, colors);
}

function generateColors(count) {
    const baseColors = [
        '#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', 
        '#10b981', '#06b6d4', '#3b82f6', '#f97316'
    ];
    return baseColors.slice(0, count);
}

function createRepoComparisonChart(comparisons, usernames, colors) {
    const ctx = document.getElementById('repoComparison');
    if (!ctx) return;

    const datasets = [
        {
            label: 'Public Repos',
            data: comparisons.map(c => c.stats.stats.public_repos),
            backgroundColor: colors[0],
            borderColor: colors[0],
            borderWidth: 2
        },
        {
            label: 'Total Stars',
            data: comparisons.map(c => c.stats.stats.total_stars),
            backgroundColor: colors[1],
            borderColor: colors[1],
            borderWidth: 2
        },
        {
            label: 'Total Forks',
            data: comparisons.map(c => c.stats.stats.total_forks),
            backgroundColor: colors[2],
            borderColor: colors[2],
            borderWidth: 2
        }
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: usernames,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#c9d1d9' }
                },
                tooltip: {
                    backgroundColor: 'rgba(22, 27, 34, 0.95)',
                    titleColor: '#c9d1d9',
                    bodyColor: '#8b949e',
                    borderColor: '#30363d',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(48, 54, 61, 0.5)' },
                    ticks: { color: '#8b949e' }
                },
                x: {
                    grid: { color: 'rgba(48, 54, 61, 0.5)' },
                    ticks: { color: '#8b949e' }
                }
            }
        }
    });
}

function createSocialComparisonChart(comparisons, usernames, colors) {
    const ctx = document.getElementById('socialComparison');
    if (!ctx) return;

    const datasets = [
        {
            label: 'Followers',
            data: comparisons.map(c => c.stats.stats.followers),
            backgroundColor: colors[3],
            borderColor: colors[3],
            borderWidth: 2
        },
        {
            label: 'Following',
            data: comparisons.map(c => c.stats.stats.following),
            backgroundColor: colors[4],
            borderColor: colors[4],
            borderWidth: 2
        }
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: usernames,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#c9d1d9' }
                },
                tooltip: {
                    backgroundColor: 'rgba(22, 27, 34, 0.95)',
                    titleColor: '#c9d1d9',
                    bodyColor: '#8b949e',
                    borderColor: '#30363d',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(48, 54, 61, 0.5)' },
                    ticks: { color: '#8b949e' }
                },
                x: {
                    grid: { color: 'rgba(48, 54, 61, 0.5)' },
                    ticks: { color: '#8b949e' }
                }
            }
        }
    });
}

function createMetricsComparisonChart(comparisons, usernames, colors) {
    const ctx = document.getElementById('metricsComparison');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Impact Score', 'Consistency', 'Diversity'],
            datasets: comparisons.map((comp, index) => ({
                label: comp.username,
                data: [
                    comp.stats.advanced_metrics.impact_score,
                    comp.stats.advanced_metrics.consistency_score,
                    comp.stats.advanced_metrics.diversity_score
                ],
                backgroundColor: hexToRgba(colors[index], 0.2),
                borderColor: colors[index],
                borderWidth: 2,
                pointBackgroundColor: colors[index],
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: colors[index]
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#c9d1d9' }
                },
                tooltip: {
                    backgroundColor: 'rgba(22, 27, 34, 0.95)',
                    titleColor: '#c9d1d9',
                    bodyColor: '#8b949e',
                    borderColor: '#30363d',
                    borderWidth: 1
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: '#8b949e'
                    },
                    grid: {
                        color: 'rgba(48, 54, 61, 0.5)'
                    },
                    pointLabels: {
                        color: '#c9d1d9',
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

function createLanguageDiversityChart(comparisons, usernames, colors) {
    const ctx = document.getElementById('languageComparison');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: usernames,
            datasets: [{
                label: 'Number of Languages',
                data: comparisons.map(c => c.stats.languages.total_languages),
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(22, 27, 34, 0.95)',
                    titleColor: '#c9d1d9',
                    bodyColor: '#8b949e',
                    borderColor: '#30363d',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(48, 54, 61, 0.5)' },
                    ticks: { 
                        color: '#8b949e',
                        stepSize: 1
                    }
                },
                x: {
                    grid: { color: 'rgba(48, 54, 61, 0.5)' },
                    ticks: { color: '#8b949e' }
                }
            }
        }
    });
}

function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}
