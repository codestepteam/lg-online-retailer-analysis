// Open every on-page brand-category FAQ answer before recording the final DOM.
(async () => {
  const buttons = Array.from(document.querySelectorAll(
    '[data-test="mms-content-faq-section"] button[aria-controls][aria-expanded]'
  ));
  const checked = [];
  for (const button of buttons) {
    const label = (button.innerText || button.textContent || '').replace(/\s+/g, ' ').trim();
    if (button.getAttribute('aria-expanded') === 'false') {
      button.scrollIntoView({block: 'center'});
      button.click();
      await new Promise(resolve => setTimeout(resolve, 250));
    }
    checked.push({label, expanded: button.getAttribute('aria-expanded') === 'true'});
  }
  const state = window.__lgCapture || (window.__lgCapture = {});
  state.faqExpansion = checked;
})();
