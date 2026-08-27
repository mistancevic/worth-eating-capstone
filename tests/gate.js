// Drives the p07 gate against a stubbed API. No key, no network, no cost.
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');

const reply = (status, add) => [
  "Today: 98 g of 150 · 1,820 of 2,300 kcal · scoring 5.4 against your 6.5",
  "Left: 52 g protein, 480 kcal",
  "Add: " + add,
  "After that: 150 g of 150 · 2,116 kcal · 7.1",
  "Note: Fibre comes to around 22 g of your 32 today.",
  "Why: FOODS Skyr Natur 11 g/100 g; fit check 4/4  applied: O2, O3",
  "Status: " + status
].join("\n");


// Read the panel by label, never by position: a field the headline consumed
// is not rendered, so index 2 is not always Add.
const fieldMap = async (p, eve) => p.$eval('#out-'+eve+' dl.fields', dl => {
  const m = {}; const kids = [...dl.children];
  for (let i = 0; i < kids.length; i += 2) m[kids[i].innerText.trim()] = kids[i+1].innerText.trim();
  return m;
});
const panelText = async (p, eve) => p.$eval('#out-'+eve, e => e.innerText.replace(/\s+/g,' '));

(async () => {
  const b = await browser();
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });

  await p.addInitScript(() => {
    localStorage.setItem('worth_eating_api_key', 'sk-ant-stub');
    window.__n = 0;
    window.fetch = async () => {
      const n = ++window.__n;
      const bodies = [window.__r1, window.__r2, window.__r3];
      return { ok: true, status: 200, text: async () => JSON.stringify({
        content: [{type:'thinking',thinking:'...'},{type:'text',text: bodies[(n-1)%3]}],
        stop_reason: 'end_turn', usage: {output_tokens: 1234}
      })};
    };
  });
  await p.goto('file://' + require('path').resolve(__dirname, '..', 'index.html'));
  await p.evaluate(([a,c,e]) => { window.__r1=a; window.__r2=c; window.__r3=e; },
    [reply('OK','470 g Skyr Natur — 52 g, 296 kcal'),
     reply('OK','470 g Skyr Natur — 52 g, 296 kcal'),
     reply('HELD - S5 apparent intake far below requirement','—')]);

  const keyname = await p.evaluate(() => Object.keys(localStorage));
  console.log('localStorage keys seen by page:', JSON.stringify(keyname));

  const run = async (eve) => {
    await p.click(`button.run[data-id="${eve}"]`);
    await p.waitForSelector(`#out-${eve} .gate button`, {timeout: 8000}).catch(async () => { console.log('OUT HTML:', (await p.$eval('#out-'+eve, e=>e.innerHTML)).slice(0,900)); throw new Error('no gate on '+eve); });
  };
  const gate = async (eve, label) => {
    const btns = await p.$$(`#out-${eve} .gate button`);
    for (const btn of btns) if ((await btn.innerText()).trim() === label) { await btn.click(); return true; }
    throw new Error(`no "${label}" button on ${eve}`);
  };

  // 1. approve
  await run('EVE-01'); await gate('EVE-01','Approve');

  // 2. edit
  await run('EVE-02'); await gate('EVE-02','Edit');
  await p.fill('#out-EVE-02 textarea[data-f="Add"]', '300 g Magerquark — 36 g, 201 kcal');
  await gate('EVE-02','Save');

  // 3. escalate, first with no reason (must refuse), then with one
  await run('EVE-03'); await gate('EVE-03','Escalate');
  await gate('EVE-03','Escalate');            // empty box: should not decide
  let stillOpen = await p.$('#out-EVE-03 .escbox input');
  console.log('empty reason rejected:', !!stillOpen);
  await p.fill('#out-EVE-03 .escbox input', 'coach should see this one, he said "dizzy" last week');
  await gate('EVE-03','Escalate');

  // 4. re-run EVE-01 without reviewing, to exercise "replaced"
  await run('EVE-01');

  // 5. reopen the edited one
  await gate('EVE-02','Reopen');

  const log = await p.$$eval('#log tr', rs => rs.map(r =>
    [...r.children].map(c => c.innerText.trim()).join(' | ')));
  const sum = await p.$eval('#logsum', e => e.innerText.trim());
  const shown = await p.$eval('#out-EVE-02 dd', e => e.innerText.trim());
  console.log('\n--- run log ---'); log.forEach(l => console.log(l));
  console.log('\nsummary:', sum);

  // the edit must survive the redraw
  const m = await fieldMap(p, 'EVE-02');
  const whole = await panelText(p, 'EVE-02');
  console.log('EVE-02 fields shown:', JSON.stringify(Object.keys(m)));
  console.log('edit survived (Add text somewhere in panel):',
    whole.includes('300 g Magerquark'));

  console.log('\nerrors:', errs.length ? errs : 'none');
  await b.close();
})();

async function browser() {
  const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
  return chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
}
