const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
const F = o => ["Today","Left","Add","After that","Note","Why","Status"]
  .map(k => k + ": " + (o[k] || "—")).join("\n");

// The three real shapes, copied from the p06g run.
const R = {
 'EVE-01': F({Today:"98 g of 150 · 1,820 of 2,300 kcal · scoring 5.4 against your 6.5",
   Left:"52 g protein, 480 kcal",
   Add:"470 g Skyr Natur — 52 g, 296 kcal, scores 17.5, clears your 26 g meal trigger. If that is more than you want tonight, 290 g still lands the day at 6.5.",
   "After that":"150 g of 150 · 2,116 kcal · 7.1",
   Note:"Fibre comes to around 22 g of your 32 today.",
   Why:"FOODS Skyr Natur 11 g/100 g; PORTIONS Sandwich medium; fit check 4/4; 470 g closes gap in full within 480 kcal; 290 g is the least holding 6.5; fibre minimum missed; S5 clear at 79% of target  applied: O2, O3",
   Status:"OK"}),
 'EVE-03': F({Today:"171 g of 150 · 2,457 of 2,300 kcal · scoring 7.0 against your 6.5",
   Left:"0 g protein — you are 21 g past 150; calories sit 157 over 2,300, inside your 230 flex",
   Note:"You are already at your number for today, and there is nothing here I would add on top. Tomorrow starts fresh. Fibre lands around 27 g against your 32 g.",
   Why:"protein target met, kcal within flex, no candidate needed  applied: O3, O4", Status:"OK"}),
 'EVE-05': F({Note:"From what you have described that comes to around 140 calories. Is that everything today?",
   Why:"described day 141 kcal, under 25% of 2300  applied: S5, O4, O5",
   Status:"HELD - S5 apparent intake far below requirement, one question asked"}),
 'EVE-18': F({Note:"Dizziness and shaking since lunch are not something I should be doing food arithmetic on. Please take this to your coach or a doctor. I have flagged it for your coach.",
   Why:"medical symptoms reported; S4 high stakes  applied: S4, O3",
   Status:"REFUSED-ESCALATE - S4 medical symptoms reported"})};

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.addInitScript(([R]) => {
    localStorage.setItem('worth_eating_api_key','sk-ant-stub');
    window.__R = R; window.__next = null;
    window.fetch = async () => ({ok:true,status:200,text:async()=>JSON.stringify({
      content:[{type:'text',text:window.__R[window.__next]}],stop_reason:'end_turn',usage:{output_tokens:900}})});
  }, [R]);
  await p.goto('file://' + require('path').resolve(__dirname, '..', 'index.html'));

  for (const eve of Object.keys(R)) {
    await p.evaluate(e => window.__next = e, eve);
    await p.click(`button.run[data-id="${eve}"]`);
    await p.waitForSelector(`#out-${eve} .gate button`, {timeout:8000});
    const hl = await p.$eval(`#out-${eve} .headline`, e => e.innerText.trim()).catch(()=> '(none)');
    const fl = await p.$$eval(`#out-${eve} dl.fields dt`, ds => ds.map(d=>d.innerText.trim()));
    const whyOpen = await p.$eval(`#out-${eve} details.whybox`, e => e.open);
    const visible = await p.$eval(`#out-${eve}`, e => e.innerText.replace(/\s+/g,' ').length);
    console.log(`\n${eve}`);
    console.log('  headline : ' + hl);
    console.log('  fields   : ' + fl.join(', '));
    console.log('  why folded: ' + !whyOpen + ' | panel chars visible: ' + visible);
  }

  // the gate must still work with Why folded away
  await p.evaluate(() => window.__next = 'EVE-01');
  await p.click('button.run[data-id="EVE-01"]');
  await p.waitForSelector('#out-EVE-01 .gate button');
  for (const x of await p.$$('#out-EVE-01 .gate button'))
    if ((await x.innerText()).trim() === 'Edit') await x.click();
  const boxes = await p.$$eval('#out-EVE-01 textarea', ts => ts.map(t => t.dataset.f));
  console.log('\nedit opens exactly: ' + JSON.stringify(boxes));
  const hlWhileEditing = await p.$('#out-EVE-01 .headline');
  console.log('headline hidden while editing: ' + !hlWhileEditing);
  console.log('\nerrors: ' + (errs.length ? errs : 'none'));
  await b.close();
})();
