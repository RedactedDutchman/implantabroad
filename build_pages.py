# Helper to (re)generate HTML pages with shared header/footer. Output is plain static HTML; no build step needed to serve.
import json
BASE="https://redacteddutchman.github.io/implantabroad"  # GitHub Pages project URL; internal links are rewritten to /implantabroad/ prefix after build
NAV='''<header><nav><a class="brand" href="/">ImplantAbroad</a><a href="/clinics.html">Clinics</a><a href="/dental-implants-mexico.html">Mexico</a><a href="/dental-implants-costa-rica.html">Costa Rica</a><a href="/dental-implants-argentina.html">Argentina</a><a href="/newsletter.html">Newsletter</a><a href="/get-listed.html">Get listed</a><a href="/methodology.html">Methodology</a></nav></header>'''
FOOT='''<footer><p><strong>Not medical advice.</strong> Prices are published estimates with sources and dates, not quotes. Clinic listings are unverified and not endorsements. Always check your dentist's registration and get a written treatment plan. See <a href="/methodology.html">methodology &amp; disclosures</a>.</p><p>&copy; 2026 ImplantAbroad · Spanish version coming later.</p></footer><script src="/js/app.js"></script>'''
def page(fn,title,desc,body,schema=None):
    sc=f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>' if schema else ""
    open(fn,"w").write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}/{'' if fn=='index.html' else fn}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}/{fn}">
