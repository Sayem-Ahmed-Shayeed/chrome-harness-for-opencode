# chrome-harness for OpenCode

Phone-harness-style control of your **visible desktop Chrome** — open a specific profile, read pages, click, fill forms — driven by small Python scripts, built for [OpenCode](https://opencode.ai) agents (and humans).

```bash
chrome-harness <<'PY'
# task: check Reserve Bank Cargo Tracking in Profile 20
# step: confirm connection, then list tabs
print(state())
for t in tabs()[:5]:
    print(t.get("title"), "-", t.get("url"))
PY
```

## What it does (v1)

- **Profiles** — `list_profiles()` (reads Chrome's `Local State`), `open_profile("Profile 16", url)`, `current_profile()`
- **Tabs** — list, open URL, close, navigate
- **Eyes** — `snap()` (interactive elements with `@e1` refs), `text()`, `shot(path)`, `js(expr)`, `errors_of()` (console/JS errors)
- **Hands** — `nav()`, `click_xy()`, `fill_js()`, `press_key()` (with Enter/Tab/Escape key codes)
- **Two interfaces** — heredoc Python with pre-imported helpers (like `phone-harness`), plus one-shot subcommands: `state`, `tabs`, `profiles`, `open`

## Requirements

- Linux with Google Chrome + Python 3.10+
- **One-time step:** relaunch Chrome with the debug flag so the harness can talk to it:
  `google-chrome --remote-debugging-port=9222`
  `chrome-harness state` must print `ready`. Without the flag it prints `no-debug-port` — the harness will never kill or relaunch your Chrome for you.

## Install

```bash
git clone https://github.com/Sayem-Ahmed-Shayeed/chrome-harness-for-opencode.git
cd chrome-harness-for-opencode
pip install -e .
```

## Usage

```bash
chrome-harness state                              # ready | no-debug-port
chrome-harness profiles                           # Profile 16 -> ggs ...
chrome-harness open "Profile 16" --url "https://console.firebase.google.com/"
echo | chrome-harness state                       # subcommands work piped too

chrome-harness <<'PY'
# task: read the visible page
# step: snapshot refs + text + error check
print(snap()[:5])
print(text()[:500])
print(errors_of())
PY
```

Act → verify → adapt: do one thing, then take a fresh `snap()` plus `errors_of()`. Check `SKILL.md` for the full agent working method.

## Safety rules

- Stop and ask before anything outward-facing or hard to reverse (send, post, delete, settings changes).
- Never auto-type a PIN, password, or 2FA code.
- The harness only drives Chrome — it never kills, updates, or relaunches your browser.

## Status

v1 implemented with per-task spec + quality reviews, 14 tests passing (`pytest tests/ -q`), fresh-clone install verified. Deferred to v2: `scroll_until`/`scroll_collect`, `hover`, key chords, `network()` waterfall, `health()` aggregate.

## Layout

```
chrome_harness/   connection.py profiles.py eyes.py hands.py cli.py
tests/            test_connection.py test_profiles.py test_eyes.py test_hands.py test_cli.py
SKILL.md          agent working method (mirrors phone-harness)
docs/             design spec + implementation plan
```
