# tests/test_eyes.py
from chrome_harness import eyes


class FakeWS:
    sent = None

    def send(self, payload):
        type(self).sent = payload

    def recv(self):
        import json
        rid = json.loads(self.sent)["id"]
        return json.dumps({"id": rid, "result": {"nodes": [
            {"nodeId": 1, "role": {"value": "button"}, "name": {"value": "Login"}},
            {"nodeId": 2, "role": {"value": "generic"}, "name": {"value": "x"}},
        ]}})

    def close(self):
        pass


def test_snap_filters_interactive(monkeypatch):
    monkeypatch.setattr(eyes.websocket, "create_connection", lambda *a, **k: FakeWS())
    rows = eyes.snap("ws://fake")
    assert rows == [{"ref": "@e1", "role": "button", "name": "Login", "nodeId": 1}]