<link rel="stylesheet" href="/css/style.css">{sc}</head><body>{NAV}<main>{body}</main>{FOOT}</body></html>''')
PROC='<option value="single_implant">Single implant</option><option value="all_on_4">Full arch / All-on-4 (per arch)</option><option value="crown">Crown</option><option value="bone_graft">Bone graft</option>'
def faq(qs): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qs]}
def art(h,d): return {"@context":"https://schema.org","@type":"Article","headline":h,"description":d,"dateModified":"2026-10-27","author":{"@type":"Organization","name":"ImplantAbroad"}}

page("index.html","Dental Implant Prices Abroad: US vs Mexico, Costa Rica, Argentina | ImplantAbroad",
"Compare published dental implant prices in the US, Mexico, Costa Rica and Argentina. Every figure has a source and date.",
f'''<h1>Dental implant prices: US vs Mexico, Costa Rica &amp; Argentina</h1>
<p>A price tracker built from published, sourced figures. Every number links to where it came from and carries an "as of" date. These are estimates, not quotes.</p>
<div class="card"><h2>Savings calculator</h2><form id="calc"><label for="procedure">Procedure</label><select id="procedure" name="procedure">{PROC}</select>
<label for="quote">Your US quote (USD)</label><input id="quote" name="quote" type="text" inputmode="decimal" placeholder="e.g. 4500" aria-describedby="quote-msg"><div id="quote-msg" role="alert" style="color:#b91c1c;font-size:.9rem"></div>
<label for="country">Destination</label><select id="country" name="country"><option value="ANY" selected>Any country (show cheapest)</option><option value="MX">Mexico</option><option value="CR">Costa Rica</option><option value="AR">Argentina</option></select>
<button type="submit">Estimate savings</button></form><div id="result" aria-live="polite"></div></div>
<div class="grid"><div class="card"><h3><a href="/dental-implants-mexico.html">Mexico</a></h3>Los Algodones, Tijuana, Cancún.</div><div class="card"><h3><a href="/dental-implants-costa-rica.html">Costa Rica</a></h3>San José, Escazú.</div><div class="card"><h3><a href="/dental-implants-argentina.html">Argentina</a></h3>Buenos Aires, Córdoba.</div></div>
<h2>Guides</h2><ul><li><a href="/dental-implants-cost-mexico-vs-usa.html">Dental implants cost in Mexico vs USA</a></li><li><a href="/dental-implants-argentina-cost.html">Dental implants in Argentina: cost</a></li><li><a href="/is-dental-tourism-safe.html">Is dental tourism safe?</a></li></ul>
<div class="card"><h2>Get price updates</h2><p>A short email when the tracked figures change. <a href="/newsletter.html">Subscribe</a>.</p></div>''',
{"@context":"https://schema.org","@type":"WebSite","name":"ImplantAbroad","url":BASE})

def country(fn,name,code,intro,sections,know):
    page(fn,f"Dental Implants in {name}: Prices, What to Know & Clinics (2026)",f"Published dental implant price ranges in {name} with sources, practical travel and aftercare notes, and a list of clinics (unverified listings).",
f'''<h1>Dental implants in {name}</h1><p>{intro}</p><h2>Published price ranges (USD)</h2><div data-prices="{code}">Loading…</div>
<p class="notice">Ranges combine sources with different inclusions. Ask any clinic for a written, itemised quote.</p>{sections}
<h2>What to know</h2><ul>{know}</ul><h2>Clinics in {name}</h2><p>Websites checked only; not partnered, not endorsed, credentials not verified.</p><div data-clinics="{code}" class="grid"></div>''',
{"@context":"https://schema.org","@type":"WebPage","name":f"Dental implants in {name}","dateModified":"2026-10-27"})
COMMON='''<li><strong>Number of trips:</strong> conventional implants usually need healing time between placing the implant and fitting the final crown, so plan for two trips; clinics state this differently, so ask for the timeline in writing.</li>
<li><strong>Aftercare:</strong> arrange who will see you at home if something goes wrong before you go. The <a href="https://wwwnc.cdc.gov/travel/page/medical-tourism" rel="nofollow">CDC</a> advises planning follow-up care and getting copies of records.</li>
<li><strong>Credentials:</strong> ask for the dentist's licence number and check it with the official registry.</li>'''
country("dental-implants-mexico.html","Mexico","MX","Mexico is the most common US destination, especially border towns like Los Algodones (near Yuma, AZ) and Tijuana (near San Diego), plus Cancún for fly-in patients.",
'''<h3>By city (single implant with abutment + crown, published)</h3><ul><li>Los Algodones: $1,100–$1,550; Tijuana: $1,200–$1,600; Cancún: $1,400–$1,850 – <a href="https://mexicodentalimplantsguide.com/dental-implants-in-mexico-cost/" rel="nofollow">Mexico Dental Implants Guide, 2026</a></li>
<li><strong>Bone grafts:</strong> published Mexico figures ($400–$1,200, <a href="https://mexicodentalimplantsguide.com/dental-implants-in-mexico-cost/" rel="nofollow">MDIG</a>) overlap the published US range ($250–$1,100, <a href="https://dentistrytodayonline.com/dental-implants-cost/" rel="nofollow">Dentistry Today</a>), so these sources show little or no saving on grafts alone.</li><li>Tijuana median $1,610 (17 clinics); Cancún median $1,580 (3 clinics) – <a href="https://toothcation.com/price-index.csv" rel="nofollow">Toothcation price index, Oct 2026</a></li></ul>''',
COMMON+'<li><strong>Mexico checks:</strong> ask for the dentist\'s <em>cédula profesional</em> (searchable on the federal SEP registry) and the clinic\'s COFEPRIS sanitary notice (<a href="https://www.placidway.com/article/4307/dental-implants-in-mexico-cities-costs-comparison" rel="nofollow">source</a>).</li><li><strong>Travel:</strong> check current US State Department travel advisories for the destination state.</li>')
country("dental-implants-costa-rica.html","Costa Rica","CR","Costa Rica clinics cluster in San José and Escazú and serve many North American patients, usually flying into San José (SJO).",
'<p>Bone graft: no reliable published Costa Rica figure found, so it is left out.</p>',COMMON+'<li><strong>Costa Rica checks:</strong> dentists are registered with the Colegio de Cirujanos Dentistas de Costa Rica; ask for the registration number.</li>')
country("dental-implants-argentina.html","Argentina","AR","Argentina is a less common destination for US patients, but prices published by Buenos Aires clinics are in the same range as Mexico. Many clinics quote in USD but charge in pesos.",
'''<h2 id="buenos-aires">Buenos Aires</h2><ul><li>Complete implant with crown: USD 1,000–1,800 (national brand implant USD 500–600, Straumann USD 800–950, crown USD 450–800); All-on-4/6 USD 8,000–12,000 per arch – <a href="https://drablois.com/cuanto-cuesta-un-implante-dental-en-buenos-aires/" rel="nofollow">Consultorios Dra. Blois</a></li>
<li>Implant post only: USD 800–1,000 – <a href="https://amosmile.ar/implantes/" rel="nofollow">AmoSmile</a></li><li>All-in finished implant (incl. extraction/graft): from USD 3,000 (Neodent) / 3,500 (Straumann) – <a href="https://www.amesteticadental.com/en/dental-implants-cost-buenos-aires" rel="nofollow">AM Estética Dental</a></li></ul>
<h2 id="cordoba">Córdoba</h2><p>We only found peso figures: implants "from ARS 500,000" at <a href="https://www.sublimis.com/odontologia-argentina-implantes-dentales.html" rel="nofollow">Sublimis</a>. We do not convert to USD because the exchange rate moves quickly. No USD figure found yet.</p>
<h2 id="other-cities">Other cities (Mendoza, Rosario)</h2><p>No sourced figures yet.</p>''',
COMMON+'<li><strong>Argentina checks:</strong> dentists hold a matrícula (national "M.N." or provincial "M.P."); check it on the national health professionals registry (REFEPS, run by the Ministry of Health).</li><li><strong>Payment:</strong> USD prices are often paid in pesos at a stated rate; confirm which rate.</li>')

