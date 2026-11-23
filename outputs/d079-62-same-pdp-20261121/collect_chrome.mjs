// 이 컴퓨터에 설치된 Chrome을 새 임시 프로필의 별도 창으로 띄워 collector.js 로 주소를 수집한다.
// 사용: node collect_chrome.mjs <임시 프로필 폴더> <순서표 파일>
//  - 순서표의 작업 이름을 위에서부터 차례로, 한 번에 한 주소씩 연다. 이미 raw2/ 에 있으면 건너뛴다.
//  - 처음에 costco.ca 의 쿠키 안내에서 "Accept All Cookies"를 한 번 누른다(사용자 승인, 임시 프로필에만 적용).
//  - 화면 크기 1200x800. 결과: raw2/<작업 이름>.json, screenshots2/<작업 이름>.jpg (1200x800 원본 크기)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const [profile, queueFile] = process.argv.slice(2);
const names = fs.readFileSync(queueFile, 'utf8').split(/\s+/).filter(Boolean);
const jobs = JSON.parse(fs.readFileSync(path.join(HERE, 'jobs.json'), 'utf8'));
const collector = fs.readFileSync(path.join(HERE, 'collector.js'), 'utf8');
const PORT = Number(process.env.PORT || 9333);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const urlOf = (name) => { const [kind, row] = name.split('-'); return kind === 's' ? jobs.slug.find((s) => s.row === row).alt : jobs.urls[row]; };

const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check',
  '--disable-backgrounding-occluded-windows', '--disable-renderer-backgrounding', '--disable-background-timer-throttling',
  '--window-size=1216,940', 'about:blank'], { stdio: 'ignore' });

async function target() {
  for (let i = 0; i < 40; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch (e) { /* 아직 안 뜸 */ }
    await sleep(500);
  }
  throw new Error('Chrome이 뜨지 않음');
}

const ws = new WebSocket(await target());
await new Promise((r) => ws.addEventListener('open', r));
let seq = 0;
const waiting = new Map();
const events = [];
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.id && waiting.has(d.id)) { waiting.get(d.id)(d); waiting.delete(d.id); } else if (d.method) events.push(d);
});
const send = (method, params = {}) => new Promise((res) => { const id = ++seq; waiting.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const evalJs = async (expression, awaitPromise = false) => {
  const r = await send('Runtime.evaluate', { expression, awaitPromise, returnByValue: true, timeout: 150000 });
  return r.result && r.result.result ? r.result.result.value : 'EVAL ERROR ' + JSON.stringify(r).slice(0, 300);
};
const go = async (url) => {
  events.length = 0;
  await send('Page.navigate', { url });
  for (let i = 0; i < 80 && !events.some((e) => e.method === 'Page.loadEventFired'); i++) await sleep(500);
};

await send('Page.enable');
const VW = Number(process.env.VW || 1200), VH = Number(process.env.VH || 800), GAP = Number(process.env.GAP || 1.2);
await send('Emulation.setDeviceMetricsOverride', { width: VW, height: VH, deviceScaleFactor: 1, mobile: false });

// 쿠키 동의 (Costco 주소가 순서표에 있을 때만, 한 번)
const firstCostco = names.map(urlOf).find((u) => u.includes('costco.ca'));
if (firstCostco) {
  await go(firstCostco);
  let state = 'no button';
  for (let i = 0; i < 30; i++) {
    // 쿠키 관리 기능은 실제 마우스 누름만 동의로 받아들이므로, 단추 위치를 찾아 마우스로 누른다.
    const rect = await evalJs(`(()=>{const b=[...document.querySelectorAll('button')].find(x=>/^Accept All Cookies$/i.test((x.innerText||'').trim())); if(!b||!b.offsetParent) return 'none'; const r=b.getBoundingClientRect(); return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2})})()`);
    if (rect !== 'none' && !String(rect).startsWith('EVAL')) {
      const p = JSON.parse(rect);
      for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x: p.x, y: p.y, button: 'left', clickCount: 1 });
      state = 'clicked';
      break;
    }
    await sleep(500);
  }
  await sleep(state === 'clicked' ? 8000 : 2500);  // 동의 직후 사이트가 페이지를 다시 불러올 수 있어 넉넉히 기다린다
  const after = await evalJs(`(()=>{try{const c=window.airgap.getConsent();return 'confirmed='+c.confirmed+' functional='+c.purposes.Functional}catch(e){return 'consent state unreadable'}})()`);
  console.log('cookie consent:', state, '/', after);
  if (after !== 'confirmed=true functional=true') { console.log('쿠키 동의가 적용되지 않아 멈춤'); ws.close(); chrome.kill(); process.exit(1); }
}

