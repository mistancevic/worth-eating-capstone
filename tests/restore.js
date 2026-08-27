const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
const reply = (status, add) => [
  "Today: 98 g of 150 · 1,820 of 2,300 kcal · scoring 5.4 against your 6.5",
  "Left: 52 g protein, 480 kcal", "Add: " + add,
  "After that: 150 g of 150 · 2,116 kcal · 7.1",
  "Note: Fibre comes to around 22 g of your 32 today.",
  "Why: FOODS Skyr Natur 11 g/100 g; fit check 4/4  applied: O2, O3",
  "Status: " + status].join("\n");


// Read the panel by label, never by position: a field the headline consumed
// is not rendered, so index 2 is not always Add.
const fieldMap = async (p, eve) => p.$eval('#out-'+eve+' dl.fields', dl => {
  const m = {}; const kids = [...dl.children];
  for (let i = 0; i < kids.length; i += 2) m[kids[i].innerText.trim()] = kids[i+1].innerText.trim();
  return m;
});
const panelText = async (p, eve) => p.$eval('#out-'+eve, e => e.innerText.replace(/\s+/g,' '));

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
  await p.addInitScript(([r]) => {
    localStorage.setItem('worth_eating_api_key', 'sk-ant-stub');
    window.fetch = async () => ({ ok: true, status: 200, text: async () => JSON.stringify({
      content: [{type:'text', text: r}], stop_reason:'end_turn', usage:{output_tokens: 900}})});
  }, [reply('OK','470 g Skyr Natur — 52 g, 296 kcal')]);
  await p.goto('file://' + require('path').resolve(__dirname, '..', 'index.html'));

  const run = async e => { await p.click(`button.run[data-id="${e}"]`);
                           await p.waitForSelector(`#out-${e} .gate button`, {timeout: 8000}); };
  const gate = async (e,l) => { for (const x of await p.$$(`#out-${e} .gate button`))
      if ((await x.innerText()).trim() === l) return x.click();
    throw new Error('no ' + l + ' on ' + e); };

  await run('EVE-01');                       // leave it pending
  await run('EVE-01');                       // re-run: the first must go to "replaced"
  await gate('EVE-01','Edit');
  await p.fill('#out-EVE-01 textarea[data-f="Note"]', 'reviewer changed this line');
  await gate('EVE-01','Save');

  const before = await p.$$eval('#log tr', rs => rs.map(r => [...r.children].map(c=>c.innerText.trim()).join(' | ')));
  console.log('--- before reload ---'); before.forEach(l => console.log(l));
  console.log('summary:', await p.$eval('#logsum', e => e.innerText.trim()));

  await p.reload();
  await p.waitForSelector('#log tr');
  const after = await p.$$eval('#log tr', rs => rs.map(r => [...r.children].map(c=>c.innerText.trim()).join(' | ')));
  console.log('\n--- after reload ---'); after.forEach(l => console.log(l));
  console.log('summary:', await p.$eval('#logsum', e => e.innerText.trim()));
  const panel = await p.$('#out-EVE-01 .verdict');
  console.log('panel restored with a verdict badge:', panel ? (await panel.innerText()).trim() : 'NO');
  const whole = await panelText(p, 'EVE-01');
  console.log('edit survived the reload:', whole.includes('reviewer changed this line'));
  console.log('fields shown:', JSON.stringify(Object.keys(await fieldMap(p, 'EVE-01'))));
  console.log('\nerrors:', errs.length ? errs : 'none');
  await b.close();
})();
