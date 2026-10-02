"""chrome-harness entry point: heredoc PY with pre-imported helpers, plus one-shot subcommands."""
import argparse
import sys

from chrome_harness import connection, profiles
from chrome_harness.eyes import snap, text, shot, js, errors_of
from chrome_harness.hands import open_url, nav


def _helpers():
    from chrome_harness import hands
    from chrome_harness.eyes import ws_call
    return {
        "state": connection.connection_state,
        "tabs": connection.list_targets,
        "list_profiles": profiles.list_profiles,
        "open_profile": profiles.open_profile,
        "current_profile": profiles.current_profile,
        "snap": snap, "text": text, "shot": shot, "js": js,
        "errors_of": errors_of, "ws_call": ws_call,
        "nav": nav, "open_url": open_url,
        "click_xy": hands.click_xy, "fill_js": hands.fill_js,
        "press_key": hands.press_key,
    }


def main(argv=None):
    if not sys.stdin.isatty():
        exec(sys.stdin.read(), dict(_helpers()))  # noqa: S102 - local harness by design
        return 0
    ap = argparse.ArgumentParser(prog="chrome-harness")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("state")
    sub.add_parser("tabs")
    sub.add_parser("profiles")
    p = sub.add_parser("open")
    p.add_argument("directory")
    p.add_argument("--url", default=None)
    ns = ap.parse_args(argv)
    if ns.cmd == "state":
        print(connection.connection_state())
    elif ns.cmd == "tabs":
        for t in connection.list_targets():
            print(t.get("id"), t.get("title"), t.get("url"))
    elif ns.cmd == "profiles":
        for pr in profiles.list_profiles():
            print(pr["directory"], "->", pr["name"])
    elif ns.cmd == "open":
        print(profiles.open_profile(ns.directory, ns.url))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
