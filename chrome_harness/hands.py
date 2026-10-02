"""Act helpers for the visible page."""
import json
import urllib.error
import urllib.parse
import urllib.request

from chrome_harness.connection import CDP_HOST, CDP_PORT
from chrome_harness.eyes import ws_call


def open_url(url):
    qs = urllib.parse.quote(url, safe=":/?#=&%")
    req = urllib.request.Request(
        f"http://{CDP_HOST}:{CDP_PORT}/json/new?{qs}", data=b"", method="PUT"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.load(r)
    except (urllib.error.URLError, OSError) as e:
        raise RuntimeError(
            f"no-debug-port: cannot reach Chrome at {CDP_HOST}:{CDP_PORT} ({e}); "
            "relaunch with --remote-debugging-port=9222"
        ) from e


def close_target(target_id):
    try:
        with urllib.request.urlopen(
            f"http://{CDP_HOST}:{CDP_PORT}/json/close/{target_id}", timeout=5
        ):
            return True
    except (urllib.error.URLError, OSError) as e:
        raise RuntimeError(
            f"no-debug-port: cannot reach Chrome at {CDP_HOST}:{CDP_PORT} ({e}); "
            "relaunch with --remote-debugging-port=9222"
        ) from e


def nav(ws_url, url):
    return ws_call(ws_url, "Page.navigate", {"url": url})


def click_xy(ws_url, x, y):
    ws_call(ws_url, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    for t in ("mousePressed", "mouseReleased"):
        ws_call(ws_url, "Input.dispatchMouseEvent", {
            "type": t, "x": x, "y": y, "button": "left", "clickCount": 1})
    return {"x": x, "y": y}


def fill_js(ws_url, selector, text):
    expr = (
        "(() => { const el = document.querySelector(%s); if (!el) return 'not-found';"
        " el.focus(); el.value = %s;"
        " el.dispatchEvent(new Event('input', {bubbles: true}));"
        " el.dispatchEvent(new Event('change', {bubbles: true})); return 'ok'; })()"
        % (json.dumps(selector), json.dumps(text))
    )
    r = ws_call(ws_url, "Runtime.evaluate", {"expression": expr, "returnByValue": True})
    return ((r.get("result") or {}).get("result") or {}).get("value")


_VK = {"Enter": 13, "Tab": 9, "Escape": 27}


def press_key(ws_url, key, code=None, text=None, windows_virtual_key_code=None):
    base = {"key": key}
    if code:
        base["code"] = code
    if text is not None:
        base["text"] = text
    if windows_virtual_key_code is not None:
        base["windowsVirtualKeyCode"] = windows_virtual_key_code
    elif key in _VK:
        base["windowsVirtualKeyCode"] = _VK[key]
    ws_call(ws_url, "Input.dispatchKeyEvent", dict(base, type="keyDown"))
    ws_call(ws_url, "Input.dispatchKeyEvent", dict(base, type="keyUp"))
    return {"key": key}
