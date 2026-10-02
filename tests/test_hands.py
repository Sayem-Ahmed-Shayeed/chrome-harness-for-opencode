from chrome_harness import hands


def test_fill_js_returns_ok(monkeypatch):
    monkeypatch.setattr(hands, "ws_call", lambda *a, **k: {"result": {"result": {"value": "ok"}}})
    assert hands.fill_js("ws://fake", "#q", "hi") == "ok"


def test_press_key_sends_key(monkeypatch):
    seen = {}
    monkeypatch.setattr(hands, "ws_call", lambda u, m, p=None: seen.setdefault("p", p) or {})
    hands.press_key("ws://fake", "Enter")
    assert seen["p"]["key"] == "Enter"
