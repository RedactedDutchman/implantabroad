const C={US:"United States",MX:"Mexico",CR:"Costa Rica",CO:"Colombia",AR:"Argentina"};
const fmt=n=>"$"+Math.round(n).toLocaleString("en-US");
async function getJSON(p){const r=await fetch(p);return r.json();}
function range(list){if(!list||!list.length)return null;return{low:Math.min(...list.map(x=>x.low)),high:Math.max(...list.map(x=>x.high))};}
function srcList(list){return list.map(s=>`<li><a href="${s.source}" rel="nofollow noopener" target="_blank">${s.label}</a>${s.region?" – "+s.region:""}: ${s.low===s.high?"from "+fmt(s.low):fmt(s.low)+"–"+fmt(s.high)}${s.avg?" (median/avg "+fmt(s.avg)+")":""} (as of ${s.as_of})</li>`).join("");}
function savingsHTML(p,c,q,r,us){
 const name=C[c];
 if(p==="bone_graft"&&us&&r.low>=us.low)return `<p><strong>Bone grafts:</strong> published prices in ${name} (${fmt(r.low)}–${fmt(r.high)}) overlap or exceed the published US range (${fmt(us.low)}–${fmt(us.high)}), so these sources do not show a meaningful saving on grafts alone.</p>`+(q>0?quoteLine(q,r,name):"");
 if(!(q>0))return `<p>Enter your US quote above to see estimated savings.</p>`;
 return quoteLine(q,r,name);}
function quoteLine(q,r,name){
 if(q<=r.low)return `<p><strong>Your quote (${fmt(q)}) is at or below the published range in ${name}</strong>, so we don't see savings from these sources.</p>`;
 if(q<r.high)return `<p><strong>Your quote (${fmt(q)}) falls inside the published range in ${name}.</strong> Savings could be up to ${fmt(q-r.low)} at the low end of the range, or none at the high end, before travel costs.</p>`;
 return `<p><strong>Estimated savings vs your US quote of ${fmt(q)}:</strong> ${fmt(q-r.high)} – ${fmt(q-r.low)}, before travel costs.</p>`;}
async function initCalc(){const f=document.getElementById("calc");if(!f)return;const d=await getJSON("data/prices.json");const msg=document.getElementById("quote-msg");
 f.addEventListener("submit",e=>{e.preventDefault();const p=f.procedure.value,c=f.country.value,raw=f.quote.value.trim().replace(/[$,\s]/g,"");const out=document.getElementById("result");msg.textContent="";
  let q=0;if(raw!==""){q=Number(raw);if(!isFinite(q)||q<0){msg.textContent="Please enter your US quote as a positive number in USD, e.g. 4500.";out.innerHTML="";return;}}
  const us=range(d.prices.US[p]);const note=`<p class="notice">Estimate only, not a quote. Ranges include different items (some are post only, some all-in). Travel, lodging, extra trips and follow-up care are not included.</p>`;
  const usLine=us?`<p>For reference, published US range: ${fmt(us.low)} – ${fmt(us.high)}.</p>`:"";
  if(c==="ANY"){out.innerHTML=compareAll(d,p,q,us)+usLine+note;return;}
  const list=d.prices[c][p];const r=range(list);if(!r){out.innerHTML=`<p>No reliable published figure found for ${d.procedures[p]} in ${C[c]}. We leave it out rather than guess.</p>`;return;}
  out.innerHTML=`<p><strong>Published range in ${C[c]}:</strong> ${fmt(r.low)} – ${fmt(r.high)} (${d.procedures[p]})</p>`+savingsHTML(p,c,q,r,us)+usLine+note+`<details><summary>Sources</summary><ul>${srcList(list)}</ul></details>`;});}
function rankCountries(d,p){const rows=[],missing=[];for(const c of DEST){const r=range(d.prices[c][p]);if(r)rows.push({c,r,list:d.prices[c][p]});else missing.push(c);}
 rows.sort((a,b)=>a.r.low-b.r.low||a.r.high-b.r.high);return{rows,missing};}
