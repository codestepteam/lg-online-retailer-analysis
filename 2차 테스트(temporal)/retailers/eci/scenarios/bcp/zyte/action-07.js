(() => {
  const cfg = window.__lgConfig || {};
  const state = window.__lgCapture || (window.__lgCapture = {});
  const roots = [document];
  for (let i = 0; i < roots.length; i++) {
    for (const element of roots[i].querySelectorAll('*')) {
      if (element.shadowRoot) roots.push(element.shadowRoot);
    }
  }
  const visible = element => !!(element && element.getClientRects().length && getComputedStyle(element).visibility !== 'hidden');
  const text = element => (element?.innerText || element?.textContent || '').replace(/\s+/g, ' ').trim();
  const all = selector => roots.flatMap(root => Array.from(root.querySelectorAll(selector)));

  state.evidenceVersion = 'bcp-v1';
  state.requireScrollBottom = !!cfg.require_scroll_bottom;
  state.metadata = {
    title: document.title,
    metaDescription: Array.from(document.querySelectorAll('meta[name="description" i]')).map(node => node.content || ''),
    robots: Array.from(document.querySelectorAll('meta[name="robots" i]')).map(node => node.content || ''),
    canonical: Array.from(document.querySelectorAll('link[rel~="canonical" i]')).map(node => node.href || node.getAttribute('href') || ''),
    h1: all('h1').filter(visible).map(text),
  };
  state.images = all('img').map((image, index) => ({
    index,
    src: image.currentSrc || image.src || '',
    alt: image.getAttribute('alt'),
    renderedWidth: image.getBoundingClientRect().width,
    renderedHeight: image.getBoundingClientRect().height,
    renderedArea: image.getBoundingClientRect().width * image.getBoundingClientRect().height,
    naturalWidth: image.naturalWidth || 0,
    naturalHeight: image.naturalHeight || 0,
    naturalArea: (image.naturalWidth || 0) * (image.naturalHeight || 0),
    loaded: image.complete && image.naturalWidth > 0,
    visible: visible(image),
  }));
  state.clickables = all('a[href],button,[role="button"]')
    .filter(visible)
    .slice(0, 1000)
    .map((element, index) => ({
      index,
      tag: element.tagName.toLowerCase(),
      text: text(element).slice(0, 300),
      href: element.href || '',
      ariaLabel: element.getAttribute('aria-label') || '',
      expanded: element.getAttribute('aria-expanded'),
    }));
})();
