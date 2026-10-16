const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../analytics.js'), 'utf8');

function setup({ hostname = 'discoverwhatif.com', id = 'G-TEST123', saved = null } = {}) {
  class Element {
    constructor(tag) { this.tag = tag; this.children = []; this.handlers = {}; }
    append(el) { this.children.push(el); }
    setAttribute() {}
    addEventListener(name, fn) { this.handlers[name] = fn; }
    querySelector(name) { return this.controls[name] ||= new Element('button'); }
    focus() {}
    controls = {};
  }
  const head = new Element('head'), body = new Element('body'), footer = new Element('footer');
  const document = {
    head, body, cookie: '', referrer: 'https://example.org/ref?q=private', handlers: {},
    createElement: tag => new Element(tag),
    querySelector: () => footer,
    addEventListener(name, fn) { this.handlers[name] = fn; }
  };
  const window = { WHATIF_ANALYTICS: { measurementId: id } };
  let stored = saved;
  const context = { window, document, location: { hostname, origin: 'https://' + hostname, pathname: '/', search: '?email=private&utm_source=launch', hash: '#hidden' }, localStorage: { getItem: () => stored, setItem: (_, value) => { stored = value; } }, URL, URLSearchParams, Date };
  vm.runInNewContext(source, context);
  function choose(value) {
    const box = body.children[0];
    box.handlers.click({ target: { closest: () => ({ hasAttribute: () => false, dataset: { choice: value } }) } });
  }
  return { head, body, footer, window, document, choose, tags: () => head.children.filter(x => x.tag === 'script'), commands: () => window.dataLayer || [] };
}

for (const config of [{hostname:'preview.vercel.app'}, {id:''}, {hostname:'localhost'}]) {
  const s = setup(config);
  assert.equal(s.head.children.length, 0, 'Unconfigured and nonproduction hosts must not start analytics');
}
const s = setup();
assert.equal(s.tags().length, 0, 'No Google requests before consent');
s.choose('denied');
assert.equal(s.tags().length, 0, 'Declining must not load Google');
s.choose('granted');
assert.equal(s.tags().length, 1);
const configs = () => s.commands().filter(x => x[0] === 'config');
assert.equal(configs().length, 1);
assert.equal(configs()[0][2].page_location, 'https://discoverwhatif.com/?utm_source=launch');
assert.equal(configs()[0][2].page_referrer, 'https://example.org/ref');
s.choose('granted');
assert.equal(s.tags().length, 1, 'Repeated consent must not insert a duplicate tag');
assert.equal(configs().length, 1, 'Repeated consent must not duplicate page views');
const card = { querySelector: sel => ({ textContent: sel === 'h3' ? 'Shopify' : 'COMMERCE' }) };
const link = { href:'https://shopify.com/?affiliate=private', rel:'sponsored noopener', closest: sel => sel === '.card' ? card : null };
const click = () => s.document.handlers.click({target:{closest:sel => sel === 'a[href]' ? link : null}});
click();
const events = () => s.commands().filter(x => x[0] === 'event');
assert.equal(events().length, 1);
assert.equal(events()[0][1], 'tool_click');
assert.equal(events()[0][2].provider_domain, 'shopify.com');
assert(!JSON.stringify(events()).includes('private'), 'Outbound query values must not be collected');
s.choose('denied');
assert.equal(s.window['ga-disable-G-TEST123'], true);
click();
assert.equal(events().length, 1, 'Revoking consent must stop custom events');
const returning = setup({saved:'granted'});
assert.equal(returning.tags().length, 1, 'Returning consenting visitors start once');
assert.equal(setup({saved:'denied'}).tags().length, 0);
console.log('PASS: production guard, consent, withdrawal, single page view, safe attribution and outbound events');
