(async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const notes = ['vis_start ' + document.visibilityState];
  const started = new Date().toISOString();
  for (let i = 0; i < 60 && !document.querySelector('h1'); i++) await sleep(250);
  for (let i = 0; i < 40 && document.readyState !== 'complete'; i++) await sleep(250);
  const scrollAll = async () => {
    let y = 0, last = 0, stable = 0, guard = 0;
    while (stable < 2 && guard++ < 80) {
      y += 800; window.scrollTo(0, y); await sleep(250);
      const H = document.documentElement.scrollHeight;
      if (y >= H) { await sleep(600); const H2 = document.documentElement.scrollHeight; if (H2 === last) stable++; else stable = 0; last = H2; y = Math.min(y, H2); }
    }
  };
  await scrollAll();
  let opened = 0;
  for (const b of document.querySelectorAll('button.accordion__show-more-btn')) if (/^Mostrar m[aá]s$/i.test((b.innerText || '').trim()) && b.offsetParent) { b.click(); opened++; await sleep(500); }
  const left = [...document.querySelectorAll('button.accordion__show-more-btn')].filter((b) => /^Mostrar m[aá]s$/i.test((b.innerText || '').trim()) && b.offsetParent).length;
  notes.push('more ' + opened + ' still_collapsed ' + left);
  let rt = '';
  for (let i = 0; i < 12; i++) {
    const s = document.querySelector('[data-testid="rr-rating-stars"]');
    rt = s && s.parentElement ? s.parentElement.innerText.trim() : '';
    if (rt && rt !== '(0)') break;
    await sleep(500);
  }
  notes.push('rating_text ' + rt);
  await scrollAll();
  const shadows = [];
  const walk = (root, path) => { for (const el of root.querySelectorAll('*')) if (el.shadowRoot) { const p = path + '>' + el.tagName.toLowerCase() + '[' + shadows.length + ']'; shadows.push({ path: p, tag: el.tagName.toLowerCase(), id: el.id || '', html: el.shadowRoot.innerHTML }); walk(el.shadowRoot, p); } };
  walk(document, '');
  const frames = [...document.querySelectorAll('iframe')].map((f) => { let html = null; try { html = f.contentDocument ? f.contentDocument.documentElement.outerHTML : null; } catch (e) { html = null; } return { id: f.id || '', src: f.src || '', html }; });
  notes.push('vis_end ' + document.visibilityState);
  const nav = performance.getEntriesByType('navigation')[0];
  const cap = { final_url: location.href, title: document.title, http_status: nav && nav.responseStatus !== undefined ? nav.responseStatus : null,
    started_utc: started, collected_utc: new Date().toISOString(), viewport: { w: innerWidth, h: innerHeight, dpr: devicePixelRatio },
    scroll_height: document.documentElement.scrollHeight, user_agent: navigator.userAgent, notes, shadows, frames };
  const h1 = document.querySelector('h1');
  window.scrollTo(0, 0); await sleep(200);
  if (h1) window.scrollTo(0, Math.max(0, h1.getBoundingClientRect().top + window.scrollY - 200));
  await sleep(600);
  for (const im of document.querySelectorAll('img')) { const r = im.getBoundingClientRect(); if (im.offsetParent && r.bottom > 0 && r.top < innerHeight && im.loading === 'lazy') im.loading = 'eager'; }
  await sleep(1200);
  const s = document.createElement('script'); s.type = 'application/json'; s.id = 'lg-capture';
  s.textContent = JSON.stringify(cap).split('<').join('\\u003c');
  document.body.appendChild(s);
})()
