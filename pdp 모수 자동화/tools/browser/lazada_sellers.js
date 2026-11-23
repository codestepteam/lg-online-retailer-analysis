// Lazada 판매자 확인(S4 보조). Lazada 탭(www.lazada.sg 또는 www.lazada.co.th)에서 실행한다.
// 주소 # 뒤의 페이지 id 목록(receiver.py /go가 붙여 줌)을 같은 사이트의 보이지 않는 iframe으로 띄워
// 판매자 칸(.seller-name-v2__detail-name)과 상점 주소(/shop/…/)를 읽는다. 판매자 이름은 HTML 원본에 없고 화면을 그려야 나온다.
// 속도: 동시 2개, 한 건마다 3.5~6.5초 쉼. 60~70페이지마다 로봇 확인(reCAPTCHA)이 뜬다.
// 로봇 확인이 뜨면 모두 멈춘다(window.__lz.punish === true). 사람이 다른 탭에서 그 상품 주소를 열어 직접 통과시킨 뒤 lzResume()으로 이어 간다.
// 이 스크립트는 로봇 확인을 풀지 않는다.
// 진행 확인: window.__lz   끝나면: lzSubmit('lazada_th')  → receiver.py가 lazada_th.json으로 저장
(() => {
  const ids = JSON.parse(decodeURIComponent(location.hash.slice('#list='.length)));
  const S = window.__lz = {queue: ids.map(id => ({id: String(id), tries: 0})), results: [], failed: [], target: 2, workers: 0, punish: false, started: Date.now(), log: []};
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const NOT_FOUND = /ไม่พบสินค้า|not found|no longer available|ขออภัย|Sorry|unavailable/i;
  async function one(item) {
    const f = document.createElement('iframe');
    f.style.cssText = 'width:1200px;height:900px;position:fixed;left:-4000px;top:0';
    f.src = location.origin + '/products/pdp-i' + item.id + '.html';
    document.body.appendChild(f);
    let res = null;
    for (let k = 0; k < 40; k++) {
      await sleep(500);
      let d, loc;
      try { d = f.contentDocument; loc = f.contentWindow.location.href; } catch (e) { res = {err: 'cross ' + e.message}; break; }
      if (loc && loc.includes('punish')) { res = {punish: true}; break; }
      const a = d && d.querySelector('.seller-name-v2__detail-name, .seller-name__detail-name');
      if (a) { res = {id: item.id, name: a.innerText.trim(), href: a.getAttribute('href'), title: (d.title || '').slice(0, 120), loc: loc.slice(0, 120)}; break; }
      if (d && d.readyState === 'complete' && k > 24 && NOT_FOUND.test(d.body ? d.body.innerText.slice(0, 3000) : '')) {
        res = {id: item.id, notfound: true, title: d.title.slice(0, 100), loc: loc.slice(0, 120)}; break;
      }
    }
    f.remove();
    return res || {id: item.id, timeout: true};
  }
  async function worker() {
    S.workers++;
    while (S.queue.length && !S.punish) {
      const item = S.queue.shift(); const r = await one(item);
      if (r.punish) { S.punish = true; S.queue.unshift(item); S.log.push(Date.now() + ' punish'); break; }
      if (r.name || r.notfound) S.results.push(r);
      else { item.tries++; if (item.tries < 2) S.queue.push(item); else S.failed.push({id: item.id, ...r}); }
      await sleep(3500 + Math.random() * 3000);
    }
    S.workers--; if (S.workers === 0) S.finished = Date.now();
  }
  window.lzResume = () => { S.punish = false; S.finished = 0; for (let k = 0; k < S.target; k++) setTimeout(worker, k * 1500); return {left: S.queue.length}; };
  window.lzSubmit = (name, port = 8765) => {
    const f = document.createElement('form'); f.method = 'POST'; f.action = `http://127.0.0.1:${port}/submit?name=${name}`;
    const t = document.createElement('textarea'); t.name = 'data'; t.value = JSON.stringify(S.results); f.appendChild(t);
    document.body.appendChild(f); f.submit();
  };
  return window.lzResume();
})();
