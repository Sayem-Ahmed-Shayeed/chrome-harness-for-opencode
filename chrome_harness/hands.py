"""Act helpers for the visible page."""
import urllib.parse
import urllib.request
from chrome_harness.connection import CDP_HOST, CDP_PORT
from chrome_harness.eyes import ws_call


def open_url(url):
    import json
    qs = urllib.parse.urlencode({"": url})[1:]
    req = urllib.request.Request(
        f"http://{CDP_HOST}:{CDP_PORT}/json/new?{qs}", data=b"", method="PUT"
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.load(r)


def close_target(target_id):
    with urllib.request.urlopen(
        f"http://{CDP_HOST}:{CDP_PORT}/json/close/{target_id}", timeout=5
    ):
        return True


def nav(ws_url, url):
    return ws_call(ws_url, "Page.navigate", {"url": url})


def click_xy(ws_url, x, y):
    for t in ("mousePressed", "mouseReleased"):
        ws_call(ws_url, "Input.dispatchMouseEvent", {
            "type": t, "x": x, "y": y, "button": "left", "clickCount": 1})
    return {"x": x, "y": y}


def fill_js(ws_url, selector, text):
    expr = (
        "(() => { const el = document.querySelector(%r); if (!el) return 'not-found';"
        " el.focus(); el.value = %r;"
        " el.dispatchEvent(new Event('input', {bubbles: true}));"
        " el.dispatchEvent(new Event('change', {bubbles: true})); return 'ok'; })()"
        % (selector, text)
    )
    r = ws_call(ws_url, "Runtime.evaluate", {"expression": expr, "returnByValue": True})
    return ((r.get("result") or {}).get("result") or {}).get("value")


def press_key(ws_url, key, code=None):
    base = {"key": key}
    if code:
        base["code"] = code
    ws_call(ws_url, "Input.dispatchKeyEvent", dict(base, type="keyDown"))
    ws_call(ws_url, "Input.dispatchKeyEvent", dict(base, type="keyUp"))
    return {"key": key}
