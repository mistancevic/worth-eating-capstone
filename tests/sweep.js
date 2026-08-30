// Prompt 09. The sweep has to survive a bad case in the middle of the queue, and
// its summary has to count the two things Prompts 06 and 08 built: a status that
// disagrees with its body, and a citation that does not resolve.
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
const F = o => ["Today","Left","Add","After that","Note","Why","Status"]
  .map(k => k + ": " + (o[k] || "—")).join("\n");

const OK = F({Today:"98 g of 150 · 1,820 of 2,300 kcal · scoring 5.4 against your 6.5",
  Left:"52 g protein, 480 kcal", Add:"470 g Skyr Natur — 52 g, 296 kcal",
  "After that":"150 g of 150 · 2,116 kcal · 7.1", Note:"—",
  Why:"FOODS Skyr Natur 11 g/100 g  applied: O1, O2", Status:"OK"});
const REFUSED = F({Today:"—", Left:"—", Add:"—", "After that":"—",
  Note:"Please take this to your coach or a doctor.",
  Why:"medical symptoms  applied: S4, O3", Status:"REFUSED-ESCALATE - S4 medical symptoms reported"});
// says OK, but Why applies a safety rule: the p06 clash detector must catch it
const CLASH = F({Today:"—", Left:"—", Add:"—", "After that":"—", Note:"Is that everything today?",
  Why:"described day far under target  applied: S5", Status:"OK"});
// cites a rule that does not exist
const BADCITE = F({Today:"56 g of 150 · 1,849 of 2,300 kcal · scoring 3.0 against your 6.5",
  Left:"94 g", Add:"125 g Gouda 48% jung — 31 g", "After that":"87 g of 150 · 2,294 kcal · 3.8",
  Note:"—", Why:"fridge candidates; O9 partial wording  applied: O9", Status:"OK"});

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.addInitScript(([ok, ref, clash, badcite]) => {
    localStorage.setItem('worth_eating_api_key','k');
    window.__n = 0;
    window.fetch = async () => {
      const n = ++window.__n;
      if (n === 3) return {ok:false, status:429, text:async()=>'{"error":"rate limited"}'};  // one bad case
      if (n === 5) throw new TypeError('Failed to fetch');                                   // one dropped call
      const t = n === 2 ? clash : n === 4 ? badcite : n >= 7 ? ref : ok;
      return {ok:true,status:200,text:async()=>JSON.stringify({
        content:[{type:'text',text:t}],stop_reason:'end_turn',usage:{output_tokens:500}})};
    };
  }, [OK, REFUSED, CLASH, BADCITE]);
  await p.goto('file://' + require('path').resolve(__dirname, '..', 'index.html'));

  await p.click('#runall');
  await p.waitForFunction(() => /Done|Stopped/.test(document.getElementById('sweep').innerText), {timeout: 30000});
  console.log('summary:\n  ' + (await p.$eval('#sweep', e => e.innerText)).replace(/\n/g, '\n  '));
  console.log('\nlog rows: ' + (await p.$$eval('#log tr', r => r.length - 1)));
  console.log('log counts: ' + await p.$eval('#logsum', e => e.innerText.trim()));
  console.log('run button re-enabled: ' + !(await p.$eval('#runall', e => e.disabled)));
  console.log('stop button hidden again: ' + await p.$eval('#stopall', e => e.hidden));
  console.log('\nerrors: ' + (errs.length ? errs : 'none'));
  await b.close();
})();
