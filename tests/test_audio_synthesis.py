"""Automated unit tests for Mechanical Keyboard Sound procedural audio synthesis."""
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import keyboard_sound as ks


@pytest.fixture(scope="session")
def pygame_mixer():
    """Initializes pygame mixer once for headless testing."""
    ks.pygame.mixer.pre_init(ks.RATE, -16, 1, 512)
    ks.pygame.init()
    yield ks.pygame.mixer
    try:
        ks.pygame.mixer.quit()
        ks.pygame.quit()
    except Exception:
        pass


def test_profiles_structure():
    """Verify all sound profiles are properly structured with required keys."""
    assert len(ks.PROFILES) >= 12, "Should contain at least 12 sound profiles."

    valid_kinds = {
        "mechanical", "gunshot", "cannon", "laser",
        "boing", "pop", "duck", "fart"
    }

    for name, cfg in ks.PROFILES.items():
        assert "kind" in cfg, f"Profile '{name}' missing 'kind' key."
        assert "description" in cfg, f"Profile '{name}' missing 'description' key."
        assert cfg["kind"] in valid_kinds, f"Unknown kind '{cfg['kind']}' in '{name}'."

        if cfg["kind"] == "mechanical":
            for param in ("click", "body", "pitch", "brightness"):
                assert param in cfg, f"Mechanical profile '{name}' missing '{param}'."
                assert cfg[param] > 0, f"Parameter '{param}' in '{name}' must be positive."


def test_make_sound_all_profiles(pygame_mixer):
    """Verify that procedural sound synthesis runs without errors for every profile."""
    for name in ks.PROFILES:
        sound = ks.make_sound(name, variant=0)
        assert isinstance(sound, ks.pygame.mixer.Sound), f"Output for '{name}' must be a pygame.mixer.Sound."
        length = sound.get_length()
        assert length > 0.02, f"Sound length for '{name}' is unexpectedly short: {length}s."
        assert length < 2.0, f"Sound length for '{name}' is unexpectedly long: {length}s."


def test_make_sound_variants(pygame_mixer):
    """Verify that multiple variants can be generated with distinct seeds."""
    profile_name = "Realistic Click-Clack"
    variants = [ks.make_sound(profile_name, i) for i in range(5)]
    assert len(variants) == 5
    for s in variants:
        assert isinstance(s, ks.pygame.mixer.Sound)


def test_settings_serialization():
    """Verify settings dictionary save and load logic."""
    test_data = {"profile": "Blue Switch (Clicky)", "volume": 85}
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_settings = Path(tmp_dir) / "settings.json"
        tmp_settings.write_text(json.dumps(test_data), encoding="utf-8")

        loaded = json.loads(tmp_settings.read_text(encoding="utf-8"))
        assert loaded == test_data
        assert loaded["profile"] in ks.PROFILES
        assert 0 <= loaded["volume"] <= 100
