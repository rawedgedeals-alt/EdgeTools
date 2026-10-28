/* WHATIF advertising: only active, approved, paid campaigns appear.
   No free placeholder billboards on the first-party software storefront. */
(() => {
  "use strict";
  const positions = [
    ["hero", document.querySelector("#tools"), "afterend"],
    ["mid", document.querySelector("#guides"), "afterend"],
    ["bottom", document.querySelector("footer"), "beforebegin"]
  ];
  const css = document.createElement("style");
  css.textContent = '.ad-slot{position:relative;overflow:hidden;margin:24px 4%;padding:23px 28px;background:linear-gradient(120deg,#141935,#281c4b 68%,#182842);border:1px solid #a591ff8f;border-radius:19px;box-shadow:0 14px 46px #03041670}.ad-slot:before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#6fe6ff,#a58dff,#ff7ccb)}.ad-label{font-size:11px;letter-spacing:.13em;font-weight:950;color:#b6a4ff}.ad-slot h2{font-size:clamp(22px,4vw,35px);margin:8px 0;color:#fff}.ad-slot p{font-size:15px;color:#d2d4eb;margin:4px 0 16px}.ad-slot a{display:inline-block;padding:11px 17px;border-radius:9px;background:#b9a6ff;color:#0e0926;text-decoration:none;font-size:13px;font-weight:900}.ad-slot a:focus-visible{outline:3px solid #72e7ff;outline-offset:4px}@media(max-width:600px){.ad-slot{margin:20px 5%;padding:20px}}';
  document.head.appendChild(css);
  const safeUrl = (u) => {
    try { const url = new URL(u); return url.protocol === "https:" ? url.href : null; } catch { return null; }
  };
  fetch("./ads.json", {cache:"no-store"})
    .then(r => r.ok ? r.json() : [])
    .then(data => {
      if (!Array.isArray(data)) return;
      for (const [slot, anchor, direction] of positions) {
        if (!anchor) continue;
        const campaign = data.find(x => x && x.slot === slot && x.active === true && safeUrl(x.url) && typeof x.headline === "string" && x.headline.trim());
        if (!campaign) continue; // No sponsor, no advertisement.
        const wrap = document.createElement("aside");
        wrap.className = "ad-slot ad-"+slot;
        wrap.setAttribute("aria-label","Paid sponsored advertisement");
        const label = document.createElement("div");
        label.className="ad-label";
        label.textContent="PAID ADVERTISEMENT";
        const h=document.createElement("h2"); h.textContent=campaign.headline.slice(0,100);
        const p=document.createElement("p"); p.textContent=String(campaign.description||"").slice(0,350);
        const a=document.createElement("a"); a.href=safeUrl(campaign.url);
        a.target="_blank"; a.rel="sponsored noopener noreferrer"; a.textContent=String(campaign.cta||"LEARN MORE").slice(0,70);
        wrap.append(label,h,p,a);
        anchor.insertAdjacentElement(direction,wrap);
      }
    }).catch(() => {});
})();
