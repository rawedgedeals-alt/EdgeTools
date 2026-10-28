/* WHATIF GA4. Basic consent: no Google requests before an affirmative choice. */
(() => {
  'use strict';
  const id = window.WHATIF_ANALYTICS?.measurementId;
  if (!/^G-[A-Z0-9]+$/.test(id || '') || location.hostname !== 'discoverwhatif.com') return;
  const key = 'whatif_analytics_consent_v1';
  let consent = null, started = false;
  try { consent = localStorage.getItem(key); } catch {}
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  const adsDenied = { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };
  function safePage() {
    const url = new URL(location.origin + location.pathname);
    const params = new URLSearchParams(location.search);
    for (const name of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']) {
      const value = params.get(name);
      if (value) url.searchParams.set(name, value.slice(0, 100));
    }
    return url.href;
  }
  function start() {
    if (started) return;
    started = true;
    window['ga-disable-' + id] = false;
    gtag('consent', 'default', { ...adsDenied, analytics_storage: 'denied' });
    gtag('consent', 'update', { ...adsDenied, analytics_storage: 'granted' });
    gtag('js', new Date());
    let referrer = '';
    try { const u = new URL(document.referrer); referrer = u.origin + u.pathname; } catch {}
    // config sends exactly one page_view; filters and sorting do not create virtual pages.
    gtag('config', id, {
      page_location: safePage(), page_referrer: referrer,
      allow_google_signals: false, allow_ad_personalization_signals: false
    });
    const tag = document.createElement('script');
    tag.async = true;
    tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.append(tag);
  }
  function event(name, params) {
    if (consent === 'granted' && started) gtag('event', name, params);
  }
  const style = document.createElement('style');
  style.textContent = '.analytics-choice{position:fixed;bottom:16px;left:16px;right:16px;max-width:650px;z-index:20;background:#111c2e;color:#f7f9ff;border:1px solid #26f3a0;border-radius:14px;padding:20px;box-shadow:0 8px 35px #0009;font:15px/1.5 system-ui}.analytics-choice[hidden]{display:none}.analytics-choice p{margin:0 0 12px;color:#d1dfec}.analytics-choice button,.analytics-preferences{cursor:pointer;font:inherit;border:1px solid #26f3a0;border-radius:7px;padding:8px 12px;background:#142036;color:#c5ffe8;margin:4px}.analytics-choice a{color:#9aefcb}';
  document.head.append(style);
  const box = document.createElement('section');
  box.className = 'analytics-choice';
  box.setAttribute('aria-label', 'Analytics preferences');
  box.innerHTML = '<p>Allow optional analytics to help improve WHATIF? Google Analytics measures visits and link clicks. The tools and guides work either way. <a href="/privacy.html">Privacy details</a></p><button type="button" data-choice="denied">Decline analytics</button><button type="button" data-choice="granted">Allow analytics</button><button type="button" data-close hidden>Close</button>';
  const close = box.querySelector('[data-close]');
  box.hidden = consent === 'granted' || consent === 'denied';
  function eraseCookies() {
    for (const cookie of document.cookie.split(';')) {
      const name = cookie.trim().split('=')[0];
      if (!/^_ga(?:_|$)/.test(name)) continue;
      for (const domain of ['', ';domain=discoverwhatif.com', ';domain=.discoverwhatif.com']) {
        document.cookie = name + '=;max-age=0;path=/' + domain;
      }
    }
  }
  box.addEventListener('click', e => {
    const button = e.target.closest('button');
    if (!button) return;
    if (button.hasAttribute('data-close')) { box.hidden = true; return; }
    consent = button.dataset.choice;
    try { localStorage.setItem(key, consent); } catch {}
    box.hidden = true;
    if (consent === 'granted') {
      if (started) {
        window['ga-disable-' + id] = false;
        gtag('consent', 'update', { ...adsDenied, analytics_storage: 'granted' });
      } else start();
    } else {
      window['ga-disable-' + id] = true;
      if (started) gtag('consent', 'update', { ...adsDenied, analytics_storage: 'denied' });
      eraseCookies();
    }
  });
  document.body.append(box);
  const preferences = document.createElement('button');
  preferences.type = 'button';
  preferences.className = 'analytics-preferences';
  preferences.textContent = 'Analytics preferences';
  preferences.addEventListener('click', () => {
    close.hidden = false;
    box.hidden = false;
    box.querySelector('button').focus();
  });
  (document.querySelector('footer') || document.body).append(preferences);
  if (consent === 'granted') start();
  document.addEventListener('click', e => {
    const filter = e.target.closest('[data-filter]');
    if (filter) event('directory_filter', { category: filter.dataset.filter });
    const link = e.target.closest('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.protocol === 'mailto:') { event('contact_click', { placement: link.closest('.ad-slot') ? 'ad' : 'page' }); return; }
    if (url.protocol !== 'https:' || url.hostname === location.hostname) return;
    const card = link.closest('.card');
    if (card) event('tool_click', {
      tool_name: card.querySelector('h3')?.textContent || '',
      category: card.querySelector('.tag')?.textContent || '',
      provider_domain: url.hostname, affiliate: link.rel.includes('sponsored')
    });
    else if (link.closest('.ad-slot')) event('sponsor_click', {
      placement: link.closest('.ad-slot').className.match(/ad-(hero|mid|bottom)/)?.[1] || '',
      provider_domain: url.hostname
    });
  });
})();
