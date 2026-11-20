/**
 * PG Food Admin - One-Click Professional Theme Management System
 * Single-click direct toggle between Light Mode & Dark Mode with zero-reload updates
 */
(function () {
    'use strict';

    const STORAGE_KEY = 'tabler-theme'; // 'light' | 'dark'

    function getCurrentTheme() {
        const stored = localStorage.getItem(STORAGE_KEY) || localStorage.getItem('tabler-theme-mode');
        if (stored === 'dark' || stored === 'light') {
            return stored;
        }
        // Fallback to system preference
        return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
    }

    function setTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-bs-theme');
        }

        localStorage.setItem(STORAGE_KEY, theme);
        localStorage.setItem('tabler-theme-mode', theme);

        // Update active classes on any custom buttons
        updateButtonStates(theme);

        // Notify ApexCharts and other reactive UI components
        window.dispatchEvent(new CustomEvent('pgfood:theme-changed', {
            detail: { theme: theme, isDark: theme === 'dark' }
        }));
    }

    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
        const nextTheme = current === 'dark' ? 'light' : 'dark';
        setTheme(nextTheme);
    }

    function updateButtonStates(theme) {
        document.querySelectorAll('[data-set-theme]').forEach(el => {
            const val = el.getAttribute('data-set-theme');
            if (val === theme) {
                el.classList.add('active', 'btn-primary');
                el.classList.remove('btn-outline-secondary');
            } else {
                el.classList.remove('active', 'btn-primary');
                el.classList.add('btn-outline-secondary');
            }
        });
    }

    // Initialize event listeners when DOM is loaded
    document.addEventListener('DOMContentLoaded', function () {
        const initialTheme = getCurrentTheme();
        setTheme(initialTheme);

        // One-click theme toggle buttons (both on dashboard & login screen)
        document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                if (window.bootstrap && window.bootstrap.Tooltip) {
                    const tip = window.bootstrap.Tooltip.getInstance(this);
                    if (tip) tip.hide();
                }
                this.blur();
                toggleTheme();
            });
        });

        // Explicit set-theme buttons (e.g. inside profile settings page)
        document.querySelectorAll('[data-set-theme]').forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                const targetTheme = this.getAttribute('data-set-theme');
                setTheme(targetTheme);
            });
        });

        // Initialize tooltips if Bootstrap Tooltip API is loaded
        if (window.bootstrap && window.bootstrap.Tooltip) {
            document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
                new window.bootstrap.Tooltip(el);
            });
        }
    });

    // Expose API globally
    window.PGThemeManager = {
        getTheme: getCurrentTheme,
        setTheme: setTheme,
        toggleTheme: toggleTheme,
        isDark: function () {
            return document.documentElement.getAttribute('data-bs-theme') === 'dark';
        }
    };
})();