// 배송지 바꾸기(환경 변수 POSTAL 이 있을 때만): 화면 위쪽의 Delivery Location 단추를 눌러 우편번호를 넣고 적용한다.
if (process.env.POSTAL && firstCostco) {
  const click = async (expr) => {
    const rect = await evalJs(`(()=>{const b=${expr}; if(!b) return 'none'; b.scrollIntoView({block:'center'}); const r=b.getBoundingClientRect(); return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2})})()`);
    if (rect === 'none' || String(rect).startsWith('EVAL')) return false;
    const p = JSON.parse(rect);
    for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x: p.x, y: p.y, button: 'left', clickCount: 1 });
    return true;
  };
  await evalJs('window.scrollTo(0,0)');
  console.log('open selector', await click(`document.querySelector('[data-testid="locationselector_DeliveryLocationSelector"] button, button[data-testid="locationselector_DeliveryLocationSelector"]')||document.querySelector('[data-testid="locationselector_DeliveryLocationSelector"]')`));
  await sleep(2000);
  console.log('inputs', await evalJs(`JSON.stringify([...document.querySelectorAll('input')].filter(i=>i.offsetParent).map(i=>(i.id||'')+'|'+(i.name||'')+'|'+(i.placeholder||'')+'|'+(i.getAttribute('aria-label')||'')+'|'+i.value))`));
  console.log('focus input', await click(`[...document.querySelectorAll('input')].find(i=>i.offsetParent&&/postal|zip|delivery/i.test((i.id||'')+(i.name||'')+(i.placeholder||'')+(i.getAttribute('aria-label')||'')))`));
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'a', code: 'KeyA', modifiers: 4, windowsVirtualKeyCode: 65, commands: ['selectAll'] });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', modifiers: 4, windowsVirtualKeyCode: 65 });
  await send('Input.insertText', { text: process.env.POSTAL });
  await sleep(800);
  console.log('typed value:', await evalJs(`(()=>{const i=document.querySelector('[id^="deliverylocationform--zipcode"]');const b=document.querySelector('[data-testid="Button_locationselector_DeliveryLocationSelector--submit"]');return (i?i.value:'no input')+' | submit '+(b?(b.disabled?'disabled':'enabled')+' '+b.innerText:'none')})()`));
  console.log('submit', await click(`[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/^Change Delivery Location$/i.test((b.innerText||'').trim()))`));
  await sleep(3000);
  console.log('form text:', await evalJs(`(()=>{const i=document.querySelector('[id^="deliverylocationform--zipcode"]');let f=i;for(let k=0;k<6&&f;k++)f=f.parentElement;return f?f.innerText.slice(0,300):'form closed'})()`));
  await go(firstCostco);
  await sleep(4000);
  console.log('delivery location now:', await evalJs(`(document.querySelector('[data-testid="locationselector_DeliveryLocationSelector"]')||{}).innerText`));
  if (process.env.POSTAL_ONLY) { ws.close(); chrome.kill(); process.exit(0); }
}

