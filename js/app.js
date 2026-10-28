const C={US:"United States",MX:"Mexico",CR:"Costa Rica",AR:"Argentina"};
const fmt=n=>"$"+Math.round(n).toLocaleString("en-US");
async function getJSON(p){const r=await fetch(p);return r.json();}
function range(list){if(!list||!list.length)return null;return{low:Math.min(...list.map(x=>x.low)),high:Math.max(...list.map(x=>x.high))};}
function srcList(list){return list.map(s=>`<li><a href="${s.source}" rel="nofollow noopener" target="_blank">${s.label}</a>${s.region?" – "+s.region:""}: ${fmt(s.low)}–${fmt(s.high)} (as of ${s.as_of})</li>`).join("");}
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
  const list=d.prices[c][p];const r=range(list);if(!r){out.innerHTML=`<p>No reliable published figure found for ${d.procedures[p]} in ${C[c]}. We leave it out rather than guess.</p>`;return;}
  const us=range(d.prices.US[p]);
  let h=`<p><strong>Published range in ${C[c]}:</strong> ${fmt(r.low)} – ${fmt(r.high)} (${d.procedures[p]})</p>`+savingsHTML(p,c,q,r,us);
  if(us)h+=`<p>For reference, published US range: ${fmt(us.low)} – ${fmt(us.high)}.</p>`;
  h+=`<p class="notice">Estimate only, not a quote. Ranges include different items (some are post only, some all-in). Travel, lodging, extra trips and follow-up care are not included.</p><details><summary>Sources</summary><ul>${srcList(list)}</ul></details>`;out.innerHTML=h;});}
async function initPriceTable(){document.querySelectorAll("[data-prices]").forEach(async el=>{const d=await getJSON("data/prices.json");const c=el.dataset.prices;let h="<div class='tablewrap'><table><tr><th>Procedure</th><th>Range (USD)</th><th>Sources</th></tr>";
 for(const p in d.procedures){const l=d.prices[c][p];const r=range(l);h+=`<tr><td>${d.procedures[p]}</td><td>${r?fmt(r.low)+" – "+fmt(r.high):"Not found – left out"}</td><td><ul>${l&&l.length?srcList(l):""}</ul></td></tr>`;}
 el.innerHTML=h+"</table></div>";});}
async function initClinics(){const els=document.querySelectorAll("[data-clinics]");if(!els.length)return;const d=await getJSON("data/clinics.json");const P=(await getJSON("data/prices.json")).procedures;
 const render=(el,list)=>{el.innerHTML=list.length?list.map(c=>`<div class="card"><strong><a href="${c.url}" rel="nofollow noopener" target="_blank">${c.name}</a></strong><br>${c.cities.join(" / ")}, ${C[c.country]}<br><small>${c.procedures.map(p=>P[p]).join(" · ")}</small><br><span class="badge">${c.status}</span></div>`).join(""):"<p>No clinics match.</p>";};
 els.forEach(el=>{const fc=el.dataset.clinics;if(fc!=="all"){render(el,d.clinics.filter(c=>c.country===fc));return;}
  const f=document.getElementById("filters");const cs=f.city;
  const fillCities=()=>{const keep=cs.value;cs.length=1;[...new Set(d.clinics.filter(c=>!f.country.value||c.country===f.country.value).flatMap(c=>c.cities))].sort((a,b)=>a.localeCompare(b)).forEach(x=>cs.add(new Option(x,x)));cs.value=[...cs.options].some(o=>o.value===keep)?keep:"";};
  const go=()=>render(el,d.clinics.filter(c=>(!f.country.value||c.country===f.country.value)&&(!f.city.value||c.cities.includes(f.city.value))&&(!f.procedure.value||c.procedures.includes(f.procedure.value))));
  f.country.addEventListener("change",fillCities);f.addEventListener("change",go);fillCities();go();});}
initCalc();initPriceTable();initClinics();
