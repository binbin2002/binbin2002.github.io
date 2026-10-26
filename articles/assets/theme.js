(() => {
  let preference;
  try { preference = localStorage.getItem('research-notes-theme'); } catch {}
  const system = matchMedia('(prefers-color-scheme: dark)');
  const apply = value => {
    document.documentElement.dataset.theme = value;
    const button = document.querySelector('[data-theme-toggle]');
    if (button) { button.textContent = value === 'dark' ? '☀ 浅色' : '◐ 深色'; button.setAttribute('aria-label', value === 'dark' ? '切换浅色主题' : '切换深色主题'); }
  };
  apply(preference || (system.matches ? 'dark' : 'light'));
  document.addEventListener('DOMContentLoaded', () => {
    apply(document.documentElement.dataset.theme);
    document.querySelector('[data-theme-toggle]')?.addEventListener('click', () => {
      preference = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      apply(preference);
      try { localStorage.setItem('research-notes-theme', preference); } catch {}
    });
  });
  system.addEventListener('change', event => { if (!preference) apply(event.matches ? 'dark' : 'light'); });
})();
