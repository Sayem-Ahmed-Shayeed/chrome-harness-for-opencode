"""Read helpers for the visible page. ws_url comes from a target's webSocketDebuggerUrl."""
import base64
import itertools
import json
import time

import websocket

_ids = itertools.count(1)
INTERACTIVE_ROLES = {"button", "link", "textbox", "checkbox", "radio", "heading", "image", "switch"}


def ws_call(ws_url, method, params=None):
    ws = websocket.create_connection(ws_url, timeout=10)
    try:
        rid = next(_ids)
        ws.send(json.dumps({"id": rid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == rid:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})
    finally:
        ws.close()


def snap(ws_url):
    tree = ws_call(ws_url, "Accessibility.getFullAXTree")
    rows = []
    for n in tree.get("nodes", []):
        role = (n.get("role") or {}).get("value", "")
        if role not in INTERACTIVE_ROLES:
            continue
        rows.append({
            "ref": f"@e{len(rows) + 1}",
            "role": role,
            "name": (n.get("name") or {}).get("value", ""),
            "nodeId": n.get("nodeId"),
        })
    return rows


def text(ws_url):
    r = ws_call(ws_url, "Runtime.evaluate", {
        "expression": "document.body ? document.body.innerText : ''",
        "returnByValue": True,
    })
    return ((r.get("result") or {}).get("result") or {}).get("value", "")


def shot(ws_url, path):
    r = ws_call(ws_url, "Page.captureScreenshot", {"format": "png"})
    with open(path, "wb") as f:
        f.write(base64.b64decode(r["data"]))
    return path


def js(ws_url, expr):
    r = ws_call(ws_url, "Runtime.evaluate", {"expression": expr, "returnByValue": True})
    return ((r.get("result") or {}).get("result") or {}).get("value")


def errors_of(ws_url, seconds=3):
    """Collect Log/Runtime error events for a few seconds. Returns [] when quiet."""
    ws = websocket.create_connection(ws_url, timeout=10)
    try:
        rid = next(_ids)
        for method in ("Log.enable", "Runtime.enable"):
            rid += 1
            ws.send(json.dumps({"id": rid, "method": method}))
            ws.recv()
        out, end = [], time.time() + seconds
        ws.settimeout(max(end - time.time(), 0.1))
        while time.time() < end:
            try:
                msg = json.loads(ws.recv())
            except Exception:
                break
            if msg.get("method") in ("Log.entryAdded", "Runtime.consoleAPICalled", "Runtime.exceptionThrown"):
                out.append(msg)
        return out
    finally:
        ws.close()
