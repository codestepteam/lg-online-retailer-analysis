// Consent can arrive after hydration, and accepting it can reload the document.
(async () => {
  const steps = [{"selector": ".js-cookies-info-reject", "text": "Odmítnout vše"}];
  const deadline = Date.now() + 5000;
  while (Date.now() < deadline) {
    const roots = [document];
    for (let i=0;i<roots.length;i++) for (const el of roots[i].querySelectorAll('*')) if (el.shadowRoot) roots.push(el.shadowRoot);
    for (const step of steps) {
      const el = roots.flatMap(r=>Array.from(r.querySelectorAll(step.selector))).find(e=>e.getClientRects().length && (!step.text || (e.innerText || e.textContent || e.value || '').trim()===step.text));
      if (el) { setTimeout(()=>el.click(),100); return; }
    }
    await new Promise(resolve=>setTimeout(resolve,250));
  }
})();
