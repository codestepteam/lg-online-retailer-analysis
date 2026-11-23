// 교차 확인용: 이 컴퓨터에 설치된 Chrome을 새 임시 프로필의 별도 창으로 띄워, 같은 수집 스크립트(collector.js)로
// 주소를 다시 수집한다. 본 수집에 쓴 브라우저와 다른 프로그램이라 "다른 도구로 한 번 더" 확인하는 데 쓴다.
// 사용: node crosscheck_chrome.mjs <임시 프로필 폴더> <작업 이름...>   (작업 이름 예: x-7961 x-8001)
// 결과: raw2/<작업 이름>.json (본 수집과 같은 형식)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const [profile, ...names] = process.argv.slice(2);
const jobs = JSON.parse(fs.readFileSync(path.join(HERE, 'jobs.json'), 'utf8'));
const collector = fs.readFileSync(path.join(HERE, 'collector.js'), 'utf8');
const PORT = 9333;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check',
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

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 800, deviceScaleFactor: 1, mobile: false });

for (const name of names) {
  const row = name.split('-')[1];
  const url = jobs.urls[row];
  const out = path.join(HERE, 'raw2', `${name}.json`);
  if (fs.existsSync(out)) { console.log(name, '이미 있음'); continue; }
  events.length = 0;
  await send('Page.navigate', { url });
  for (let i = 0; i < 60 && !events.some((e) => e.method === 'Page.loadEventFired'); i++) await sleep(500);
  await send('Runtime.evaluate', { expression: `window.__job=${JSON.stringify({ name, url })};` });
  const r = await send('Runtime.evaluate', { expression: collector, awaitPromise: true, returnByValue: true, timeout: 120000 });
  const summary = r.result && r.result.result ? r.result.result.value : JSON.stringify(r);
  const p = await send('Runtime.evaluate', { expression: 'JSON.stringify(window.__payload||null)', returnByValue: true });
  const body = p.result && p.result.result ? p.result.result.value : 'null';
  if (body && body !== 'null') fs.writeFileSync(out, body);
  const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 80 });
  if (shot.result && shot.result.data) fs.writeFileSync(path.join(HERE, 'screenshots2', `${name}.jpg`), Buffer.from(shot.result.data, 'base64'));
  console.log(summary);
  await sleep(1500);
}
ws.close();
chrome.kill();
