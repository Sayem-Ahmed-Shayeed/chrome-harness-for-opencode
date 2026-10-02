from chrome_harness import hands


def test_fill_js_returns_ok(monkeypatch):
    monkeypatch.setattr(hands, "ws_call", lambda *a, **k: {"result": {"result": {"value": "ok"}}})
    assert hands.fill_js("ws://fake", "#q", "hi") == "ok"


def test_fill_js_escapes_quotes_and_newlines(monkeypatch):
    import json
    seen = {}
    def _fake(u, m, p=None):
        seen["expr"] = p["expression"]
        return {"result": {"result": {"value": "ok"}}}
    monkeypatch.setattr(hands, "ws_call", _fake)
    text = "o'brien\nline2"
    assert hands.fill_js("ws://fake", "#q", text) == "ok"
    assert json.dumps(text) in seen["expr"]
    assert json.dumps("#q") in seen["expr"]


def test_click_xy_sends_mouse_moved_first(monkeypatch):
    calls = []
    monkeypatch.setattr(hands, "ws_call", lambda u, m, p=None: calls.append(p) or {})
    hands.click_xy("ws://fake", 10, 20)
    assert [c["type"] for c in calls] == ["mouseMoved", "mousePressed", "mouseReleased"]
    assert calls[0]["x"] == 10 and calls[0]["y"] == 20


def test_press_key_sends_key(monkeypatch):
    seen = {}
    monkeypatch.setattr(hands, "ws_call", lambda u, m, p=None: seen.setdefault("p", p) or {})
    hands.press_key("ws://fake", "Enter")
    assert seen["p"]["key"] == "Enter"


def test_press_key_enter_maps_virtual_key_code(monkeypatch):
    calls = []
    monkeypatch.setattr(hands, "ws_call", lambda u, m, p=None: calls.append(p) or {})
    hands.press_key("ws://fake", "Enter")
    assert calls[0]["windowsVirtualKeyCode"] == 13
    assert calls[0]["type"] == "keyDown"
    assert calls[1]["type"] == "keyUp"


def test_open_url_down_raises_no_debug_port(monkeypatch):
    import urllib.error
    monkeypatch.setattr(
        hands.urllib.request, "urlopen",
        lambda *a, **k: (_ for _ in ()).throw(urllib.error.URLError("refused")),
    )
    try:
        hands.open_url("https://example.com")
    except RuntimeError as e:
        assert "no-debug-port" in str(e)
        assert "--remote-debugging-port=9222" in str(e)
    else:
        raise AssertionError("expected RuntimeError")
