(() => {
  const search = document.querySelector('#search');
  const cards = [...document.querySelectorAll('[data-card]')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const params = new URLSearchParams(location.search);
  let category = buttons.some(b => b.dataset.filter === params.get('category')) ? params.get('category') : '全部';
  search.value = params.get('q') || '';
  function render(updateURL = true) {
    const words = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const visible = (category === '全部' || card.dataset.category === category) && words.every(word => card.dataset.search.toLocaleLowerCase().includes(word));
      card.hidden = !visible;
      if (visible) count++;
    });
    document.querySelectorAll('[data-group]').forEach(group => { group.hidden = !group.querySelector('[data-card]:not([hidden])'); });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    document.querySelector('#result-count').textContent = `${count} / ${cards.length} 篇文章`;
    document.querySelector('#empty').hidden = count !== 0;
    if (updateURL) {
      const url = new URL(location.href);
      search.value.trim() ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
      category !== '全部' ? url.searchParams.set('category', category) : url.searchParams.delete('category');
      try { history.replaceState(null, '', url); } catch {}
    }
  }
  search.addEventListener('input', () => render());
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; render(); }));
  document.querySelector('#reset').addEventListener('click', () => { search.value = ''; category = '全部'; render(); search.focus(); });
  render(false);
})();
