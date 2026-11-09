"""Mechanical Keyboard Sound for Windows. Generates effects locally; never stores typed text."""
import array
import json
import math
import os
import random
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

try:
    import pygame
    from pynput import keyboard
except ImportError as exc:
    raise SystemExit(
        "Missing packages. In Command Prompt run:\n"
        "py -3.13 -m pip install --only-binary=:all: pygame==2.6.1 pynput\n\n"
        + str(exc)
    )

RATE = 44100
APP_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "MechanicalKeyboardSound"
SETTINGS = APP_DIR / "settings.json"

# kind selects the local synthesizer; there are no external sound files.
PROFILES = {
    "Realistic Click-Clack": {
        "kind": "mechanical", "click": .72, "body": .52, "pitch": 1.00, "brightness": 1.00,
        "description": "Balanced mechanical click with a short, solid clack."
    },
    "Blue Switch (Clicky)": {
        "kind": "mechanical", "click": 1.00, "body": .36, "pitch": 1.18, "brightness": 1.35,
        "description": "Brighter, sharper, louder mechanical clicks."
    },
    "Brown Switch (Tactile)": {
        "kind": "mechanical", "click": .58, "body": .62, "pitch": .98, "brightness": .90,
        "description": "Softer click with a noticeable tactile bump."
    },
    "Red Switch (Smooth)": {
        "kind": "mechanical", "click": .30, "body": .46, "pitch": .90, "brightness": .72,
        "description": "Quieter, smoother key sounds."
    },
    "Deep Thock": {
        "kind": "mechanical", "click": .24, "body": 1.00, "pitch": .68, "brightness": .62,
        "description": "Low-pitched, bass-heavy keyboard thock."
    },
    "Gunshot (Movie FX)": {
        "kind": "gunshot", "description": "A short, stylized cinematic pop and punchy report."
    },
    "Cannon Fire": {
        "kind": "cannon", "description": "A big cartoon battlefield-style boom with a rumbling tail."
    },
    "Laser Pew": {
        "kind": "laser", "description": "A sci-fi descending laser zap."
    },
    "Cartoon Boing": {
        "kind": "boing", "description": "A springy, wobbling cartoon boing."
    },
    "Bubble Pop": {
        "kind": "pop", "description": "A quick, bubbly pop with a tiny plunk."
    },
    "Rubber Duck": {
        "kind": "duck", "description": "A silly, squeaky duck-like quack."
    },
    "Tiny Fart": {
        "kind": "fart", "description": "A short, goofy raspberry sound."
    },
}


def _to_sound(samples):
    """Convert normalized float samples to a pygame mono PCM sound."""
    pcm = array.array("h", (int(max(-1.0, min(1.0, s)) * 30000) for s in samples))
    if sys.byteorder != "little":
        pcm.byteswap()
    return pygame.mixer.Sound(buffer=pcm.tobytes())


