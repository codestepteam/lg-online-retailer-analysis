// Darty 상품 화면 확인(S4 보조). 한국에서는 'FNAC DARTY - Maintenance'(403)로 막히므로 프랑스 VPN을 켠 뒤 Darty 탭에서 실행한다.
// 아래 PATHS에 확인할 주소의 경로('/nav/achat/…html')를 넣는다. 보이지 않는 iframe으로 띄워 상품 제목(h1)부터
// 'Les points forts' 앞까지에서 판매자 문구(Vendu par …)와 PRODUIT INDISPONIBLE(판매 불가), PRODUIT ÉPUISÉ(품절)를 찾는다.
// 그 아래 '비슷한 상품' 칸의 판매자는 다른 상품 것이라 읽지 않는다.
// 진행 확인: window.__dt.results
const PATHS = [/* '/nav/achat/gros_electromenager/lavage_sechage/seche-linge/bosch_wtw96430ff.html', … */];
(() => {
  const S = window.__dt = {queue: [...PATHS], results: [], started: Date.now()};
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  async function one(path) {
    const f = document.createElement('iframe');
    f.style.cssText = 'width:1200px;height:900px;position:fixed;left:-4000px;top:0';
    f.src = path; document.body.appendChild(f);
    let res = null;
    for (let k = 0; k < 40; k++) {
      await sleep(500);
      let d; try { d = f.contentDocument; } catch (e) { res = {path, err: e.message}; break; }
      const h1 = d && d.querySelector('h1');
      if (h1 && d.readyState === 'complete') {
        await sleep(800);
        const t = d.body.innerText.replace(/\s+/g, ' ');
        const a = t.indexOf(h1.innerText.trim().slice(0, 30)); const b = t.indexOf('Les points forts');
        const main = t.slice(Math.max(0, a), b > a ? b : a + 1500);
        res = {path, title: (d.title || '').slice(0, 90), h1: h1.innerText.trim().slice(0, 80),
               seller: (main.match(/Vendu (?:et (?:expédié|installé) )?par [^\d€]{0,40}/i) || [''])[0],
               indisponible: /PRODUIT INDISPONIBLE/i.test(main), epuise: /PRODUIT ÉPUISÉ/i.test(main), main: main.slice(0, 260)};
        break;
      }
    }
    f.remove();
    return res || {path, timeout: true};
  }
  (async () => { while (S.queue.length) { S.results.push(await one(S.queue.shift())); await sleep(2500 + Math.random() * 2000); } S.done = Date.now(); })();
  return {queued: PATHS.length};
})();
