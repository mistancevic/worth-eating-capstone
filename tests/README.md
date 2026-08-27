# Browser tests

Three scripts that drive `index.html` in a real Chromium with `window.fetch`
stubbed. No API key, no network, no cost, so they can be run as often as you
like and they never hit the model.

They exist because Prompt 07 added the first real interaction in the product.
Up to p06g the page was a form and a fetch, and reading it was enough. A gate
with five states, an editable panel and a log that has to agree with it is not
something to check by eye on a phone.

```
node tests/gate.js       # approve, edit, save, escalate, reopen, replaced
node tests/restore.js    # a re-run marks the old row replaced; a reload restores both
node tests/headline.js   # the headline picks the right sentence on all four reply shapes
node tests/followup.js   # the finished day asks, the answer goes back as a second turn,
                         # and a refusal is never offered a reply box
```

Each prints what it found and ends with `errors: none`. Read the output; there
are no assertions, on purpose. A test that only says PASS tells you nothing
about a layout, and every one of these is really a question about what ends up
on screen.

One rule learned the hard way on 2026-08-27: **select fields by their label,
never by position.** A field the headline has consumed is not rendered at all,
so `dd[2]` is not always `Add`. Both suites broke on exactly that when the
headline landed, and the app was fine.
