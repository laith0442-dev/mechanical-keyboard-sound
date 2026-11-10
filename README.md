# Mechanical Keyboard Sound ⌨️🔊

<p align="center">
  <strong>Simulate authentic mechanical switches and expressive audio effects on any keyboard with zero external audio assets.</strong>
</p>

<p align="center">
  <a href="https://github.com/laith0442-dev/mechanical-keyboard-sound/releases"><img src="https://img.shields.io/github/v/release/laith0442-dev/mechanical-keyboard-sound?color=blue&label=Release" alt="Release"></a>
  <a href="https://www.python.org/downloads/release/python-3130/"><img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg" alt="Python Version"></a>
  <a href="https://github.com/laith0442-dev/mechanical-keyboard-sound/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="https://github.com/laith0442-dev/mechanical-keyboard-sound/actions"><img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6.svg" alt="Platform"></a>
  <a href="https://github.com/laith0442-dev/mechanical-keyboard-sound/stargazers"><img src="https://img.shields.io/github/stars/laith0442-dev/mechanical-keyboard-sound?style=flat" alt="GitHub Stars"></a>
</p>

---

## 📖 Overview

**Mechanical Keyboard Sound** is a lightweight, high-performance desktop utility for Windows that transforms typing on standard membrane keyboards or laptop keyboards into an auditory tactile experience.

Unlike traditional keyboard sound apps that require gigabytes of external `.wav` or `.ogg` sound packs, **Mechanical Keyboard Sound** features a **100% procedural audio engine**. Every mechanical click, clack, thock, and sound effect is synthesized dynamically in memory using mathematical signal processing.

<img width="566" height="563" alt="image" src="https://github.com/user-attachments/assets/ec5f8b46-d198-4b09-9343-3ec47fdeb3c0" />

<img width="567" height="563" alt="image" src="https://github.com/user-attachments/assets/0105e9b5-318c-4239-90f8-c619390eb4f7" />



```
       [ Key Press in Any App ]
                  │
                  ▼
   [ pynput Global Keyboard Hook ]
                  │  (Filters modifiers & held keys)
                  ▼
    [ Procedural Sound Engine ] ──► (Mathematical Synthesis: sine, noise, envelopes)
                  │
                  ▼
         [ Pygame Mixer PCM ] ──► (Low-latency 44.1 kHz playback)
```

---

## ✨ Key Features

- **Procedural Audio Synthesis**: Pure algorithmic sound generation. No external audio files, missing assets, or storage bloat.
- **12 Curated Sound Profiles**:
  - **Mechanical Switches**: Realistic Click-Clack, Blue Switch (Clicky), Brown Switch (Tactile), Red Switch (Smooth), Deep Thock.
  - **Expressive Sound Effects**: Gunshot (Movie FX), Cannon Fire, Laser Pew, Cartoon Boing, Bubble Pop, Rubber Duck, Tiny Fart.
- **Anti-Repetition Realism**: Generates 5 randomized variants per profile at startup with subtle pitch perturbation ($0.96\times$ to $1.04\times$) and round-robin playback to eliminate the "machine-gun" effect.
- **Low-Latency Background Operation**: Minimal CPU overhead while running in the background or minimized.
- **Smart Modifier Filtering**: Keys like `Shift`, `Ctrl`, `Alt`, `Caps Lock`, `Esc`, and `Windows` remain silent so shortcut combinations feel natural.
- **Key-Hold Deduplication**: Holding down keys (e.g., Backspace or Space) does not flood your ears with rapid repeat sounds.
- **Native Windows GUI**: Clean Tkinter/TTK interface with volume controls, live profile switching, test buttons, and mute toggles.
- **Automatic Persistence**: Automatically remembers your favorite sound profile and volume level in `%APPDATA%\MechanicalKeyboardSound\settings.json`.
- **100% Private & Offline**: No keystroke logging, no network telemetry, and no data collection whatsoever.

---

## 🎛️ Available Sound Profiles

| Profile | Category | Description |
| :--- | :--- | :--- |
| **Realistic Click-Clack** | Mechanical | Balanced mechanical switch with a crisp click and solid bottom-out clack. |
| **Blue Switch (Clicky)** | Mechanical | Bright, sharp, and loud mechanical click reminiscent of Cherry MX Blue switches. |
| **Brown Switch (Tactile)** | Mechanical | Subtle click with a warm, rounded body simulating a tactile bump. |
| **Red Switch (Smooth)** | Mechanical | Quiet, dampened, linear switch sound with minimal click resonance. |
| **Deep Thock** | Mechanical | Bass-heavy, low-pitched mechanical thock popular in custom lubed keyboards. |
| **Gunshot (Movie FX)** | FX / Fun | Stylized cinematic report with snappy transient attack and decaying punch. |
| **Cannon Fire** | FX / Fun | Deep battlefield boom with a rumbling low-frequency tail. |
| **Laser Pew** | FX / Fun | Sci-fi downward frequency sweep with subtle fizz. |
| **Cartoon Boing** | FX / Fun | Dual-tone frequency-modulated spring wobble. |
| **Bubble Pop** | FX / Fun | Crisp high-frequency snap followed by a plunk tone. |
| **Rubber Duck** | FX / Fun | Silly, squeaky harmonic quack sound effect. |
| **Tiny Fart** | FX / Fun | Comic raspberry raspberry sound modulated with low-frequency harmonics. |

