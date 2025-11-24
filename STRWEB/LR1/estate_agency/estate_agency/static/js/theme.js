(function() {
  'use strict';

  const THEME_STORAGE_KEY = 'estate-agency-theme';
  const THEME_LIGHT = 'light';
  const THEME_DARK = 'dark';

  function getInitialTheme() {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    if (savedTheme) {
      return savedTheme;
    }
    
    return THEME_LIGHT;
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_STORAGE_KEY, theme);

    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
      toggle.checked = theme === THEME_DARK;
    }
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || getInitialTheme();
    const newTheme = currentTheme === THEME_LIGHT ? THEME_DARK : THEME_LIGHT;
    applyTheme(newTheme);
  }

  function initTheme() {
    const initialTheme = getInitialTheme();
    applyTheme(initialTheme);

    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
      toggle.addEventListener('change', toggleTheme);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
})();

