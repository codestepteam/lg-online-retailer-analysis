// Magalu 상품 페이지 확인(S3 보조). Magalu 탭(www.magazineluiza.com.br)에서 실행한다.
// 주소 # 뒤의 목록(receiver.py /go가 붙여 줌, 'https://magazineluiza.com.br/' 뒤 경로 목록)을 같은 사이트 안에서 차례로 받아
// 상품명, 판매자 문구(Vendido por …), Produto indisponível(판매 불가) 표시만 뽑는다. HTML 전체는 저장하지 않는다.
// 속도: 동시 6개로 시작해 60건 연속 성공마다 1개씩 늘리고(최대 5~6개 권장), 403/429/보호 화면이 나오면 1분 쉬고 절반으로 줄인다.
// 진행 확인: window.__mg   끝나면: mgSubmit('magalu')  → receiver.py가 magalu.json으로 저장
(() => {
  const PREFIX = 'https://magazineluiza.com.br/';
  const list = JSON.parse(decodeURIComponent(location.hash.slice('#list='.length)));
  const S = window.__mg = {queue: list.map(p => ({url: PREFIX + p, tries: 0})), results: [], failed: [], workers: 0, target: 6, max: 5,
                           blocks: 0, okStreak: 0, pausedUntil: 0, started: Date.now(), log: []};
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  function textOf(doc) {  // 글자 조각을 공백으로 이어 'Electrolux R$'처럼 판매자 정규식이 읽을 수 있게 한다
    const w = doc.createTreeWalker(doc.body || doc.documentElement, NodeFilter.SHOW_TEXT,
      {acceptNode: n => /^(SCRIPT|STYLE|NOSCRIPT)$/.test(n.parentNode && n.parentNode.nodeName) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT});
    const parts = []; let n;
    while ((n = w.nextNode())) { const t = n.nodeValue.trim(); if (t) parts.push(t); }
    return parts.join(' ');
  }
  async function one(item) {
    const url = item.url.replace('://magazineluiza.com.br', '://www.magazineluiza.com.br');
    let r, h;
    try { r = await fetch(url, {credentials: 'include'}); h = await r.text(); } catch (e) { return {blocked: true, reason: 'fetch ' + e.message}; }
    const d = new DOMParser().parseFromString(h, 'text/html'); const title = (d.title || '').trim();
    if (r.status === 403 || r.status === 429 || (h.length < 60000 && (/protected by|px-captcha|captcha/i.test(h) || !title)))
      return {blocked: true, reason: 'code ' + r.status + ' len ' + h.length};
    const txt = textOf(d); const i = txt.search(/Vendido(?: e entregue)? por/);
    return {rec: {url: item.url, ok: true, code: r.status, final: r.url, title: title.slice(0, 200), sold: i >= 0 ? txt.slice(i, i + 200) : '',
                  unavail: /Produto indispon[ií]vel/i.test(txt), len: h.length}};
  }
  async function worker() {
    S.workers++;
    while (S.queue.length) {
      if (S.workers > S.target) break;
      if (Date.now() < S.pausedUntil) { await sleep(1000); continue; }
      const item = S.queue.shift(); const res = await one(item);
      if (res.rec) {
        S.results.push(res.rec); S.okStreak++;
        if (S.okStreak >= 60 && S.target < S.max) { S.target++; S.okStreak = 0; S.log.push(Date.now() + ' up ' + S.target); worker(); }
      } else {
        item.tries++; S.blocks++; S.okStreak = 0;
        if (item.tries < 3) S.queue.push(item); else S.failed.push({url: item.url, ok: false, reason: res.reason});
        if (Date.now() >= S.pausedUntil) { S.pausedUntil = Date.now() + 60000; S.target = Math.max(2, Math.floor(S.target / 2)); S.log.push(Date.now() + ' block ' + res.reason + ' -> ' + S.target); }
      }
      await sleep(900 + Math.random() * 900);
    }
    S.workers--; if (S.workers === 0) S.finished = Date.now();
  }
  window.mgSubmit = (name, port = 8765) => {
    const f = document.createElement('form'); f.method = 'POST'; f.action = `http://127.0.0.1:${port}/submit?name=${name}`;
    const t = document.createElement('textarea'); t.name = 'data'; t.value = JSON.stringify(S.results.concat(S.failed)); f.appendChild(t);
    document.body.appendChild(f); f.submit();
  };
  for (let k = 0; k < S.target; k++) setTimeout(worker, k * 300);
  return {queued: S.queue.length};
})();
