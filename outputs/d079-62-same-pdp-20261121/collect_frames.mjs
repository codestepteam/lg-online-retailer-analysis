// Falabella 상세 설명 안의 "제조사 설명 문서"(별도 주소의 문서)를 브라우저로 직접 열어 저장한다.
// 유료 수집 서비스 안에서는 이 문서가 열리지 않았기 때문에, 같은 문서 주소를 따로 열어 글과 그림을 읽는다.
// 사용: node collect_frames.mjs <임시 프로필 폴더> <주소 목록 JSON 파일>   결과: raw2/frames/<주소의 sha1>.json
import { spawn } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const [profile, listFile] = process.argv.slice(2);
const srcs = JSON.parse(fs.readFileSync(listFile, 'utf8'));
const PORT = 9334; const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
fs.mkdirSync(path.join(HERE, 'raw2', 'frames'), { recursive: true });
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [`--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check',
  '--disable-backgrounding-occluded-windows', '--disable-renderer-backgrounding', '--disable-background-timer-throttling', '--window-size=1216,940', 'about:blank'], { stdio: 'ignore' });
let wsUrl; for (let i = 0; i < 40; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); const p = l.find((t) => t.type === 'page'); if (p) { wsUrl = p.webSocketDebuggerUrl; break; } } catch (e) {} await sleep(500); }
const ws = new WebSocket(wsUrl); await new Promise((r) => ws.addEventListener('open', r));
let seq = 0; const waiting = new Map();
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && waiting.has(d.id)) { waiting.get(d.id)(d); waiting.delete(d.id); } });
const send = (method, params = {}) => new Promise((res) => { const id = ++seq; waiting.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e, a = false) => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: a, returnByValue: true, timeout: 90000 }); return r.result?.result?.value ?? 'EVAL ERROR ' + JSON.stringify(r).slice(0, 200); };
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 800, deviceScaleFactor: 1, mobile: false });
for (const src of srcs) {
  const id = crypto.createHash('sha1').update(src).digest('hex');
  const out = path.join(HERE, 'raw2', 'frames', id + '.json');
  if (fs.existsSync(out)) { console.log('이미 있음', id); continue; }
  await send('Page.navigate', { url: src });
  const info = await ev(`(async()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));let prev=-1,same=0,n=0;for(let i=0;i<60;i++){n=document.body?document.body.innerText.length:0;if(n>20&&n===prev)same++;else same=0;prev=n;if(same>=4)break;await sleep(500);}
    let y=0;for(let i=0;i<40;i++){y+=800;window.scrollTo(0,y);await sleep(200);if(y>=document.documentElement.scrollHeight)break;}await sleep(1500);window.scrollTo(0,0);
    return JSON.stringify({src:location.href,title:document.title,collected_utc:new Date().toISOString(),text_len:document.body.innerText.length,html:document.documentElement.outerHTML});})()`, true);
  if (String(info).startsWith('EVAL ERROR')) { console.log('ERROR', src.slice(0, 100), info); continue; }
  const o = JSON.parse(info); o.requested_src = src;
  fs.writeFileSync(out, JSON.stringify(o));
  console.log(id.slice(0, 8), 'text', o.text_len, 'html', o.html.length, src.slice(-70));
  await sleep(800);
}
ws.close(); chrome.kill();
