(() => {
  'use strict';
  const dataNode = document.getElementById('postcard-data');
  if (!dataNode) return;
  const rows = JSON.parse(dataNode.textContent), $ = id => document.getElementById(id);
  const redirects = JSON.parse($('postcard-redirects')?.textContent || '{}');
  const hash = location.hash.match(/^#cartolina-([\w-]+)$/);
  if (hash && redirects[hash[1]]) { location.replace(redirects[hash[1]]); return; }
  let index = 0;
  function scale() {
    const width = Number($('card-zoom').value);
    $('card-image').style.width = width + '%';
    $('card-zoom-value').textContent = width + '%';
  }
  function show(i, updateHash = true) {
    index = Math.max(0, Math.min(rows.length - 1, i));
    const row = rows[index];
    $('card-select').value = String(index);
    $('card-image').src = row.preview;
    $('card-image').alt = row.caption || 'Cartolina senza data';
    $('card-full').href = row.image;
    $('card-old').href = row.uncropped || row.old;
    $('card-title').textContent = row.caption || 'Cartolina senza data';
    $('card-text').textContent = row.text || '[Trascrizione non ancora disponibile.]';
    $('card-status').textContent = row.status;
    $('card-note').textContent = row.note || '';
    for (const suffix of ['', '-bottom']) {
      $('card-count' + suffix).textContent = (index + 1) + ' di ' + rows.length;
      $('card-prev' + suffix).disabled = index === 0;
      $('card-next' + suffix).disabled = index === rows.length - 1;
    }
    $('card-zoom').value = '100'; scale();
    $('card-frame').scrollTop = 0; $('card-frame').scrollLeft = 0;
    if (updateHash) history.replaceState(null, '', '#cartolina-' + row.id);
  }
  $('card-select').addEventListener('change', () => show(Number($('card-select').value)));
  for (const suffix of ['', '-bottom']) {
    $('card-prev' + suffix).addEventListener('click', () => show(index - 1));
    $('card-next' + suffix).addEventListener('click', () => show(index + 1));
  }
  $('card-zoom').addEventListener('input', () => { $('card-image').src = rows[index].image; scale(); });
  $('card-fit').addEventListener('click', () => { $('card-zoom').value = '100'; scale(); });
  document.querySelectorAll('[data-card-index]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault(); show(Number(link.dataset.cardIndex));
    $('lettore-cartoline').scrollIntoView({ behavior: 'smooth' });
  }));
  window.addEventListener('hashchange', () => {
    const target = location.hash.match(/^#cartolina-([\w-]+)$/);
    if (target && redirects[target[1]]) { location.replace(redirects[target[1]]); return; }
    const next = target ? rows.findIndex(row => String(row.id) === target[1]) : 0;
    show(next < 0 ? 0 : next, false);
  });
  const initial = hash ? rows.findIndex(row => String(row.id) === hash[1]) : 0;
  show(initial < 0 ? 0 : initial, false);
})();