def make_sound(name, variant):
    cfg = PROFILES[name]
    rng = random.Random((variant + 1) * 8171 + list(PROFILES).index(name) * 313)
    kind = cfg["kind"]

    if kind == "mechanical":
        click_level, body_level = cfg["click"], cfg["body"]
        pitch = cfg["pitch"] * rng.uniform(.96, 1.04)
        brightness = cfg["brightness"]
        samples = []
        for i in range(int(RATE * .070)):
            t = i / RATE
            noise = rng.uniform(-1, 1) * math.exp(-t * (105 / max(.5, brightness))) * click_level * .46
            body = (
                math.sin(2 * math.pi * 175 * pitch * t) * .65
                + math.sin(2 * math.pi * 310 * pitch * t) * .20
            ) * math.exp(-t * 62) * body_level * .40
            impact = math.sin(2 * math.pi * 1150 * pitch * t) * math.exp(-t * 260) * click_level * .10
            samples.append(noise + body + impact)
        return _to_sound(samples)

    # Vary the pitch slightly so repeated keystrokes do not sound identical.
    pitch = rng.uniform(.96, 1.04)
    durations = {
        "gunshot": .28, "cannon": .88, "laser": .30, "boing": .46,
        "pop": .20, "duck": .31, "fart": .43,
    }
    samples = []
    count = int(RATE * durations[kind])

    for i in range(count):
        t = i / RATE
        noise = rng.uniform(-1.0, 1.0)
        sample = 0.0

        if kind == "gunshot":
            # A sharp noise burst plus a descending low-frequency punch and soft tail.
            attack = 1 - math.exp(-t * 900)
            crack = noise * math.exp(-t * 35) * attack * .48
            f = 48 + 58 * math.exp(-t * 24)
            boom = math.sin(2 * math.pi * f * pitch * t) * math.exp(-t * 15) * .58
            tail = math.sin(2 * math.pi * 72 * pitch * t) * math.exp(-t * 25) * .12
            sample = crack + boom + tail

        elif kind == "cannon":
            # Broad blast followed by a slower, low rumble.
            attack = 1 - math.exp(-t * 500)
            blast = noise * math.exp(-t * 5.5) * attack * .42
            f1 = 34 + 27 * math.exp(-t * 3.5)
            f2 = 51 + 12 * math.exp(-t * 2.5)
            rumble = (
                math.sin(2 * math.pi * f1 * pitch * t) * .66
                + math.sin(2 * math.pi * f2 * pitch * t) * .22
            ) * math.exp(-t * 3.2) * .65
            distant_tail = math.sin(2 * math.pi * 43 * pitch * max(0, t - .16)) * math.exp(-max(0, t - .16) * 5.5) * .12 if t > .16 else 0
            sample = blast + rumble + distant_tail

        elif kind == "laser":
            # Frequency sweep from a high sci-fi zap down to a low pew.
            f0, falloff, base = 1050 * pitch, 17.5, 145 * pitch
            phase = 2 * math.pi * (base * t + f0 * (1 - math.exp(-falloff * t)) / falloff)
            zap = math.sin(phase) * math.exp(-t * 8.5) * .62
            fizz = noise * math.exp(-t * 42) * .12
            sample = zap + fizz

        elif kind == "boing":
            # Wobbling spring tone with a decaying noisy attack.
            wobble = 42 * math.sin(2 * math.pi * 5.5 * t) * math.exp(-t * 3.4)
            phase = 2 * math.pi * (255 * pitch * t + 7.5 * math.sin(2 * math.pi * 5.5 * t) * math.exp(-t * 3.4))
            spring = math.sin(phase) * math.exp(-t * 5.8) * .62
            overtone = math.sin(2 * math.pi * (440 + wobble) * pitch * t) * math.exp(-t * 8) * .16
            tap = noise * math.exp(-t * 75) * .12
            sample = spring + overtone + tap

        elif kind == "pop":
            snap = noise * math.exp(-t * 48) * (1 - math.exp(-t * 800)) * .42
            plunk = math.sin(2 * math.pi * 230 * pitch * t) * math.exp(-t * 25) * .34
            sample = snap + plunk

        elif kind == "duck":
            # Amplitude pulses and harmonics suggest a silly duck-like quack.
            wobble = 1 + .20 * math.sin(2 * math.pi * 13 * t)
            env = (1 - math.exp(-t * 90)) * math.exp(-t * 7.5)
            freq = (390 + 65 * math.sin(2 * math.pi * 7 * t)) * pitch
            quack = (math.sin(2 * math.pi * freq * t) * .50 + math.sin(2 * math.pi * freq * 2.03 * t) * .23)
            airy = noise * .07
            sample = (quack + airy) * env * wobble

        elif kind == "fart":
            # Comic raspberry: harmonically rough low tone, modulated noise, fast fade.
            pulse = .55 + .45 * math.sin(2 * math.pi * (10 + 3 * math.sin(2 * math.pi * 2 * t)) * t)
            env = (1 - math.exp(-t * 70)) * math.exp(-t * 5.8)
            f = (78 + 24 * math.sin(2 * math.pi * 6 * t)) * pitch
            rasp = math.sin(2 * math.pi * f * t) * .38 + math.sin(2 * math.pi * f * 2.2 * t) * .15
            sample = (rasp + noise * .20) * env * pulse

        samples.append(sample)

    return _to_sound(samples)