---

## 🔒 Privacy & Security First

Because this software interacts with keyboard inputs, your privacy is paramount:

> [!IMPORTANT]
> **Mechanical Keyboard Sound is NOT a keylogger.**
> - **Zero Logging**: It **never** logs, saves, writes, or transmits any typed characters, words, or scan codes.
> - **Zero Network Activity**: The application contains no network libraries, analytics, telemetry, or remote connections. It runs completely offline.
> - **Ephemeral In-Memory Checks**: Key objects are checked solely against an ignored set (`Shift`, `Ctrl`, `Alt`, etc.) and a temporary `held` set to prevent audio repeat loops. Once a key is released, it is immediately discarded.

---

## 🚀 Installation & Getting Started

### Option 1: Standalone Executable (Recommended)

1. Go to the [Releases](https://github.com/laith0442-dev/mechanical-keyboard-sound/releases) page.
2. Download `MechanicalKeyboardSound.exe`.
3. Double-click to launch! No installation or Python setup required.

---

### Option 2: Running from Source

#### Prerequisites
- Windows 10 or 11 (64-bit)
- Python 3.10 – 3.13 (Python 3.13 recommended)

#### 1. Clone the Repository
```bash
git clone https://github.com/laith0442-dev/mechanical-keyboard-sound.git
cd mechanical-keyboard-sound
```

#### 2. Create a Virtual Environment (Recommended)
```powershell
py -3.13 -m venv venv
.\venv\Scripts\activate
```

#### 3. Install Dependencies
```powershell
pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt
```

#### 4. Run the Application
```powershell
python keyboard_sound.py
```

---

## 🛠️ Building the Standalone EXE

To package your own standalone `.exe` using PyInstaller:

```powershell
.\build_exe.bat
```
or run manually:
```powershell
py -3.13 -m PyInstaller --clean --noconfirm --onefile --windowed --name MechanicalKeyboardSound keyboard_sound.py
```
The compiled binary will be placed in `dist\MechanicalKeyboardSound.exe`.

---

## 🧪 Running Automated Tests

A dedicated test suite is included to verify sound synthesis integrity across all profiles:

```powershell
pip install -r requirements-dev.txt
pytest
```

---

## 🔧 Troubleshooting

### No sound is playing when typing
1. Click the **Test sound** button in the app. If you hear a click, the audio output is functioning properly.
2. Increase the volume slider (it defaults to 65%).
3. Verify that your Windows default audio playback device is selected and not muted.
4. Ensure the button shows **Disable sounds** (if it says **Enable sounds**, the app is currently muted).

### Keyboard sounds stop when typing inside an Administrator window
- On Windows, security restrictions prevent standard user-space background hooks from intercepting events inside elevated (Administrator) windows (e.g. Task Manager, elevated Command Prompt/PowerShell).
- To enable sounds across elevated windows, right-click `MechanicalKeyboardSound.exe` and select **Run as Administrator**.

### Antivirus or SmartScreen Warnings
- Standalone executables generated with PyInstaller sometimes trigger Windows SmartScreen reputation warnings because they are not digitally code-signed with an expensive commercial certificate.
- You can inspect the complete source code, verify that no malicious code exists, and build the executable yourself using `build_exe.bat`.

---

## 📋 System Requirements

- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **Processor**: Any standard x64 processor
- **Memory**: Less than 40 MB RAM
- **Disk Space**: ~25 MB

---

## 🗺️ Roadmap

- [ ] System tray minimization (minimize directly to taskbar notification area).
- [ ] Custom user-defined procedural synthesis profiles via GUI sliders.
- [ ] Per-key sound mapping (e.g., distinct heavy clacks for Spacebar and Enter).
- [ ] Cross-platform support for Linux (X11/Wayland) and macOS.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/laith0442-dev/mechanical-keyboard-sound/issues) or read our [Contributing Guide](CONTRIBUTING.md).

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Eng. Laith Qawasmeh**

- GitHub: [@laith1299](https://github.com/laith1299)


---


