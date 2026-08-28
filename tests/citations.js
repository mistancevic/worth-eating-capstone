// Prompt 08. Every reply here is a fake, on purpose: the point is not whether
// the agent cites well, it is whether the page can tell a real citation from an
// invented one. A suite that only ever sees good replies proves nothing.
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
const F = o => ["Today","Left","Add","After that","Note","Why","Status"]
  .map(k => k + ": " + (o[k] || "—")).join("\n");

const REPLIES = {
  // honest: every reference resolves
  'EVE-01': F({Today:"98 g of 150 · 1,820 of 2,300 kcal · scoring 5.4 against your 6.5",
    Left:"52 g protein, 480 kcal",
    Add:"470 g Skyr Natur — 52 g, 296 kcal, scores 17.5, clears your 26 g meal trigger",
    "After that":"150 g of 150 · 2,116 kcal · 7.1", Note:"—",
    Why:"PORTIONS Sandwich medium; FOODS Skyr Natur 11 g/100 g, Banane unit_g 120; fit check 4/4  applied: O1, O2",
    Status:"OK"}),
  // invented rule identifiers that do not exist in either policy file
  'EVE-02': F({Today:"—", Left:"—", Add:"—", "After that":"—",
    Note:"I do not have numbers for that.",
    Why:"unknown product; S7 unknown-product rule; O9 partial-day wording  applied: S7, O9",
    Status:"HELD - S7 named product with no row in FOODS"}),
  // a food that is not in foods.csv, named in Add
  'EVE-04': F({Today:"56 g of 150 · 1,849 of 2,300 kcal · scoring 3.0 against your 6.5",
    Left:"94 g protein, 451 kcal",
    Add:"200 g Hüttenkäse Light — 24 g protein, 130 kcal",
    "After that":"80 g of 150 · 1,979 kcal · 4.0", Note:"—",
    Why:"fridge candidates considered; fit check 3/4  applied: O2",
    Status:"OK"}),
  // the substring trap: Tomatensauce must not also score a hit for Tomaten
  'EVE-05': F({Today:"—", Left:"—", Add:"—", "After that":"—",
    Note:"Is that everything today?",
    Why:"FOODS Tomatensauce 50 kcal/100 g; described day far under target  applied: S5",
    Status:"HELD - S5 apparent intake far below requirement"}),
};

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.addInitScript(([R]) => {
    localStorage.setItem('worth_eating_api_key','k'); window.__R = R;
    window.fetch = async () => ({ok:true,status:200,text:async()=>JSON.stringify({
      content:[{type:'text',text:window.__R[window.__next]}],stop_reason:'end_turn',usage:{output_tokens:700}})});
  }, [REPLIES]);
  await p.goto('file://' + require('path').resolve(__dirname, '..', 'index.html'));

  for (const eve of Object.keys(REPLIES)) {
    await p.evaluate(e => window.__next = e, eve);
    await p.click(`button.run[data-id="${eve}"]`);
    await p.waitForSelector(`#out-${eve} .gate button`, {timeout: 8000});
    const tags = await p.$$eval(`#out-${eve} .cite`,
      cs => cs.map(c => (c.classList.contains('bad') ? '✗ ' : '✓ ') + c.innerText.trim()));
    const warn = await p.$eval(`#out-${eve} .cites .err`, e => e.innerText.trim()).catch(()=> '');
    console.log('\n' + eve);
    console.log('  ' + tags.join('   '));
    if (warn) console.log('  ' + warn.replace(/\s+/g,' '));
  }
  console.log('\nerrors: ' + (errs.length ? errs : 'none'));
  await b.close();
})();
