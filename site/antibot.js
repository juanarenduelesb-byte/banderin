/* Banderín - comprobación anti-robots (Cloudflare Turnstile) en los formularios que envían correos.
   Solo se activa cuando hay clave pública en cuenta-config.js (turnstile). Sin cookies de seguimiento.
   Devuelve un token de un solo uso; '' si Turnstile no está configurado. */
(function () {
  let loading = null, wid = null, waiting = null;
  function key() { return (window.CUENTA && window.CUENTA.turnstile) || ''; }
  function load() {
    if (loading) return loading;
    loading = new Promise((ok, ko) => {
      const s = document.createElement('script');
      s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
      s.async = true; s.onload = ok; s.onerror = ko;
      document.head.appendChild(s);
    });
    return loading;
  }
  window.botToken = async function () {
    const k = key();
    if (!k) return '';
    try {
      await load();
      let box = document.getElementById('botBox');
      if (!box) {
        box = document.createElement('div'); box.id = 'botBox';
        box.style.cssText = 'position:fixed;left:50%;bottom:calc(110px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:95';
        document.body.appendChild(box);
      }
      return await new Promise((ok) => {
        waiting = ok;
        const done = (t) => { if (waiting) { const w = waiting; waiting = null; w(t || ''); } };
        if (wid === null) {
          wid = window.turnstile.render(box, {
            sitekey: k, appearance: 'interaction-only', execution: 'execute',
            language: document.documentElement.lang === 'en' ? 'en' : 'es',
            callback: done, 'error-callback': () => done(''), 'timeout-callback': () => done(''), 'expired-callback': () => {}
          });
        } else window.turnstile.reset(wid);
        window.turnstile.execute(wid);
        setTimeout(() => done(''), 30000);
      });
    } catch (e) { return ''; }
  };
})();