page("clinics.html","Dental Implant Clinic Directory: Mexico, Costa Rica, Argentina | ImplantAbroad","Filter dental implant clinics by country, city and procedure. Unverified listings, not endorsements.",
f'''<h1>Clinic directory</h1><p class="notice">Every listing is an <strong>unverified listing – not yet partnered</strong>. We checked that the clinic website exists; we did not verify licences, quality or prices. Inclusion is not an endorsement.</p>
<form id="filters" class="card grid"><div><label for="fc">Country</label><select id="fc" name="country"><option value="" selected>All countries</option><option value="MX">Mexico</option><option value="CR">Costa Rica</option><option value="AR">Argentina</option></select></div>
<div><label for="fci">City</label><select id="fci" name="city"><option value="">All</option></select></div><div><label for="fp">Procedure</label><select id="fp" name="procedure"><option value="">All</option>{PROC}</select></div></form>
<div data-clinics="all" class="grid"></div><p>Clinic? <a href="/get-listed.html">Get listed</a>. Spot an error? Contact: coming soon.</p>''')

page("get-listed.html","Get Your Dental Clinic Listed | ImplantAbroad","Dental clinics in Mexico, Costa Rica and Argentina can request a listing on ImplantAbroad.",
'''<h1>Get your clinic listed</h1><div class="grid"><div class="card"><h3>Free basic listing</h3>Name, city, website, procedures. Marked "unverified".</div>
<div class="card"><h3>Verified listing</h3>We check licence/registration documents you provide and published prices. Pricing: contact us / launching soon.</div><div class="card"><h3>Featured listing</h3>Shown first in your city, clearly labelled "Featured (paid)". Pricing: contact us / launching soon.</div><div class="card"><h3>Per-lead</h3>Pay only for patient enquiries we forward, with patient consent. Pricing: contact us / launching soon.</div></div>
<p>Paid placement never changes the published price ranges and is always disclosed. See <a href="/methodology.html">disclosures</a>.</p>
<div class="card"><p class="notice">Listing requests open soon. Thank you for your interest.</p>
<form action="#" method="POST" onsubmit="return false"><fieldset disabled style="border:0;padding:0;margin:0"><label>Clinic name<input name="clinic" required></label><label>Website<input name="website" type="url" required></label>
<label>Country<select name="country"><option>Mexico</option><option>Costa Rica</option><option>Argentina</option></select></label><label>City<input name="city" required></label><label>Contact email<input name="email" type="email" required></label>
<label>Interested in<select name="plan"><option>Free basic listing</option><option>Verified listing</option><option>Featured listing</option><option>Per-lead</option></select></label><label>Dentist registration numbers (optional)<textarea name="registration"></textarea></label>
<button type="submit">Request listing (opens soon)</button></fieldset></form></div>''')

page("newsletter.html","Dental Implant Price Updates Newsletter | ImplantAbroad","Get an email when published dental implant prices abroad change.",
'''<h1>Price updates newsletter</h1><p>Occasional email when our tracked, sourced figures change. No spam; unsubscribe any time.</p><div class="card"><p class="notice">Signups open soon. Please check back shortly.</p>
<form action="#" method="POST" onsubmit="return false"><fieldset disabled style="border:0;padding:0;margin:0"><label for="em">Email</label><input id="em" name="email" type="email" required><button type="submit">Subscribe (opens soon)</button></fieldset></form></div>''')

