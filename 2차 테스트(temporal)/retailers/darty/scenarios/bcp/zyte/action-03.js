// Preserve the requested page's head and H1 before scrolling changes its URL.
(() => {
  const visible = e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
  window.__lgInitialMetadata = {
    url: location.href,
    title: Array.from(document.head.querySelectorAll('title')).map(e => e.textContent.trim()),
    metaDescription: Array.from(document.querySelectorAll('meta[name="description" i]')).map(e => e.content || ''),
    robots: Array.from(document.querySelectorAll('meta[name="robots" i]')).map(e => e.content || ''),
    canonical: Array.from(document.querySelectorAll('link[rel~="canonical" i]')).map(e => e.getAttribute('href')),
    h1: Array.from(document.querySelectorAll('h1')).filter(visible).map(e => (e.innerText || e.textContent || '').trim())
  };
})();
