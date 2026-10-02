# tests/test_profiles.py
from chrome_harness import profiles


def test_list_profiles_has_ggs():
    by_dir = {p["directory"]: p for p in profiles.list_profiles()}
    assert by_dir["Profile 16"]["name"] == "ggs"
    assert len(by_dir) == 10


def test_open_profile_builds_argv(monkeypatch, tmp_path):
    monkeypatch.setattr(profiles, "LAST_PROFILE_FILE", str(tmp_path / "last"))
    seen = {}

    class FakePopen:
        def __init__(self, argv, env=None, stdout=None, stderr=None):
            seen["argv"] = argv

    monkeypatch.setattr(profiles.subprocess, "Popen", FakePopen)
    argv = profiles.open_profile("Profile 16", "https://example.com")
    assert argv == ["google-chrome", "--profile-directory=Profile 16", "https://example.com"]
    assert seen["argv"] == argv


def test_current_profile_roundtrip(monkeypatch, tmp_path):
    monkeypatch.setattr(profiles, "LAST_PROFILE_FILE", str(tmp_path / "last"))
    assert profiles.current_profile() is None


def test_list_profiles_missing_raises_with_path(monkeypatch, tmp_path):
    missing = str(tmp_path / "Local State")
    monkeypatch.setattr(profiles, "LOCAL_STATE", missing)
    try:
        profiles.list_profiles()
    except RuntimeError as e:
        assert missing in str(e)
    else:
        raise AssertionError("expected RuntimeError")
