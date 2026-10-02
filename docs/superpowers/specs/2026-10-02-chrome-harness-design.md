# Chrome Harness Design — 2026-10-02

## Purpose
Phone-harness-style control for visible desktop Chrome on Linux (`DISPLAY=:0`, Wayland), with full profile support. User asked for every phone-harness feature (click, fill, every task) plus Chrome extras.

## Architecture (approved)
- CLI `chrome-harness` at `~/.local/bin/chrome-harness`, invoked as heredoc: `chrome-harness <<'PY'` with helpers pre-imported.
- Talks to the user's running Chrome via CDP on `localhost:9222`. One-time Chrome relaunch with `--remote-debugging-port=9222` required; never kill silently.
- Skill at `~/.config/opencode/skills/chrome-harness/SKILL.md` (<500 lines), scripts under `scripts/`.
- Mirrors phone-harness working method: `# task:` + `# step:` comments, tell user before/after each script, one action then verify.

## Components (approved)
- Profiles: `list_profiles()` (from `~/.config/google-chrome/Local State`), `open_profile("Profile 16", url)`, `current_profile()`. Verified: 10 profiles incl. `Profile 16 -> ggs`.
- Eyes: `snapshot(-i)` with refs `@e1`, `get_text()`, `screenshot()`, `console()`, `errors()`, `network()`, `health()`, `eval(js)`, `style(selector)`.
- Hands: `click()`, `fill()`, `type_text()` (needs focused field), `press()`, `keydown/keyup` chords, `hover()`, `scroll(direction)`, `back/forward/reload()`, `new_tab/close_tab/focus_tab()`, `get_url/get_title()`.
- Walk: `scroll_until(pred)`, `scroll_collect(extract)` for infinite lists.
- Safety: consent gate for send/post/delete/settings change; never auto-type PIN/password/2FA; `connection_state()` reports `ready/no-chrome/no-debug-port/profile-locked`.

## Data flow + errors (approved)
- Flow: heredoc PY -> helpers -> CDP websocket -> visible Chrome -> fresh `snapshot()` + `console()` check -> print observation. Batch only proven sequences.
- Errors: `no-chrome` relay launch cmd; `no-debug-port` relay relaunch cmd; `profile-locked` reuse window (SingletonLock); `target-gone` re-list tabs.

## Location + tests (approved)
- Skill: `~/.config/opencode/skills/chrome-harness/`; CLI: `~/.local/bin/chrome-harness`.
- Tests: (1) open Profile 16 to `https://console.firebase.google.com/` + list tabs, (2) form fill + submit verified by URL change, (3) Ctrl+T, type URL, screenshot.

## Out of scope v1
- iPhone Mirroring, cloud phones (stay in phone-harness). Headless-only flows (stay in agent-browser). No password vaulting.
