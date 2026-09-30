(() => {
  const phase = "before_scroll";
  const openRoots = base => {
    const roots = [base];
    for (let i = 0; i < roots.length; i++) {
      for (const element of roots[i].querySelectorAll('*')) {
        if (element.shadowRoot) roots.push(element.shadowRoot);
      }
    }
    return roots;
  };
  const first = (roots, selector) => roots.map(item => item.querySelector(selector)).find(Boolean);
  const root = first(openRoots(document), 'main') || first(openRoots(document), '[role="main"]') || document.body;
  const roots = openRoots(root);
  const all = selector => roots.flatMap(item => Array.from(item.querySelectorAll(selector)));
  const viewport = {width: innerWidth, height: innerHeight};
  const scanBelow = innerHeight * 3;
  const rootTop = root.getBoundingClientRect().top + scrollY;
  const candidates = [];
  let backgroundNodesScanned = 0;
  const clean = value => String(value || '').replace(/\s+/g, ' ').trim();
  const text = element => clean(element?.innerText || element?.textContent).slice(0, 320);
  const path = element => {
    const parts = [];
    for (let node = element; node && node.nodeType === 1 && parts.length < 12; node = node.parentElement || node.getRootNode()?.host) {
      let part = node.tagName.toLowerCase();
      if (node.id) { parts.unshift(part + '#' + node.id); break; }
      let index = 1;
      for (let sibling = node.previousElementSibling; sibling; sibling = sibling.previousElementSibling) {
        if (sibling.tagName === node.tagName) index++;
      }
      parts.unshift(part + ':nth-of-type(' + index + ')');
      if (node === root) break;
    }
    return parts.join(' > ');
  };
  const record = (element, kind, source) => {
    const box = element.getBoundingClientRect();
    if (box.width <= 0 || box.height <= 0 || box.top + scrollY - rootTop > scanBelow || box.bottom + scrollY < rootTop) return;
    const style = getComputedStyle(element);
    if (!element.getClientRects().length || style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return;
    const block = element.closest('section,article,[class*="hero" i],[class*="banner" i],[data-testid*="hero" i],[data-testid*="banner" i]') || element.parentElement;
    const context = block || element.parentElement;
    const heading = context?.querySelector('h1,h2,h3,h4');
    const blockBox = context?.getBoundingClientRect();
    candidates.push({
      kind, elementPath: path(element), containerPath: context ? path(context) : '',
      source: String(source || '').slice(0, 600), alt: element.getAttribute('alt'),
      heading: text(heading), nearbyText: text(context),
      documentTop: Math.round(box.top + scrollY), topFromMain: Math.round(box.top + scrollY - rootTop),
      x: Math.round(box.left + scrollX), width: Math.round(box.width), height: Math.round(box.height),
      area: Math.round(box.width * box.height),
      containerTop: blockBox ? Math.round(blockBox.top + scrollY) : null,
      inCommonUi: !!element.closest('header,nav,footer,aside'),
      productCardHint: !!element.closest('[class*="product-card" i],[class*="product-tile" i],[data-testid*="product-card" i]'),
      loaded: kind === 'image' ? element.complete && element.naturalWidth > 0 :
        kind === 'video' ? element.readyState >= 2 || !!element.poster : null,
    });
  };
  for (const element of all('img,video,svg,iframe')) {
    if (element.tagName === 'IMG') record(element, 'image', element.currentSrc || element.src);
    else if (element.tagName === 'VIDEO') {
      record(element, 'video', element.currentSrc || element.poster || element.querySelector('source')?.src);
    } else if (element.tagName === 'IFRAME') {
      record(element, 'iframe-embed', element.src);
    } else {
      const box = element.getBoundingClientRect();
      if (box.width >= 64 && box.height >= 40) record(element, 'inline-svg', '');
    }
  }
  for (const element of all('section,article,div,a')) {
    const box = element.getBoundingClientRect();
    if (box.width <= 0 || box.height <= 0 || box.top + scrollY - rootTop > scanBelow || box.bottom + scrollY < rootTop) continue;
    backgroundNodesScanned++;
    const background = getComputedStyle(element).backgroundImage;
    if (background && background !== 'none' && /url\(/i.test(background)) record(element, 'css-background', background);
    for (const pseudo of ['::before', '::after']) {
      const image = getComputedStyle(element, pseudo).backgroundImage;
      if (image && image !== 'none' && /url\(/i.test(image)) record(element, 'css-background' + pseudo, image);
    }
  }
  const byArea = [...candidates].sort((a, b) => b.area - a.area || a.documentTop - b.documentTop);
  const byTop = [...candidates].sort((a, b) => a.documentTop - b.documentTop || b.area - a.area);
  const selected = [...new Set([...byArea.slice(0, 100), ...byTop.slice(0, 60)])]
    .sort((a, b) => a.documentTop - b.documentTop || b.area - a.area);
  const evidence = window.__lgHeroEvidence || (window.__lgHeroEvidence = {version: 'id18-candidates-v1', snapshots: {}});
  evidence.snapshots[phase] = {
    url: location.href, capturedAt: new Date().toISOString(), viewport,
    scrollY, rootPath: path(root), rootTop: Math.round(rootTop),
    observationLimitFromMain: scanBelow, pageH1: text(first(roots, 'h1')),
    targetBrand: (window.__lgConfig || {}).target_brand || null,
    targetCategory: (window.__lgConfig || {}).target_category || null,
    targetCategoryCode: (window.__lgConfig || {}).target_category_code || null,
    backgroundNodesScanned, candidateCount: candidates.length,
    retainedCount: selected.length, truncated: selected.length < candidates.length,
    candidates: selected,
  };
  if (phase === 'after_scroll' && window.__lgCapture) window.__lgCapture.heroEvidence = evidence;
})();