for (const name of names) {
  const out = path.join(HERE, 'raw2', `${name}.json`);
  if (fs.existsSync(out)) { console.log(name, '이미 있음'); continue; }
  try {
    const url = urlOf(name);
    await go(url);
    // 보안 확인 화면이면 풀지 않고 기다린다(사용자가 창에서 직접 푼다). 최대 15분.
    for (let i = 0; i < 180; i++) {
      const t = await evalJs(`document.title+' ## '+(document.querySelector('h1')?document.querySelector('h1').innerText:'')`);
      if (!/Un paso m|Just a moment|잠시만|Verify you are human|captcha/i.test(String(t))) break;
      if (i === 0) console.log(new Date().toISOString(), name, '보안 확인 화면. 사용자가 풀 때까지 기다림');
      await sleep(5000);
    }
    // 페이지가 받아 오는 자료가 2초 동안 더 늘지 않을 때까지 최대 40초 기다린다.
    await evalJs(`(async()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));let p=-1,same=0;for(let i=0;i<80&&same<4;i++){const n=performance.getEntriesByType('resource').length;if(n===p&&document.readyState==='complete')same++;else same=0;p=n;await sleep(500);}return p})()`, true);
    await evalJs(`window.__job=${JSON.stringify({ name, url })};`);
    let summary = await evalJs(collector, true);
    if (String(summary).startsWith('EVAL ERROR')) {  // 수집 도중 페이지가 다시 불려 끊긴 경우 한 번만 다시 연다
      console.log(name, 'retry after', String(summary).slice(0, 120));
      await sleep(3000); await go(url);
      await evalJs(`window.__job=${JSON.stringify({ name, url })};`);
      summary = await evalJs(collector, true);
    }
    if (String(summary).startsWith('EVAL ERROR')) { console.log(name, 'FAILED', String(summary).slice(0, 200)); continue; }
    const body = await evalJs('JSON.stringify(window.__payload||null)');
    if (body && body !== 'null' && !String(body).startsWith('EVAL ERROR')) fs.writeFileSync(out, body);
    const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 85 });
    if (shot.result && shot.result.data) fs.writeFileSync(path.join(HERE, 'screenshots2', `${name}${process.env.FULL ? '.top' : ''}.jpg`), Buffer.from(shot.result.data, 'base64'));
    if (process.env.FULL) {
      // 전체 페이지 그림: 맨 위로 올리고, 늦게 뜨는 사진을 모두 불러온 뒤, 페이지 전체를 4000픽셀 높이 조각으로 찍는다(조각은 stitch_full.py 가 한 장으로 잇는다).
      // 전체 페이지 그림: 화면을 한 칸씩 실제로 내리면서, 그 칸에 보이는 사진이 다 뜬 것을 확인한 뒤 찍는다.
      // 둘째 칸부터는 화면에 붙어 따라다니는 띠(머리말, 담기 띠 등)를 숨겨 같은 띠가 반복해 찍히지 않게 한다.
      const settle = `(async()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));for(const im of document.querySelectorAll('img')){const r=im.getBoundingClientRect();if(r.bottom>-200&&r.top<innerHeight+200&&im.loading==='lazy')im.loading='eager';}let pend=0;for(let i=0;i<24;i++){pend=[...document.querySelectorAll('img')].filter(im=>{const r=im.getBoundingClientRect();return im.offsetParent&&r.width>40&&r.bottom>0&&r.top<innerHeight&&!(im.complete&&im.naturalWidth>0)}).length;if(!pend)break;await sleep(500);}await sleep(700);return JSON.stringify({y:Math.round(scrollY),H:document.documentElement.scrollHeight,pend});})()`;
      // 화면을 따라다니는 영역(sticky)은 제자리에 한 번만 찍히도록 따라다니기를 끈다.
      await evalJs(`(()=>{for(const el of document.querySelectorAll('body *')){if(getComputedStyle(el).position==='sticky'){el.setAttribute('data-lg-unstuck','1');el.style.setProperty('position','relative','important');el.style.setProperty('top','auto','important');el.style.setProperty('bottom','auto','important');}}})()`);
      await evalJs('window.scrollTo(0,0)');
      const segs = []; let y = 0; let guard = 0; let pendTotal = 0;
      while (guard++ < 80) {
        await evalJs(`window.scrollTo(0,${y})`);
        if (segs.length >= 1) await evalJs(`(()=>{for(const el of document.querySelectorAll('body *')){if(el.hasAttribute('data-lg-hidden'))continue;if(getComputedStyle(el).position!=='fixed')continue;const r=el.getBoundingClientRect();if(r.width<1||r.height<1)continue;el.setAttribute('data-lg-hidden','1');el.style.setProperty('visibility','hidden','important');}})()`);
        const st = JSON.parse(await evalJs(settle, true));
        pendTotal += st.pend;
        const seg = await send('Page.captureScreenshot', { format: 'jpeg', quality: 84 });
        const file = `${name}.part${String(segs.length).padStart(2, '0')}.jpg`;
        if (seg.result && seg.result.data) fs.writeFileSync(path.join(HERE, 'screenshots2', file), Buffer.from(seg.result.data, 'base64'));
        segs.push({ file, y: st.y });
        if (st.y + VH >= st.H - 1) break;
        y = st.y + VH;
      }
      const H = segs[segs.length - 1].y + VH;
      fs.writeFileSync(path.join(HERE, 'screenshots2', `${name}.full.json`), JSON.stringify({ name, height: H, width: VW, vh: VH, segs, imgs_pending_total: pendTotal, shot_utc: new Date().toISOString() }));
    }
    console.log(new Date().toISOString(), summary);
  } catch (e) {
    console.log(name, 'ERROR', String(e).slice(0, 200));
  }
  await sleep(GAP * 1000 * (0.8 + Math.random() * 0.4));
}
console.log('DONE');
ws.close();
chrome.kill();
