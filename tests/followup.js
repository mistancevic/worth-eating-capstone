const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
const F = o => ["Today","Left","Add","After that","Note","Why","Status"]
  .map(k => k + ": " + (o[k] || "—")).join("\n");

const first = F({Today:"171 g of 150 · 2,457 of 2,300 kcal · scoring 7.0 against your 6.5",
  Left:"0 g protein remaining — you are 21 g past 150; calories are 157 over 2,300, inside your 230 flex",
  Note:"You are at your number for today, so there is nothing you need to add. Still hungry?",
  Why:"protein target met; O4 finished-day wording  applied: O3, O4", Status:"OK"});
const second = F({Today:"171 g of 150 · 2,457 of 2,300 kcal · scoring 7.0 against your 6.5",
  Left:"73 kcal of room before the edge of your flex",
  Add:"Gurke, 300 g, 36 kcal — that is half the room you have left.",
  "After that":"171 g of 150 · 2,493 kcal · 6.9",
  Note:"—", Why:"FOODS Gurke 12 kcal/100 g, max 300 g  applied: O1, O4", Status:"OK"});
const refusal = F({Note:"Dizziness and shaking are not something I should be doing food arithmetic on. Please take this to your coach or a doctor.",
  Why:"S4 high stakes  applied: S4, O3", Status:"REFUSED-ESCALATE - S4 medical symptoms reported"});

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.addInitScript(([a,c,d]) => {
    localStorage.setItem('worth_eating_api_key','k');
    window.__q = [a]; window.__2 = c; window.__ref = d; window.__n = 0;
    window.fetch = async (u, o) => {
      const body = JSON.parse(o.body);
      window.__lastTurns = body.messages.map(m => m.role);
      const t = window.__mode === 'refusal' ? window.__ref
              : (body.messages.length > 1 ? window.__2 : window.__q[0]);
      return {ok:true,status:200,text:async()=>JSON.stringify({
        content:[{type:'text',text:t}],stop_reason:'end_turn',usage:{output_tokens:800}})};
    };
  }, [first, second, refusal]);
  await p.goto('file://' + require('path').resolve(__dirname, '..', 'index.html'));

  // 1. the finished day asks, and a reply box appears
  await p.click('button.run[data-id="EVE-03"]');
  await p.waitForSelector('#out-EVE-03 .gate button');
  console.log('reply box on the finished day :', !!(await p.$('#out-EVE-03 .replybox input')));
  console.log('headline                      :', await p.$eval('#out-EVE-03 .headline', e=>e.innerText.trim()));

  // 2. answer it
  await p.fill('#out-EVE-03 .replybox input', 'yes, still hungry');
  await p.click('#out-EVE-03 .replybox button');
  await p.waitForSelector('#out-EVE-03 .gate button');
  console.log('turns sent on the follow-up   :', JSON.stringify(await p.evaluate(()=>window.__lastTurns)));
  console.log('panel says what he said       :', await p.$eval('#out-EVE-03 .followed', e=>e.innerText.trim()));
  console.log('new headline                  :', await p.$eval('#out-EVE-03 .headline', e=>e.innerText.trim()));
  console.log('reply box gone once answered  :', !(await p.$('#out-EVE-03 .replybox input')));

  // 3. a refusal must NOT offer a box
  await p.evaluate(() => window.__mode = 'refusal');
  await p.click('button.run[data-id="EVE-18"]');
  await p.waitForSelector('#out-EVE-18 .gate button');
  console.log('reply box on a refusal        :', !!(await p.$('#out-EVE-18 .replybox input')), '(must be false)');

  const log = await p.$$eval('#log tr', rs => rs.map(r => [...r.children].map(c=>c.innerText.trim()).join(' | ')));
  console.log('\n--- run log ---'); log.forEach(l => console.log(l));
  console.log('\nerrors:', errs.length ? errs : 'none');
  await b.close();
})();
