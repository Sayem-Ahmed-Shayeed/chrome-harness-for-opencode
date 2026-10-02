"""Chrome profile helpers. Reads names from the Local State file (verified 2026-10-02: 10 profiles)."""
import json
import os
import subprocess

CONFIG_DIR = os.path.expanduser("~/.config/google-chrome")
LOCAL_STATE = os.path.join(CONFIG_DIR, "Local State")
LAST_PROFILE_FILE = os.path.expanduser("~/.cache/chrome-harness/last_profile")


def list_profiles():
    try:
        with open(LOCAL_STATE) as f:
            info = json.load(f)["profile"]["info_cache"]
    except (OSError, ValueError, KeyError) as e:
        raise RuntimeError(f"cannot read Chrome Local State at {LOCAL_STATE}: {e}") from e
    return [
        {"directory": k, "name": v.get("name", k), "email": v.get("user_name", "")}
        for k, v in sorted(info.items())
    ]


def open_profile(directory, url=None):
    argv = ["google-chrome", f"--profile-directory={directory}"]
    if url:
        argv.append(url)
    env = dict(os.environ, DISPLAY=os.environ.get("DISPLAY", ":0"))
    subprocess.Popen(argv, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.makedirs(os.path.dirname(LAST_PROFILE_FILE), exist_ok=True)
    with open(LAST_PROFILE_FILE, "w") as f:
        f.write(directory)
    return argv


def current_profile():
    try:
        with open(LAST_PROFILE_FILE) as f:
            return f.read().strip() or None
    except OSError:
        return None
