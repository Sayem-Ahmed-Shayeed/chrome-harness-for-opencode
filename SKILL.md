---
name: chrome-harness
description: Use when controlling the user's visible desktop Chrome — open a specific profile, navigate tabs, snapshot page refs, click, fill forms, read console errors, or screenshot. Use for any visible-Chrome automation instead of headless tools.
---

# chrome-harness

Phone-harness-style control of visible desktop Chrome via CDP. Same habits: `# task:` + `# step:`, tell the user before/after each script, one action then verify with a fresh `snap()`.

## Requires

One-time: relaunch Chrome with `--remote-debugging-port=9222`. `chrome-harness state` must print `ready`; on `no-debug-port` relay the relaunch command and stop — never kill Chrome.

## Working method

```bash
chrome-harness <<'PY'
# task: open ggs profile to firebase console
# step: list tabs to confirm connection
print(state(), tabs()[:2])
PY
```

- Read with `snap()` refs (`@e1`), not screenshots. `text()` for content, `shot()` only for visuals.
- Act, verify, adapt: one call, then fresh `snap()` + `errors_of()`. Never batch unverified steps.
- `fill_js(selector, text)` needs the element present — check `snap()` first.
- Consent: stop and ask before send/post/delete/settings; never type passwords/2FA.
