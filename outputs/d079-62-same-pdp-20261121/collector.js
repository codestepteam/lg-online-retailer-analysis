// 브라우저 화면 안에서 실행하는 수집 스크립트.
// 하는 일: 페이지를 끝까지 내려 늦게 뜨는 영역을 불러오고, 접힌 영역(사양표 등)을 펼친 뒤,
// 페이지 원본 전체(별도 영역인 shadow DOM 포함)를 window.__payload 에 담는다.
// 값을 고르거나 고치지 않는다. 값 추출은 저장된 원본에서 extract_values.py 가 한다.
(async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const job = window.__job || {};
  const host = location.hostname;
  const started = new Date().toISOString();
  const notes = ['vis_start ' + document.visibilityState];

  for (let i = 0; i < 60 && !document.querySelector('h1'); i++) await sleep(250);
  // 페이지 불러오기가 끝날 때까지 최대 20초 기다린다.
  for (let i = 0; i < 80 && document.readyState !== 'complete'; i++) await sleep(250);

  const scrollAll = async () => {
    let y = 0, last = 0, stable = 0, guard = 0;
    while (stable < 2 && guard++ < 150) {
      y += 800;
      window.scrollTo(0, y);
      await sleep(300);
      const H = document.documentElement.scrollHeight;
      if (y >= H) {
        await sleep(700);
        const H2 = document.documentElement.scrollHeight;
        if (H2 === last) stable++; else stable = 0;
        last = H2;
        y = Math.min(y, H2);
      }
    }
  };
  await scrollAll();

  if (host.endsWith('costco.ca')) {
    for (const id of ['product_details', 'specifications']) {
      const b = document.getElementById(id);
      if (b && b.getAttribute('aria-expanded') === 'false') { b.click(); await sleep(600); notes.push('opened ' + id); }
      else notes.push(id + (b ? ' already open' : ' missing'));
    }
    // 본품 가격이 뜰 때까지 최대 10초 기다린다.
    for (let i = 0; i < 20 && !document.querySelector('[data-testid="Text_single-price-whole-value"]'); i++) await sleep(500);
    // 제조사 설명(Syndigo)이 그려질 때까지 기다린다. 원본 데이터에 Syndigo 표시가 있으면 최대 30초, 없으면 3초.
    const expects = /contentVendors[^a-zA-Z]{1,8}Syndigo/.test(document.documentElement.innerHTML);
    const limit = expects ? 60 : 6;
    let prev = -1, same = 0;
    for (let i = 0; i < limit + 6; i++) {
      const pp = document.querySelector('syndigo-powerpage');
      const n = pp && pp.shadowRoot ? pp.shadowRoot.innerHTML.length : 0;
      if (n > 0 && n === prev) same++; else same = 0;
      prev = n;
      if (same >= 3) break;
      if (i >= limit && n === 0) break;
      if (n === 0 && pp) pp.scrollIntoView();
      await sleep(500);
    }
    notes.push('expects_syndigo ' + expects);
    // 제조사 설명 제공처가 FlixMedia인 페이지: 상세 영역의 "View More"를 눌러 펼치고, 설명이 그려질 때까지 최대 30초 기다린다.
    const vend = (document.documentElement.innerHTML.match(/contentVendors[^a-zA-Z\]]{1,8}([A-Za-z]+)/) || [])[1] || '';
    notes.push('vendor ' + vend);
    const acc = document.querySelector('[data-testid="Accordion_product_details"]');
    if (acc) for (const b of acc.querySelectorAll('button')) if (/^View More$/i.test((b.innerText || '').trim())) { b.click(); await sleep(500); notes.push('clicked View More'); }
    if (vend === 'FlixMedia') {
      let fprev = -1, fsame = 0, fn = 0;
      for (let i = 0; i < 66; i++) {
        const fx = document.querySelector('#flix-inpage');
        fn = fx ? (fx.innerText || '').length : 0;
        if (fn > 50 && fn === fprev) fsame++; else fsame = 0;
        fprev = fn;
        if (fsame >= 3) break;
        if (i >= 60 && fn <= 50) break;
        if (fx && i % 4 === 0) fx.scrollIntoView();
        await sleep(500);
      }
      notes.push('flix ' + fn);
    }
    notes.push('syndigo ' + prev);
    await scrollAll();
  } else {
    // Falabella 계열: 사양표 "더 보기"와 상세 설명 "더 보기"를 펼친다.
    // 접힌 영역의 "Mostrar más (더 보기)" 단추만 한 번씩 누른다. 같은 영역을 두 번 눌러 다시 접히지 않게 한다.
    // 닫혀 있는 "Especificaciones (사양)" 영역을 연다.
    for (const hd of document.querySelectorAll('button.accordion__header[aria-expanded="false"]')) {
      if (/^Especificaciones/i.test((hd.innerText || '').trim())) { hd.click(); await sleep(800); notes.push('opened Especificaciones'); }
    }
    let opened = 0;
    for (const b of document.querySelectorAll('button.accordion__show-more-btn')) {
      if (/^Mostrar m[aá]s$/i.test((b.innerText || '').trim()) && b.offsetParent) { b.click(); opened++; await sleep(500); }
    }
    const left = [...document.querySelectorAll('button.accordion__show-more-btn')].filter((b) => /^Mostrar m[aá]s$/i.test((b.innerText || '').trim()) && b.offsetParent).length;
    notes.push('more ' + opened + ' still_collapsed ' + left);
    notes.push('accordions ' + [...document.querySelectorAll('button.accordion__header')].map((x) => (x.innerText || '').trim().slice(0, 14) + '=' + x.getAttribute('aria-expanded')).join(','));
    // 제조사 설명 문서(별도 문서)가 들어올 때까지 최대 10초 기다린다.
    let fr = 0;
    for (let i = 0; i < 20; i++) { fr = document.querySelectorAll('#contenidoIndexado iframe').length; if (fr) break; await sleep(500); }
    notes.push('desc_frames ' + fr);
    await sleep(800);
    await scrollAll();
  }

  // 원본 담기: 문서 전체 + shadow DOM + 같은 출처의 iframe
  const shadows = [];
  const walk = (root, path) => {
    for (const el of root.querySelectorAll('*')) {
      if (el.shadowRoot) {
        const p = path + '>' + el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + '[' + shadows.length + ']';
        shadows.push({ path: p, tag: el.tagName.toLowerCase(), id: el.id || '', html: el.shadowRoot.innerHTML });
        walk(el.shadowRoot, p);
      }
    }
  };
  walk(document, '');
  const frames = [...document.querySelectorAll('iframe')].map((f) => {
    let html = null;
    try { html = f.contentDocument ? f.contentDocument.documentElement.outerHTML : null; } catch (e) { html = null; }
    return { id: f.id || '', src: f.src || '', html };
  });

  notes.push('vis_end ' + document.visibilityState);
  const nav = performance.getEntriesByType('navigation')[0];
  window.__payload = {
    name: job.name || '',
    requested_url: job.url || '',
    final_url: location.href,
    title: document.title,
    http_status: nav && nav.responseStatus !== undefined ? nav.responseStatus : null,
    started_utc: started,
    collected_utc: new Date().toISOString(),
    viewport: { w: innerWidth, h: innerHeight, dpr: devicePixelRatio },
    scroll_height: document.documentElement.scrollHeight,
    user_agent: navigator.userAgent,
    notes,
    html: document.documentElement.outerHTML,
    shadows,
    frames,
  };
  // 스크린샷 준비(원본을 담은 뒤에 한다): 상품명이 화면 위쪽에 오도록 맞추고 쿠키 안내 창은 그림을 가리지 않게 숨긴다(동의하지 않음).
  for (const sel of ['#costco-consent-manager', '#transcend-consent-manager']) {
    const c = document.querySelector(sel);
    if (c) { c.style.display = 'none'; window.__payload.notes.push('hid ' + sel); }
  }
  const h1 = document.querySelector('h1');
  window.scrollTo(0, 0);
  await sleep(200);
  if (h1) {
    const top = h1.getBoundingClientRect().top + window.scrollY;
    window.scrollTo(0, Math.max(0, top - (job.h1Offset || 200)));
  }
  await sleep(700);
  // 화면에 보이는 사진이 모두 뜰 때까지 최대 10초 기다린다.
  let pending = 0;
  const inView = (im) => { const r = im.getBoundingClientRect(); return im.offsetParent && r.width > 40 && r.bottom > 0 && r.top < innerHeight; };
  for (const im of document.querySelectorAll('img')) if (inView(im) && im.loading === 'lazy') im.loading = 'eager';
  for (let i = 0; i < 20; i++) {
    pending = [...document.querySelectorAll('img')].filter((im) => {
      const r = im.getBoundingClientRect();
      return im.offsetParent && r.width > 40 && r.bottom > 0 && r.top < innerHeight && !(im.complete && im.naturalWidth > 0);
    }).length;
    if (!pending) break;
    await sleep(500);
  }
  window.__payload.notes.push('imgs_pending ' + pending);

  const p = window.__payload;
  return [p.name, p.http_status, p.viewport.w + 'x' + p.viewport.h, 'html ' + p.html.length, 'sh ' + shadows.length,
    'fr ' + frames.length, (h1 ? h1.innerText.trim().slice(0, 60) : 'NO H1'), p.notes.join('; '),
    p.final_url === p.requested_url ? 'url same' : 'URL CHANGED ' + p.final_url].join(' | ');
})()
