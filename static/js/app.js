/**
 * Application Entry Point - Data Initialization & Interactions
 */

document.addEventListener('DOMContentLoaded', function () {
    const dataElement = document.getElementById('github-data');
    if (!dataElement) return;

    try {
        const text = dataElement.textContent.trim();
        if (text && text !== 'null' && text !== 'None') {
            const userData = JSON.parse(text);
            if (userData && window.AppCharts) {
                window.AppCharts.refreshTheme();
            }
        }
    } catch (error) {
        console.error('Error parsing user data JSON:', error);
    }
});