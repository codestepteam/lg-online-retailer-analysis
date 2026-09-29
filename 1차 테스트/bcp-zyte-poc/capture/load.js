(async () => {
  const cfg = CONFIG;
  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
  const log = {retailer:cfg.retailer, pageType:cfg.page_type, steps:[], startedAt:new Date().toISOString()};
  window.__lgCapture = log;
  const visible = e => e && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
  const roots = () => {
    const result = [document];
    for (let i=0;i<result.length;i++) for (const e of result[i].querySelectorAll('*')) if(e.shadowRoot) result.push(e.shadowRoot);
    return result;
  };
  const find = step => roots().flatMap(r=>Array.from(r.querySelectorAll(step.selector || 'button,[role="button"]')))
    .find(e=>visible(e) && (!step.text || (e.innerText || e.textContent || '').trim() === step.text) && (!step.text_pattern || new RegExp(step.text_pattern).test((e.innerText || e.textContent || '').trim())));
  const click = async step => {
    let el=find(step);
    const until=Date.now()+Math.min(step.wait_for_ms || 0,8000);
    while(!el && Date.now()<until){await sleep(250);el=find(step);}
    if(!el){ log.steps.push({...step,status:'not-present'});return false; }
    if(step.expand && el.getAttribute('aria-expanded')==='true'){log.steps.push({...step,status:'already-open'});return true;}
    if(step.closedParent && !el.closest(step.closedParent)){log.steps.push({...step,status:'already-open'});return true;}
    el.scrollIntoView({block:'center'}); el.click(); await sleep(step.wait_ms || 500);
    log.steps.push({...step,status:'clicked',expanded:el.getAttribute('aria-expanded')}); return true;
  };
  for(const step of cfg.cookies || []) {if(find(step)){await click(step);break;}}
  const readyUntil=Date.now()+5000;
  while(!document.querySelector(cfg.ready) && Date.now()<readyUntil) await sleep(250);
  log.ready=!!document.querySelector(cfg.ready);
  for(const step of cfg.steps || []) await click(step);
  log.initialMetadata=window.__lgInitialMetadata;
  // ponytail: finite scrolling captures this page, not every page of an infinite catalog.
  const scroller=cfg.scroll_selector ? roots().flatMap(r=>Array.from(r.querySelectorAll(cfg.scroll_selector))).filter(visible).sort((a,b)=>b.scrollHeight-a.scrollHeight)[0] : document.scrollingElement;
  if(!scroller) throw new Error("Configured scroll container missing");
  const scrollPage = async () => {
  let last=-1,stable=0;
  for(let i=0;i<(cfg.scroll_steps || 18);i++){
    const y=Math.min(i*800,scroller.scrollHeight-scroller.clientHeight);
    scroller.scrollTo({top:Math.max(0,y),behavior:'instant'}); await sleep(250);
    stable=y===last?stable+1:0;if(stable>2)break;last=y;
  }
  log.scroll={selector:cfg.scroll_selector || 'document',y:scroller.scrollTop,height:scroller.scrollHeight,reachedBottom:scroller.scrollTop+scroller.clientHeight>=scroller.scrollHeight-4};
  };
  await scrollPage();
  const heightBeforeExpand=scroller.scrollHeight;
  for(const step of cfg.after_scroll || []) await click(step);
  if(scroller.scrollHeight > heightBeforeExpand+100) await scrollPage();
  // Modal contents can be replaced when another tab is opened. Preserve every inspected panel.
  const panels=[];
  for(const panel of cfg.panels || []){
    await click(panel.open);
    const el=roots().flatMap(r=>Array.from(r.querySelectorAll(panel.content))).filter(visible).at(-1);
    if(el && el.textContent.trim().length>=(panel.min_chars||1)){panels.push({label:panel.label,html:el.innerHTML});log.steps.push({panel:panel.label,status:'saved',chars:el.textContent.length});}
    else log.steps.push({panel:panel.label,status:'missing'});
    if(panel.close){
      const clicked=await click(panel.close), until=Date.now()+2500;
      while(find(panel.close) && Date.now()<until) await sleep(150);
      if(!clicked || find(panel.close)) log.steps.push({panel:panel.label+' close',status:'missing'});
    }
  }
  for(const el of document.querySelectorAll('img[loading="lazy"],iframe[loading="lazy"]'))el.loading='eager';
  await Promise.race([Promise.all(Array.from(document.images).map(i=>i.complete?Promise.resolve():new Promise(r=>{i.addEventListener('load',r,{once:true});i.addEventListener('error',r,{once:true});}))),sleep(1500)]);
  if(panels.length){
    const section=document.createElement('section');section.id='lg-captured-panels';
    section.style.cssText='display:block;position:static;max-width:1400px;margin:40px auto;padding:24px;background:white;color:#222';
    const heading=document.createElement('h2');heading.textContent='Captured expanded information';section.append(heading);
    for(const panel of panels){const h=document.createElement('h3');h.textContent=panel.label;const content=document.createElement('div');content.innerHTML=panel.html;section.append(h,content);}
    document.body.append(section);
  }
  scroller.scrollTo({top:0,behavior:'instant'}); window.scrollTo({top:0,behavior:'instant'}); await sleep(350);
  for(const step of cfg.final_steps || []) await click(step);
  log.viewport={width:innerWidth,height:innerHeight};
  if(innerWidth<(cfg.min_viewport_width||0))log.error='Viewport narrower than required';
  log.url=location.href; log.title=document.title;
  log.textLength=document.body.innerText.length;
  log.images=Array.from(document.images).map(i=>({src:i.currentSrc||i.src,loaded:i.complete&&i.naturalWidth>0}));
  log.required=(cfg.required || []).map(selector=>({selector,expected:'present',present:roots().some(r=>r.querySelector(selector))}));
  for(const selector of cfg.required_visible || []) log.required.push({selector,expected:'visible',present:roots().some(r=>Array.from(r.querySelectorAll(selector)).some(visible))});
  for(const selector of cfg.required_hidden || []) log.required.push({selector,expected:'hidden',present:!roots().some(r=>Array.from(r.querySelectorAll(selector)).some(visible))});
  log.cookieRemaining=(cfg.cookie_checks || []).filter(step=>!!find(step));
  log.finishedAt=new Date().toISOString();
})();
