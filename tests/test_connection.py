from chrome_harness.connection import connection_state, list_targets


def test_connection_state_known_value():
    assert connection_state() in ("ready", "no-debug-port")


def test_list_targets_returns_list():
    assert isinstance(list_targets(), list)