page("methodology.html","Methodology, Disclaimer & Disclosures | ImplantAbroad","How ImplantAbroad collects price data, lists clinics, and makes money. Not medical advice.",
'''<h1>Methodology &amp; disclaimer</h1><h2>Not medical advice</h2><p>ImplantAbroad provides price research only. It is not medical or dental advice and makes no guarantees about outcomes, safety or prices. Talk to a licensed dentist about your case.</p>
<h2>Check your dentist's registration</h2><ul><li>Mexico: cédula profesional (SEP registry), clinic COFEPRIS notice.</li><li>Costa Rica: Colegio de Cirujanos Dentistas de Costa Rica.</li><li>Argentina: matrícula nacional/provincial (REFEPS).</li></ul>
<h2>How price data is collected</h2><p>We only use figures published by a named source (cost surveys, price guides, clinic price pages). Each figure in <a href="/data/prices.json">prices.json</a> has a source URL and an "as of" date. Ranges shown are the lowest low and highest high across sources, which mix different inclusions. If we can't find a figure, we leave it out and say so. We do not invent or average-in our own numbers.</p>
<h2>How clinics are listed</h2><p>Clinics in <a href="/data/clinics.json">clinics.json</a> were found via web search and their websites checked to exist. All are marked "unverified listing – not yet partnered". Listing is not endorsement.</p>
<h2>Affiliate / lead disclosure</h2><p>We may in future earn money from clinics through paid featured or verified listings and per-lead fees, and possibly affiliate links. Paid placements will be labelled. Payments never change published price figures. Currently no clinic pays us.</p>
<h2>Corrections</h2><p>Contact: coming soon.</p>''')

page("dental-implants-cost-mexico-vs-usa.html","Dental Implants Cost in Mexico vs USA (2026, Sourced Figures)","Sourced 2026 figures: a complete single implant averages about $4,500 in the US vs roughly $1,100–$1,850 in Mexico.",
'''<h1>Dental implants cost in Mexico vs USA</h1><p>Updated 27 Oct 2026. All figures USD, from the linked sources.</p><div class="tablewrap"><table><tr><th></th><th>USA</th><th>Mexico</th></tr>
<tr><td>Single implant (complete)</td><td>avg $4,507, range $3,760–$5,733 (<a href="https://realdentalcosts.com/en/state-of-us-dental-costs-2026/" rel="nofollow">RealDentalCosts 2026</a>); Aspen Dental avg $4,259, range $3,158–$6,533 (<a href="https://www.aspendental.com/pricing-offers/dental-implants-cost/" rel="nofollow">Aspen</a>)</td><td>$1,200–$1,650 average range (<a href="https://mexicodentalimplantsguide.com/dental-implants-in-mexico-cost/" rel="nofollow">MDIG 2026</a>); Tijuana $1,550–$1,850 (<a href="https://www.medicaltourismco.com/dental-work-in-tijuana-cost-quality-and-reviews/" rel="nofollow">MedicalTourismCo</a>)</td></tr>
<tr><td>All-on-4 per arch</td><td>avg $15,179, range $11,642–$27,505 (RealDentalCosts, labelled estimate)</td><td>$8,500–$11,000 (MDIG); Los Algodones median $8,900, Tijuana $9,500 (<a href="https://toothcation.com/price-index.csv" rel="nofollow">Toothcation, Oct 2026</a>)</td></tr>
<tr><td>Crown</td><td>avg $1,369 (RealDentalCosts citing ASQ360/CareCredit)</td><td>Zirconia crown median $450 Cancún/Los Algodones, $500 Tijuana (Toothcation)</td></tr></table></div>
<p>Note: CareCredit reports a lower US average ($2,143) for the implant procedure alone, not the full restoration (<a href="https://www.carecredit.com/well-u/health-wellness/single-tooth-implant/" rel="nofollow">CareCredit</a>). Compare like with like.</p>
<h2>Costs not in these numbers</h2><p>Flights, lodging, a likely second trip, and any follow-up at home. Many sources marketing Mexico are clinics or lead-gen sites, so treat their "savings %" claims with care.</p><p><a href="/">Try the calculator</a> · <a href="/dental-implants-mexico.html">Mexico guide &amp; clinics</a></p>''',
art("Dental implants cost in Mexico vs USA","Sourced 2026 price comparison"))

