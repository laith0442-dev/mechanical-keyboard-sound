# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-11-09

### Added
- **Procedural Audio Engine**:
  - Pure mathematical sound synthesis generating 16-bit signed PCM mono audio at 44.1 kHz.
  - Zero external sound files or media dependencies.
  - 5 pre-rendered randomized variants per profile with round-robin playback.
  - Subtle random pitch perturbation (0.96x – 1.04x) on every key stroke to eliminate the machine-gun effect.
- **12 Built-in Sound Profiles**:
  - Mechanical switch models: Realistic Click-Clack, Blue Switch (Clicky), Brown Switch (Tactile), Red Switch (Smooth), Deep Thock.
  - Novelty audio effects: Gunshot (Movie FX), Cannon Fire, Laser Pew, Cartoon Boing, Bubble Pop, Rubber Duck, Tiny Fart.
- **Global Keyboard Listener**:
  - Low-latency global keyboard hooks powered by `pynput.keyboard`.
  - Smart modifier suppression: Shift, Ctrl, Alt, Windows/Cmd, Caps Lock, and Esc keys remain silent.
  - Thread-safe key-holding deduplication preventing rapid sound flooding while holding down keys.
- **Modern Graphical User Interface**:
  - Lightweight Tkinter / TTK interface with Windows native styling.
  - Profile selection dropdown with live descriptions.
  - Continuous volume slider (0–100%) with percentage readout.
  - Live sound testing button ("Test sound").
  - Mute/unmute toggle ("Disable sounds" / "Enable sounds").
  - Application status indicator and graceful exit handler.
- **Configuration Persistence**:
  - Auto-saved user preferences (last selected profile and volume) in `%APPDATA%\MechanicalKeyboardSound\settings.json`.
- **Packaging & Build System**:
  - PyInstaller single-file windowed build specification (`MechanicalKeyboardSound.spec`).
  - Automated build batch script (`build_exe.bat`).
- **Developer Tools**:
  - Automated pytest test suite for headless audio synthesis and profile parameter verification.
