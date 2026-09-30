(() => {
  // Preserve open shadow trees as native declarative shadow DOM before remote scripts are removed.
  function preserve(root){
    for(const e of root.querySelectorAll('*')){
      if(e.shadowRoot){
        preserve(e.shadowRoot);
        const template=document.createElement('template');template.setAttribute('shadowrootmode','open');
        template.innerHTML=e.shadowRoot.innerHTML;
        for(const sheet of e.shadowRoot.adoptedStyleSheets || []){try{const style=document.createElement('style');style.textContent=Array.from(sheet.cssRules).map(r=>r.cssText).join('\n');template.content.prepend(style);}catch{}}
        e.prepend(template);
      }
      if(e.tagName==='STYLE' && !e.textContent.trim() && e.sheet){try{e.textContent=Array.from(e.sheet.cssRules).map(r=>r.cssText).join('\n');}catch{}}
      if(e.tagName==='IMG' && e.currentSrc)e.setAttribute('src',e.currentSrc);
      if(e.tagName==='INPUT' && e.checked)e.setAttribute('checked','');
    }
  }
  preserve(document);
  const state=window.__lgCapture || {error:'load-script-did-not-run'};
  const node=document.createElement('script');node.type='application/json';node.id='lg-capture-state';node.textContent=JSON.stringify(state);document.body.append(node);
})();
