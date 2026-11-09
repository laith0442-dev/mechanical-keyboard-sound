# Contributing to Mechanical Keyboard Sound

Thank you for your interest in contributing to **Mechanical Keyboard Sound**! Contributions from the community help make this project better for everyone.

---

## Code of Conduct

Please be respectful, constructive, and helpful when opening issues or participating in pull requests.

---

## How Can I Contribute?

### 1. Adding New Sound Profiles
One of the most exciting ways to contribute is designing new procedural sound profiles!
All sounds in this project are generated mathematically without any audio files.
- Open `keyboard_sound.py` and inspect the `PROFILES` dictionary and `make_sound()` function.
- Tune parameters (`click`, `body`, `pitch`, `brightness`) or design a new procedural synthesizer block.
- Keep performance in mind: audio synthesis happens at startup in a fraction of a second.
- Write tests in `tests/test_audio_synthesis.py` for your new profile.

### 2. Reporting Bugs
If you find a bug:
1. Search existing [Issues](https://github.com/laith0442-dev/mechanical-keyboard-sound/issues) to avoid duplicates.
2. If not found, open a new issue using our **Bug Report** template.
3. Include your Windows version, Python version, error traceback, and steps to reproduce.

### 3. Suggesting Enhancements
Feature requests are welcome! Use the **Feature Request** template to explain the motivation and proposed behavior.

---

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/laith0442-dev/mechanical-keyboard-sound.git
   cd mechanical-keyboard-sound
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```powershell
   py -3.13 -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements-dev.txt
   ```

4. **Run tests:**
   ```powershell
   pytest
   ```

5. **Run the application:**
   ```powershell
   python keyboard_sound.py
   ```

6. **Build the standalone executable:**
   ```powershell
   .\build_exe.bat
   ```

---

## Submitting Pull Requests

1. Create a feature branch (`git checkout -b feature/amazing-sound-profile`).
2. Make your changes adhering to clean Python conventions (PEP 8).
3. Ensure automated tests pass (`pytest`).
4. Commit your changes with clear, descriptive commit messages.
5. Push to your branch and open a Pull Request against `main`.
