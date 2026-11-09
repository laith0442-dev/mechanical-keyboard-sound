# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

---

## Privacy & Input Handling Disclosure

Because **Mechanical Keyboard Sound** listens to global keyboard events to trigger audio playback, we take user privacy and security with absolute seriousness:

1. **No Keystroke Logging**: The application **does not** record, log, save, or serialize typed keys, words, sentences, or text.
2. **Transient In-Memory State Only**: Key objects are only inspected in memory to determine whether they belong to an ignored modifier list (`Shift`, `Ctrl`, `Alt`, `Esc`, etc.) and to prevent repeating sounds while a key is held. This state is cleared immediately when the key is released.
3. **No Network Activity**: The application contains **zero network calls, zero analytics, zero telemetry, and zero phone-home mechanisms**. All sound synthesis and playback happen 100% offline and locally on your computer.
4. **Local Configuration Only**: The only file written to your machine is a local JSON file storing your selected profile and volume percentage:
   `%APPDATA%\MechanicalKeyboardSound\settings.json`

---


