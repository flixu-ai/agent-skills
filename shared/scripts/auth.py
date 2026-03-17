#!/usr/bin/env python3
"""
Flixu CLI Authentication — shared across all Flixu agent skills.

Checks for FLIXU_API_KEY in three locations (in order):
  1. Environment variable FLIXU_API_KEY
  2. Config file ~/.flixu/credentials
  3. If neither found, opens browser for key creation and stores it

Usage:
  python auth.py              # Check auth status, login if needed
  python auth.py --check      # Silent check, exit 0 if authenticated, 1 if not
  python auth.py --logout     # Remove stored credentials
  python auth.py --status     # Print current auth status and plan info

The script validates the key by calling GET /v1/quota.
"""

import json
import os
import sys
import webbrowser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_BASE = "https://api.flixu.ai/v1"
CREDENTIALS_DIR = Path.home() / ".flixu"
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials"
SIGNUP_URL = "https://app.flixu.ai/sign-up"
API_KEYS_URL = "https://app.flixu.ai/settings/api-keys"


def get_api_key() -> str | None:
    """Resolve API key from env → config file → None."""
    # 1. Environment variable (highest priority)
    env_key = os.environ.get("FLIXU_API_KEY")
    if env_key:
        return env_key

    # 2. Credentials file
    if CREDENTIALS_FILE.exists():
        try:
            creds = json.loads(CREDENTIALS_FILE.read_text())
            return creds.get("api_key")
        except (json.JSONDecodeError, IOError):
            pass

    return None


def validate_key(api_key: str) -> dict | None:
    """Validate key by calling GET /v1/quota. Returns quota data or None."""
    req = Request(
        f"{API_BASE}/quota",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read()).get("data")
    except (HTTPError, URLError):
        return None


def store_key(api_key: str):
    """Store API key in ~/.flixu/credentials."""
    CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_FILE.write_text(json.dumps({"api_key": api_key}, indent=2))
    CREDENTIALS_FILE.chmod(0o600)  # Restrict to owner only
    print(f"  ✓ Credentials saved to {CREDENTIALS_FILE}")


def remove_key():
    """Remove stored credentials."""
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()
        print("  ✓ Credentials removed.")
    else:
        print("  No credentials found.")


def interactive_login():
    """Guide user through login flow."""
    print()
    print("  ╔═══════════════════════════════════════╗")
    print("  ║       Flixu CLI Authentication        ║")
    print("  ╚═══════════════════════════════════════╝")
    print()
    print("  No API key found. Let's set one up.\n")

    # Check if they have an account
    print("  Do you have a Flixu account? [Y/n] ", end="", flush=True)
    has_account = input().strip().lower()

    if has_account in ("n", "no"):
        print(f"\n  Opening sign-up page: {SIGNUP_URL}")
        webbrowser.open(SIGNUP_URL)
        print("  Create your account, then come back here.\n")
        print("  Press Enter when you've signed up...", end="", flush=True)
        input()

    # Open API keys page
    print(f"\n  Opening API keys page: {API_KEYS_URL}")
    webbrowser.open(API_KEYS_URL)
    print("  Create a new API key and copy it.\n")

    # Prompt for the key
    print("  Paste your API key: ", end="", flush=True)
    api_key = input().strip()

    if not api_key:
        print("\n  ✗ No key provided. Aborting.")
        sys.exit(1)

    # Validate
    print("\n  Validating key...", end="", flush=True)
    quota = validate_key(api_key)

    if not quota:
        print(" ✗")
        print("  Invalid API key. Please check and try again.")
        sys.exit(1)

    print(" ✓")

    # Store the key
    store_key(api_key)

    # Show account info
    plan = quota.get("plan", "free")
    credits = quota.get("credits_remaining", 0)
    print(f"\n  Logged in successfully!")
    print(f"  Plan: {plan}")
    print(f"  Credits remaining: {credits:,}")
    print()

    return api_key


def print_status(api_key: str):
    """Print auth status and account info."""
    quota = validate_key(api_key)
    if not quota:
        print("  ✗ Key is invalid or expired.")
        source = "FLIXU_API_KEY env" if os.environ.get("FLIXU_API_KEY") else str(CREDENTIALS_FILE)
        print(f"  Source: {source}")
        sys.exit(1)

    source = "FLIXU_API_KEY env var" if os.environ.get("FLIXU_API_KEY") else str(CREDENTIALS_FILE)
    plan = quota.get("plan", "free")
    credits = quota.get("credits_remaining", 0)

    print(f"  ✓ Authenticated")
    print(f"  Source: {source}")
    print(f"  Plan: {plan}")
    print(f"  Credits: {credits:,}")


def main():
    args = sys.argv[1:]

    # --logout
    if "--logout" in args:
        remove_key()
        return

    api_key = get_api_key()

    # --check (silent)
    if "--check" in args:
        if api_key and validate_key(api_key):
            sys.exit(0)
        else:
            sys.exit(1)

    # --status
    if "--status" in args:
        if not api_key:
            print("  ✗ Not authenticated. Run: python auth.py")
            sys.exit(1)
        print_status(api_key)
        return

    # Default: check or interactive login
    if api_key:
        print_status(api_key)
    else:
        interactive_login()


if __name__ == "__main__":
    main()
