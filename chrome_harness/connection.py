"""CDP HTTP transport. No websocket dependency here on purpose."""
import json
import urllib.error
import urllib.request

CDP_HOST = "127.0.0.1"
CDP_PORT = 9222


def _http_get(path):
    url = f"http://{CDP_HOST}:{CDP_PORT}{path}"
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
            return json.load(r)
    except (urllib.error.URLError, ConnectionRefusedError, TimeoutError, OSError):
        return None


def connection_state():
    """Return 'ready' when CDP answers, else 'no-debug-port'."""
    if _http_get("/json/version") is None:
        return "no-debug-port"
    return "ready"


def list_targets():
    """Return CDP targets list (tabs/pages), [] when unreachable."""
    data = _http_get("/json/list")
    return data if isinstance(data, list) else []
