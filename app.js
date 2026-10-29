/* COSTUME Atlas local edition. Reference layout: Anhao (MIT), see LICENSE. */
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const format = value => Number(value).toLocaleString('zh-CN');
  const PAGE = 60;
  const state = { category: '', query: '', view: 'detail', shown: PAGE };
  const grid = $('#grid');
  const viewer = $('#viewer');
  const info = $('#infoDialog');
  const modal = { index: 0, token: 0, returnFocus: null };
  let data = [], categories = [], filtered = [], rendered = 0;
  let searchTimer, copyTimer;

  function renderCategories() {
    const options = [['', '全部', data.length], ...categories.map(category => [category, category, data.filter(item => item.分类 === category).length])];
    $('#categoryTabs').innerHTML = options.map(([value, label, count]) => `<button class="line-tab" type="button" data-category="${esc(value)}" aria-pressed="${value === state.category}"><span class="tab-name">${esc(label)}</span><span class="tab-count">${format(count)} 套服装</span></button>`).join('');
    $('#categorySelect').innerHTML = '<option value="">全部分类</option>' + categories.map(category => `<option value="${esc(category)}">${esc(category)}</option>`).join('');
  }

  function card(item, index) {
    return `<article class="pose-card" role="button" tabindex="0" data-index="${index}" aria-label="查看 ${esc(item.id)} ${esc(item.服装名称)}"><div class="card-image"><img class="main-image" src="${esc(item.缩略图)}" alt="${esc(item.分类)}服装：${esc(item.中文描述)}" loading="lazy" decoding="async"><div class="image-top"><span class="pose-no">${esc(item.id)}</span><span class="angle-tag">${esc(item.分类)}</span></div><span class="zoom-hint"><svg class="icon" width="16" height="16"><use href="#icon-expand"/></svg></span></div><div class="card-body"><h3>${esc(item.服装名称)}</h3><p class="costume-desc">${esc(item.中文描述)}</p><div class="card-meta"><span class="category">${esc(item.分类)}</span><span>· PNG 原图</span></div></div></article>`;
  }

  function render(append = false) {
    if (!append) {
      const terms = state.query.toLowerCase().split(/\s+/u).filter(Boolean);
      filtered = data.filter(item => (!state.category || item.分类 === state.category) && terms.every(term => item.检索.includes(term)));
      rendered = 0;
      grid.innerHTML = '';
    }
    grid.classList.toggle('compact', state.view === 'compact');
    grid.insertAdjacentHTML('beforeend', filtered.slice(rendered, state.shown).map((item, offset) => card(item, rendered + offset)).join(''));
    rendered = Math.min(state.shown, filtered.length);
    grid.setAttribute('aria-busy', 'false');
    $('#resultCount').textContent = `${format(filtered.length)} 套服装`;
    $('#visibleCount').textContent = filtered.length ? `已显示 ${format(rendered)} / ${format(filtered.length)} 套` : '';
    if (!filtered.length) grid.innerHTML = '<div class="empty"><div class="empty-icon"><svg class="icon" width="24" height="24"><use href="#icon-search"/></svg></div><h3>没有找到匹配的服装</h3><p>试试其他关键词，或减少筛选条件。</p><button type="button" id="emptyReset">清除全部筛选</button></div>';
    $('#loadMore').hidden = rendered >= filtered.length;
    $('#loadMore').textContent = `加载更多（剩余 ${format(filtered.length - rendered)} 套）`;
    $('#searchClear').hidden = !$('#searchInput').value;
    $('#categorySelect').value = state.category;
    $('#filterBadge').textContent = Number(Boolean(state.category)) + Number(state.view === 'compact') || '';
    document.querySelectorAll('[data-category]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === state.category)));
    document.querySelectorAll('[data-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === state.view)));
    const chips = [];
    if (state.category) chips.push(['category', `分类：${state.category}`]);
    if (state.query) chips.push(['query', `搜索：${state.query}`]);
    if (state.view === 'compact') chips.push(['view', '简洁卡片']);
    $('#activeFilters').innerHTML = chips.map(([key, label]) => `<button class="filter-chip" type="button" data-clear="${key}" aria-label="移除${esc(label)}">${esc(label)}</button>`).join('');
  }

  function resetView() { state.shown = PAGE; render(); }
  function resetAll() {
    clearTimeout(searchTimer);
    Object.assign(state, { category: '', query: '', view: 'detail', shown: PAGE });
    $('#searchInput').value = '';
    render();
  }

  function showItem() {
    const item = filtered[modal.index];
    const token = ++modal.token;
    $('#viewerCategory').textContent = item.分类;
    $('#viewerPosition').textContent = `${format(modal.index + 1)} / ${format(filtered.length)}`;
    $('#viewerTitle').textContent = item.服装名称;
    $('#viewerId').textContent = item.id;
    $('#viewerDescription').textContent = item.中文描述;
    $('#viewerEnglish').textContent = item.英文关键词;
    $('#viewerMetaCategory').textContent = item.分类;
    $('#viewerDimensions').textContent = '正在读取…';
    $('#copyStatus').textContent = '';
    const image = $('#viewerImage');
    image.src = item.缩略图;
    image.alt = `${item.id} · ${item.中文描述}`;
    const status = $('#imageStatus');
    status.textContent = '正在加载原图…';
    status.hidden = false;
    // Show the thumbnail immediately, then the local WebP, then full PNG.
    const preview = new Image();
    preview.onload = () => { if (token === modal.token && !viewer.hidden && !status.hidden) image.src = item.预览图; };
    preview.src = item.预览图;
    const original = new Image();
    original.onload = () => {
      if (token !== modal.token || viewer.hidden) return;
      image.src = item.原图;
      $('#viewerDimensions').textContent = `${original.naturalWidth} × ${original.naturalHeight} · PNG`;
      status.hidden = true;
    };
    original.onerror = () => {
      if (token !== modal.token || viewer.hidden) return;
      status.textContent = '原图加载失败，请检查本地图片文件';
      $('#viewerDimensions').textContent = '无法读取';
    };
    original.src = item.原图;
    $('#downloadImage').href = item.原图;
    $('#downloadImage').download = `${item.id}.png`;
    $('#openImage').href = item.原图;
    $('#itemPrev').disabled = $('#itemNext').disabled = filtered.length < 2;
  }

  function openViewer(index, trigger) {
    modal.index = index;
    modal.returnFocus = trigger;
    viewer.hidden = false;
    document.body.classList.add('viewer-open');
    for (const node of document.body.children) {
      if (['HEADER', 'SECTION', 'MAIN', 'FOOTER'].includes(node.tagName)) node.inert = true;
    }
    showItem();
    $('#viewerClose').focus();
  }

  function closeViewer() {
    viewer.hidden = true;
    modal.token++;
    document.body.classList.remove('viewer-open');
    for (const node of document.body.children) node.inert = false;
    const item = filtered[modal.index];
    // Reveal the current card if keyboard navigation crossed a loaded page.
    if (modal.index >= rendered) { state.shown = Math.ceil((modal.index + 1) / PAGE) * PAGE; render(true); }
    const target = grid.querySelector(`[data-index="${modal.index}"]`) || modal.returnFocus;
    if (item && target?.isConnected) target.focus({ preventScroll: true });
  }

  function step(direction) {
    modal.index = (modal.index + direction + filtered.length) % filtered.length;
    showItem();
  }

  async function copy(text) {
    clearTimeout(copyTimer);
    try {
      await navigator.clipboard.writeText(text);
      $('#copyStatus').textContent = '已复制到剪贴板';
    } catch {
      $('#copyStatus').textContent = '复制未获浏览器允许，请选中文本手动复制。';
    }
    copyTimer = setTimeout(() => { $('#copyStatus').textContent = ''; }, 3000);
  }

  $('#categoryTabs').addEventListener('click', event => {
    const button = event.target.closest('[data-category]');
    if (button) { state.category = button.dataset.category; resetView(); }
  });
  $('#categorySelect').addEventListener('change', event => { state.category = event.target.value; resetView(); });
  $('#viewFilter').addEventListener('click', event => {
    const button = event.target.closest('[data-view]');
    if (button) { state.view = button.dataset.view; resetView(); }
  });
  $('#searchInput').addEventListener('input', event => {
    clearTimeout(searchTimer);
    const value = event.target.value;
    $('#searchClear').hidden = !value;
    searchTimer = setTimeout(() => { state.query = value.trim(); resetView(); }, 120);
  });
  $('#searchClear').addEventListener('click', () => {
    clearTimeout(searchTimer);
    $('#searchInput').value = state.query = '';
    resetView();
    $('#searchInput').focus();
  });
  $('#filterToggle').addEventListener('click', () => {
    const expanded = $('#filterPanel').classList.toggle('open');
    $('#filterToggle').setAttribute('aria-expanded', String(expanded));
  });
  $('#resetFilters').addEventListener('click', resetAll);
  $('#activeFilters').addEventListener('click', event => {
    const chip = event.target.closest('[data-clear]');
    if (!chip) return;
    const key = chip.dataset.clear;
    state[key] = key === 'view' ? 'detail' : '';
    if (key === 'query') { clearTimeout(searchTimer); $('#searchInput').value = ''; }
    resetView();
  });
  $('#loadMore').addEventListener('click', () => { state.shown += PAGE; render(true); });
  grid.addEventListener('click', event => {
    if (event.target.closest('#emptyReset')) return resetAll();
    const card = event.target.closest('[data-index]');
    if (card) openViewer(Number(card.dataset.index), card);
  });
  grid.addEventListener('keydown', event => {
    const card = event.target.closest('[data-index]');
    if (card && ['Enter', ' '].includes(event.key)) { event.preventDefault(); openViewer(Number(card.dataset.index), card); }
  });
  $('#itemPrev').addEventListener('click', () => step(-1));
  $('#itemNext').addEventListener('click', () => step(1));
  $('#viewerClose').addEventListener('click', closeViewer);
  viewer.addEventListener('click', event => { if (event.target === viewer) closeViewer(); });
  $('#copyId').addEventListener('click', () => copy(filtered[modal.index].id));
  $('#copyDescription').addEventListener('click', () => copy(filtered[modal.index].中文描述));

  let touch = null;
  $('#viewerStage').addEventListener('touchstart', event => {
    const first = event.touches[0];
    touch = event.touches.length === 1 ? { x: first.clientX, y: first.clientY } : null;
  }, { passive: true });
  $('#viewerStage').addEventListener('touchcancel', () => { touch = null; }, { passive: true });
  $('#viewerStage').addEventListener('touchend', event => {
    if (!touch) return;
    const last = event.changedTouches[0];
    const dx = last.clientX - touch.x, dy = last.clientY - touch.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.3 && !event.target.closest('button')) step(dx < 0 ? 1 : -1);
    touch = null;
  }, { passive: true });

  document.addEventListener('keydown', event => {
    if (info.open) return;
    if (!viewer.hidden) {
      if (event.key === 'Escape') { event.preventDefault(); closeViewer(); }
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
        event.preventDefault();
        step(['ArrowRight', 'ArrowDown'].includes(event.key) ? 1 : -1);
      }
      if (event.key === 'Tab') {
        const focusable = [...viewer.querySelectorAll('button:not([disabled]), a[href]')];
        const first = focusable[0], last = focusable.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
      return;
    }
    const editing = event.target.closest('input, textarea, select, [contenteditable="true"]');
    if (event.key === '/' && !editing) { event.preventDefault(); $('#searchInput').focus(); }
    if (event.key === 'Escape' && editing) $('#searchInput').blur();
  });

  const help = {
    guide: ['使用指南', `<ul><li>将服装图导入 AI 工具的<strong>服装参考 / 图像参考</strong>功能，作为穿搭与角色造型参考。</li><li>按季节或风格分类，搜索中文、英文关键词或 ID。多个词用空格分隔，例如<strong>白色 蕾丝</strong>；搜索结果同时满足各词。</li><li>点击卡片查看完整中文描述与英文关键词，下载原尺寸 PNG 可查看更清晰的细节。</li><li><strong>← / →</strong> 或 <strong>↑ / ↓</strong> 浏览当前筛选结果，<strong>Esc</strong> 关闭大图，<strong>/</strong> 聚焦搜索；手机可在图片上左右滑动。</li><li>选择“简洁卡片”可隐藏描述；手机点击“筛选”可展开分类与展示设置。</li><li>图片只有服装，不包含人物。脸部、体型和背景需使用其他参考图或提示词补充。</li><li>中文描述依据原站英文关键词翻译，原词可能是截断的标签列表；请结合图片确认服装细节。</li></ul>`],
    notice: ['注意事项', `<p>以下为原站使用条款的中文译文，原始说明以<a href="https://ai-costume-gallery.pages.dev/" target="_blank" rel="noopener noreferrer">原站</a>为准：</p><ul><li>可免费使用，包括作品创作中的商业使用、编辑和参考使用。</li><li><strong>禁止对图片数据本身进行再分发、转载或转售，包括原尺寸图片及加工后的图片。</strong></li><li>无需署名（署名为自愿）。图片元数据已删除；使用时不提供保证。</li><li>这些是 AI 生成的虚构服装，并非真实商品照片。</li><li>全部服装图通过文字生成图像（t2i）的方式制作，未使用真实商品图片。</li><li>发布前已检查与现有品牌的相似性，但不保证不侵犯第三方权利。</li><li>使用者须自行确认并判断；原作者不承担使用这些数据产生的问题的责任。</li><li>请勿用于表现真实人物、未成年人，或违反公序良俗的用途。</li></ul><div class="info-note">此版本仅供本地参考。界面样式参考 Anhao 的 AI 姿势参考库，其 MIT 代码许可不覆盖服装图片与原始数据。</div>`],
  };
  document.querySelectorAll('[data-info]').forEach(button => button.addEventListener('click', () => {
    const [title, html] = help[button.dataset.info];
    $('#infoTitle').textContent = title;
    $('#infoContent').innerHTML = html;
    info.showModal();
  }));
  $('#infoClose').addEventListener('click', () => info.close());
  info.addEventListener('click', event => {
    const rect = info.getBoundingClientRect();
    if (event.target === info && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) info.close();
  });

  fetch('data/costume-zh.json').then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }).then(items => {
    data = items;
    categories = [...new Set(data.map(item => item.分类))];
    $('#statCostumes').textContent = format(data.length);
    $('#statCategories').textContent = format(categories.length);
    renderCategories();
    render();
  }).catch(() => {
    $('#resultCount').textContent = '图库数据加载失败';
    grid.setAttribute('aria-busy', 'false');
    grid.innerHTML = '<div class="empty"><h3>无法读取服装数据</h3><p>请使用“启动图库.cmd”启动，再通过本地网址访问。<br>同时检查 data/costume-zh.json 是否存在。</p><button type="button" id="reloadData">重新加载</button></div>';
    $('#reloadData').addEventListener('click', () => location.reload());
  });
})();