function compareAll(d,p,q,us){const{rows,missing}=rankCountries(d,p);
 if(!rows.length)return `<p>No reliable published figures found for ${d.procedures[p]} in any destination.</p>`;
 let h=`<p><strong>${d.procedures[p]}: all destinations, cheapest first</strong> (ranked by the low end of each published range)</p><ol class="rank">`;
 rows.forEach((x,i)=>{h+=`<li class="card"${i===0?' style="border:2px solid #0f6e8c"':""}>${i===0?'<span class="badge" style="background:#0f6e8c;color:#fff">Cheapest published low end</span><br>':""}<strong>${C[x.c]}:</strong> ${fmt(x.r.low)} – ${fmt(x.r.high)}${savingsHTML(p,x.c,q,x.r,us)}<details><summary>Sources for ${C[x.c]}</summary><ul>${srcList(x.list)}</ul></details></li>`;});
 h+="</ol>";if(missing.length)h+=`<p>Not shown: ${missing.map(c=>C[c]).join(", ")}, because no reliable published figure was found for this procedure. We leave it out rather than guess.</p>`;return h;}
const DEST=["MX","CR","CO","AR"];
async function initPriceTable(){document.querySelectorAll("[data-prices]").forEach(async el=>{const d=await getJSON("data/prices.json");const c=el.dataset.prices;let h="<div class='tablewrap'><table><tr><th>Procedure</th><th>Range (USD)</th><th>Sources</th></tr>";
 for(const p in d.procedures){const l=d.prices[c][p];const r=range(l);h+=`<tr><td>${d.procedures[p]}</td><td>${r?fmt(r.low)+" – "+fmt(r.high):"Not found – left out"}</td><td><ul>${l&&l.length?srcList(l):""}</ul></td></tr>`;}
 h+="</table></div>";const lc=(d.local_currency||{})[c];if(lc&&lc.length)h+=`<h3>Published prices in local currency (not converted)</h3><ul>${lc.map(x=>`<li>${x.region}: ${x.text} – <a href="${x.source}" rel="nofollow noopener" target="_blank">${x.label}</a> (as of ${x.as_of})</li>`).join("")}</ul>`;el.innerHTML=h;});}
async function initClinics(){const els=document.querySelectorAll("[data-clinics]");if(!els.length)return;const d=await getJSON("data/clinics.json");const P=(await getJSON("data/prices.json")).procedures;
 const render=(el,list)=>{el.innerHTML=list.length?list.map(c=>`<div class="card"><strong><a href="${c.url}" rel="nofollow noopener" target="_blank">${c.name}</a></strong><br>${c.cities.join(" / ")}, ${C[c.country]}<br><small>${c.procedures.map(p=>P[p]).join(" · ")}</small><br><small>Languages (per site): ${c.languages.join(", ")} · ${c.publishes_prices?`<a href="${c.price_page}" rel="nofollow noopener" target="_blank">Publishes prices</a>`:"No price list found"}${c.accreditation_mentioned_on_site.length?" · Site mentions: "+c.accreditation_mentioned_on_site.join(", ")+" (not verified by us)":""}</small><br><span class="badge">${c.status}</span></div>`).join(""):"<p>No clinics match.</p>";};
 els.forEach(el=>{const fc=el.dataset.clinics;if(fc!=="all"){render(el,d.clinics.filter(c=>c.country===fc));return;}
  const f=document.getElementById("filters");const cs=f.city;
  const fillCities=()=>{const keep=cs.value;cs.length=1;[...new Set(d.clinics.filter(c=>!f.country.value||c.country===f.country.value).flatMap(c=>c.cities))].sort((a,b)=>a.localeCompare(b)).forEach(x=>cs.add(new Option(x,x)));cs.value=[...cs.options].some(o=>o.value===keep)?keep:"";};
  const ORDER={MX:0,CR:1,CO:2,AR:3};const sortC=l=>f.country.value?l:[...l].sort((a,b)=>ORDER[a.country]-ORDER[b.country]||a.cities[0].localeCompare(b.cities[0])||a.name.localeCompare(b.name));
  const go=()=>render(el,sortC(d.clinics.filter(c=>(!f.country.value||c.country===f.country.value)&&(!f.city.value||c.cities.includes(f.city.value))&&(!f.procedure.value||c.procedures.includes(f.procedure.value)))));
  f.country.addEventListener("change",fillCities);f.addEventListener("change",go);fillCities();go();});}
initCalc();initPriceTable();initClinics();