class App:
    def __init__(self, root):
        self.root = root
        root.title("Mechanical Keyboard Sound & Fun FX")
        root.geometry("570x535")
        root.minsize(510, 480)
        try:
            self.settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.settings = {}

        start_profile = self.settings.get("profile", "Realistic Click-Clack")
        if start_profile not in PROFILES:
            start_profile = "Realistic Click-Clack"
        self.profile = tk.StringVar(value=start_profile)
        self.current_profile = start_profile
        self.volume = tk.IntVar(value=max(0, min(100, int(self.settings.get("volume", 65)))))
        self.current_volume = self.volume.get()
        self.enabled = True
        self.lock = threading.Lock()
        self.held = set()
        self.variant = 0

        try:
            pygame.mixer.pre_init(RATE, -16, 1, 512)
            pygame.init()
            pygame.mixer.set_num_channels(32)
            self.sounds = {name: [make_sound(name, i) for i in range(5)] for name in PROFILES}
        except Exception as exc:
            try:
                pygame.quit()
            except Exception:
                pass
            messagebox.showerror("Audio initialization failed", f"Could not initialize audio output or synthesize sounds.\n\n{exc}")
            raise

        self.build_ui()
        self.set_volume(self.volume.get())
        self.listener = keyboard.Listener(on_press=self.key_down, on_release=self.key_up)
        self.listener.start()
        self.status.set("Ready — type in any app. Minimize to keep it running.")
        root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        box = ttk.Frame(self.root, padding=18)
        box.pack(fill="both", expand=True)
        ttk.Label(box, text="Mechanical Keyboard Sound", font=("Segoe UI", 17, "bold")).pack(anchor="w")
        ttk.Label(box, text="Choose keyboard clicks or fun sound effects for each key press.", wraplength=510).pack(anchor="w", pady=(3, 14))

        pf = ttk.LabelFrame(box, text="Sound profile", padding=12)
        pf.pack(fill="x", pady=(0, 12))
        self.combo = ttk.Combobox(pf, textvariable=self.profile, values=list(PROFILES), state="readonly")
        self.combo.pack(fill="x")
        self.description = tk.StringVar()
        ttk.Label(pf, textvariable=self.description, wraplength=495).pack(anchor="w", pady=(7, 0))
        self.combo.bind("<<ComboboxSelected>>", self.profile_changed)
        self.update_description()

        vf = ttk.LabelFrame(box, text="Volume", padding=12)
        vf.pack(fill="x", pady=(0, 12))
        row = ttk.Frame(vf)
        row.pack(fill="x")
        self.scale = ttk.Scale(row, from_=0, to=100, command=lambda v: self.set_volume(int(float(v))))
        self.scale.set(self.volume.get())
        self.scale.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.vol_label = ttk.Label(row, width=5, anchor="e")
        self.vol_label.pack(side="right")
        self.scale.bind("<ButtonRelease-1>", lambda _e: self.save_settings())

        buttons = ttk.Frame(box)
        buttons.pack(fill="x", pady=(1, 10))
        self.toggle = ttk.Button(buttons, text="Disable sounds", command=self.toggle_sound)
        self.toggle.pack(side="left")
        ttk.Button(buttons, text="Test sound", command=self.play_sound).pack(side="left", padx=8)
        ttk.Button(buttons, text="Exit", command=self.close).pack(side="right")

        privacy_text = (
            "Leave this window open or minimize it, then type in another app. "
            "The selected sound plays for each key press. Typing is not recorded or saved. "
            "Gunshot and cannon effects are synthesized sound effects; keep the volume comfortable."
            "                                                                                                    "
            "-----------------------------------------------------------------------------------------------------"
            "Designed by Eng. Laith Qawasmeh - github.com/laith0442-dev"
        )
        ttk.Label(box, text=privacy_text, wraplength=510, justify="left").pack(anchor="w", pady=(2, 10))
        ttk.Separator(box).pack(fill="x", pady=(0, 8))
        self.status = tk.StringVar(value="Starting keyboard listener…")
        ttk.Label(box, textvariable=self.status).pack(anchor="w")

    def update_description(self):
        self.description.set(PROFILES[self.profile.get()]["description"])

    def profile_changed(self, _event=None):
        self.current_profile = self.profile.get()
        self.update_description()
        self.save_settings()

    def set_volume(self, value):
        self.current_volume = max(0, min(100, int(value)))
        self.volume.set(self.current_volume)
        for variants in self.sounds.values():
            for snd in variants:
                snd.set_volume(self.current_volume / 100)
        if hasattr(self, "vol_label"):
            self.vol_label.configure(text=f"{self.current_volume}%")

    def save_settings(self):
        try:
            APP_DIR.mkdir(parents=True, exist_ok=True)
            SETTINGS.write_text(
                json.dumps({"profile": self.current_profile, "volume": self.current_volume}, indent=2),
                encoding="utf-8"
            )
        except OSError:
            pass

    def toggle_sound(self):
        self.enabled = not self.enabled
        self.toggle.configure(text="Disable sounds" if self.enabled else "Enable sounds")
        self.status.set("Ready — type in any app." if self.enabled else "Muted — keyboard listener remains active.")

    def play_sound(self):
        if not self.enabled or self.current_volume <= 0:
            return
        try:
            variants = self.sounds[self.current_profile]
            self.variant = (self.variant + 1) % len(variants)
            variants[self.variant].play()
        except (pygame.error, KeyError):
            pass

    def key_down(self, key):
        # Do not make sounds for modifier/navigation keys. Key identity is never stored to disk.
        ignored = (
            keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.ctrl, keyboard.Key.ctrl_r,
            keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.alt_l, keyboard.Key.cmd,
            keyboard.Key.cmd_r, keyboard.Key.caps_lock, keyboard.Key.esc,
        )
        if key in ignored:
            return
        with self.lock:
            if key in self.held:
                return
            self.held.add(key)
        self.play_sound()

    def key_up(self, key):
        with self.lock:
            self.held.discard(key)

    def close(self):
        self.save_settings()
        try:
            self.listener.stop()
        except Exception:
            pass
        try:
            pygame.mixer.stop()
            pygame.quit()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