page("dental-implants-argentina-cost.html","Dental Implants in Argentina: Cost in 2026 (Buenos Aires, Córdoba)","What Buenos Aires and Córdoba clinics publish for dental implant prices in 2026, with sources.",
'''<h1>Dental implants in Argentina: cost</h1><p>Updated 27 Oct 2026. Few independent surveys exist; the figures below are published by clinics themselves.</p><ul>
<li>Buenos Aires, complete implant with crown: <strong>USD 1,000–1,800</strong>; All-on-4/6 <strong>USD 8,000–12,000 per arch</strong>; grafts/sinus lift +USD 300–1,500; 3D CT about USD 100 (<a href="https://drablois.com/cuanto-cuesta-un-implante-dental-en-buenos-aires/" rel="nofollow">Dra. Blois</a>).</li>
<li>Buenos Aires, implant only: USD 800–1,000 (<a href="https://amosmile.ar/implantes/" rel="nofollow">AmoSmile</a>).</li>
<li>Buenos Aires, all-in incl. extraction/graft and crown: from USD 3,000–3,500; full-mouth USD 24,000–30,000 (<a href="https://www.amesteticadental.com/en/dental-implants-cost-buenos-aires" rel="nofollow">AM Estética Dental</a>).</li>
<li>Buenos Aires, implants ARS 480,000–1,200,000 depending on brand (<a href="https://soluciondental.com.ar/tratamientos/implantes-dentales-precios-caba/" rel="nofollow">Solución Dental</a>).</li>
<li>Córdoba: from ARS 500,000 (<a href="https://www.sublimis.com/odontologia-argentina-implantes-dentales.html" rel="nofollow">Sublimis</a>). No USD figure found.</li></ul>
<p>The huge spread (USD 1,000 vs 3,000+) is mostly about what is included. Argentine prices change frequently with inflation and imported materials, as one clinic notes.</p><p><a href="/dental-implants-argentina.html">Argentina guide &amp; clinics</a></p>''',
art("Dental implants in Argentina cost","Sourced 2026 prices"))

page("is-dental-tourism-safe.html","Is Dental Tourism Safe? What Official Sources Say","What the CDC, ADA and UK GDC say about getting dental work abroad, and checks to make before you go.",
'''<h1>Is dental tourism safe?</h1><p>There's no yes/no answer and we can't give one. Here's what official bodies say:</p><ul>
<li>The <a href="https://wwwnc.cdc.gov/travel/page/medical-tourism" rel="nofollow">CDC</a> lists risks of medical tourism including infections (including antibiotic-resistant ones), differing provider standards, and complications on flying after procedures, and advises seeing a provider at home first and planning follow-up care. See also the <a href="https://www.cdc.gov/yellow-book/hcp/health-care-abroad/medical-tourism.html" rel="nofollow">CDC Yellow Book</a>.</li>
<li>The ADA's consumer site <a href="https://www.mouthhealthy.org/all-topics-a-z/travel" rel="nofollow">MouthHealthy</a> has travel guidance, and the ADA ethics council has published a <a href="https://www.ada.org/-/media/project/ada-organization/ada/ada-org/files/about/principles/cebja-statements-and-white-papers/2026/dental-tourism_01_2025.pdf?hash=BEDFAF12986C7FBF69A40B3C75FA7BC6&amp;rev=e2dc5d6afd8e4a2f8fae9c582bd05781" rel="nofollow">statement on dental tourism</a>.</li>
<li>The UK General Dental Council has a guide, <a href="https://www.gdc-uk.org/docs/default-source/going-abroad-for-dental-treatment/going-abroad-for-your-dental-care.pdf?sfvrsn=c67e2b57_4" rel="nofollow">Going abroad for your dental care</a>.</li></ul>
<h2>Checks before you book</h2><ul><li>Verify the dentist's licence in the official registry (see <a href="/methodology.html">methodology</a>).</li><li>Get a written, itemised treatment plan and timeline.</li><li>Ask what happens, and who pays, if something fails.</li><li>Arrange a dentist at home for follow-up.</li><li>Bring copies of X-rays/CT scans and records home.</li></ul>
<p class="notice">This page summarises public sources. It is not medical advice and does not guarantee any outcome.</p>''',
faq([("Is dental tourism safe?","It depends on the provider and planning. The CDC lists risks such as infections and differing standards and recommends planning follow-up care. This is not medical advice.")]))

pages=["","clinics.html","dental-implants-mexico.html","dental-implants-costa-rica.html","dental-implants-argentina.html","get-listed.html","newsletter.html","methodology.html","dental-implants-cost-mexico-vs-usa.html","dental-implants-argentina-cost.html","is-dental-tourism-safe.html"]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{BASE}/{p}</loc><lastmod>2026-10-27</lastmod></url>\n" for p in pages)+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
