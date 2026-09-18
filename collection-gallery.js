(() => {
  const root = document.querySelector('#jp-detail-review');
  const data = document.querySelector('#collection-gallery-data');
  if (!root || !data) return;
  const views = JSON.parse(data.textContent);
  const stage = root.querySelector('.gallery-stage');
  const image = stage.querySelector('img');
  const buttons = [...root.querySelectorAll('.image-controls [data-view]')];
  function show(key) {
    const view = views[key];
    if (!view) return;
    image.src = view.src;
    image.alt = view.alt;
    image.width = view.width;
    image.height = view.height;
    image.className = 'hero-img';
    stage.dataset.kind = view.kind;
    stage.style.cssText = view.framing || '';
    root.querySelector('.hero-caption').textContent = view.caption;
    root.querySelector('.hero-source').textContent = view.source;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === key)));
  }
  buttons.forEach((button, index) => {
    button.addEventListener('click', () => show(button.dataset.view));
    button.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + buttons.length) % buttons.length;
      buttons[next].focus();
      show(buttons[next].dataset.view);
    });
  });
})();
