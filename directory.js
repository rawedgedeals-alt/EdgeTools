let products=[],filter="All",q="",sort="az",affiliateMap={};
const root=document.querySelector("#cards"),counter=document.querySelector("#results-count");
products=Array.from(root.querySelectorAll(".card"),card=>{const tag=card.querySelector(".tag").textContent;return {name:card.querySelector("h3").textContent,category:tag==="AI"?"AI":tag[0]+tag.slice(1).toLowerCase(),description:card.querySelector("p").textContent,bestFor:card.querySelector(".best").textContent.replace(/^GOOD FOR: /,""),url:card.querySelector("a").href}});
function https(u){try{const p=new URL(u);return p.protocol==="https:"?p.href:null}catch{return null}}
function render(){
root.replaceChildren();
let rows=products.filter(p=>(filter==="All"||p.category===filter)&&(p.name+" "+p.category+" "+p.description+" "+(p.bestFor||"")).toLowerCase().includes(q));
rows.sort((a,b)=>sort==="za"?b.name.localeCompare(a.name):a.name.localeCompare(b.name));counter.textContent=rows.length+" of "+products.length+" tools";
if(!rows.length){const el=document.createElement("div");el.className="empty";el.textContent="No matching tools. Try another category or search.";root.append(el);return}
for(const p of rows){const card=document.createElement("article");card.className="card";
const tag=document.createElement("span");tag.className="tag";tag.textContent=p.category.toUpperCase();
const h=document.createElement("h3");h.textContent=p.name;
const best=document.createElement("div");best.className="best";best.textContent=p.bestFor?"GOOD FOR: "+p.bestFor:"";
const desc=document.createElement("p");desc.textContent=p.description;card.append(tag,h,best,desc);
const aff=affiliateMap[p.name],approved=aff&&aff.approved===true?https(aff.url):null,url=approved||https(p.url);
if(url){const link=document.createElement("a");link.href=url;link.target="_blank";link.rel=(approved?"sponsored ":"")+"noopener noreferrer";link.textContent="EXPLORE "+p.name.toUpperCase()+" →";link.setAttribute("aria-label","Visit "+p.name+" website in a new tab");card.append(link);
if(approved){const note=document.createElement("small");note.className="affiliate-note";note.textContent="Affiliate link: WHATIF may earn a commission.";card.append(note)}}
root.append(card)}}
document.querySelectorAll("[data-filter]").forEach(b=>b.addEventListener("click",()=>{filter=b.dataset.filter;document.querySelectorAll("[data-filter]").forEach(v=>{v.classList.toggle("active",v===b);v.setAttribute("aria-pressed",String(v===b))});render()}));
document.querySelector("#search").addEventListener("input",e=>{q=e.target.value.trim().toLowerCase();render()});
document.querySelector("#sort").addEventListener("change",e=>{sort=e.target.value;render()});
document.querySelector("#year").textContent=new Date().getFullYear();
Promise.all([fetch("./tools.json").then(r=>{if(!r.ok)throw Error("Directory");return r.json()}),fetch("./affiliate-links.json",{cache:"no-store"}).then(r=>r.ok?r.json():{programs:[]}).catch(()=>({programs:[]}))]).then(([items,affiliates])=>{if(!Array.isArray(items))throw Error("Directory data");products=items.filter(x=>x&&typeof x.name==="string"&&typeof x.description==="string"&&typeof x.category==="string");for(const a of (Array.isArray(affiliates.programs)?affiliates.programs:[])){if(a&&a.approved===true&&typeof a.name==="string"&&https(a.url))affiliateMap[a.name]=a}render()}).catch(()=>{counter.textContent="Showing the directory. Live updates are temporarily unavailable."});
