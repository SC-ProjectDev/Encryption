#!/usr/bin/env python3
"""
cipher_tool.py
Interactive CLI supporting:
  • ROT13
  • ROT-47 (zero-width chars stripped)
  • Optional reversal
  • Encode ⬌ Decode modes
"""

import re
import string
import sys

# ──────────  Common helpers ──────────
def yes_no(prompt: str) -> bool:
    while True:
        ans = input(f"{prompt} [y/n] > ").strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print("Please answer y or n.")

def choose(items: dict, header: str):
    while True:
        print(f"\n{header}")
        for key, (label, _) in items.items():
            print(f"  {key}) {label}")
        choice = input("Select option > ").strip()
        if choice in items:
            return items[choice]
        print("❌ Invalid choice—try again.")

# ──────────  ROT13  ──────────
_rot13_table = str.maketrans(
    string.ascii_uppercase + string.ascii_lowercase,
    string.ascii_uppercase[13:] + string.ascii_uppercase[:13]
    + string.ascii_lowercase[13:] + string.ascii_lowercase[:13]
)
def rot13(s: str) -> str:
    return s.translate(_rot13_table)

# ──────────  ROT47  (printable ASCII 33–126) ──────────
_ZW_RE = re.compile(r'[\u200B\u200C\u200D\uFEFF]')   # zero-width chars to strip

def _rot47_core(s: str) -> str:
    out = []
    for ch in s:
        o = ord(ch)
        if 33 <= o <= 126:                # printable ASCII block
            out.append(chr(33 + ((o - 33 + 47) % 94)))
        else:
            out.append(ch)                # leave others unchanged
    return ''.join(out)

def rot47_no_zw(s: str) -> str:
    """ROT-47 after removing zero-width characters."""
    return _rot47_core(_ZW_RE.sub('', s))

# ──────────  Cipher registry  ──────────
CIPHERS = {
    "1": ("ROT13", rot13),
    "2": ("ROT-47 (no zero-width)", rot47_no_zw),
}

# ──────────  Main loop ──────────
def main() -> None:
    modes = {"1": ("Encode", True), "2": ("Decode", False)}

    print("=== Simple Cipher Tool ===")
    while True:
        mode_label, encode_mode = choose(modes, "Do you want to:")
        cipher_label, cipher_fn = choose(CIPHERS, "Choose a cipher:")

        prompt = "Enter the plaintext" if encode_mode else "Paste the encoded text"
        text = input(f"\n{prompt} > ")

        # Reversal logic
        if encode_mode:
            reverse = yes_no("Reverse the result after encoding?")
            output = cipher_fn(text)
            if reverse:
                output = output[::-1]
        else:                               # decode
            was_reversed = yes_no("Was the text reversed before it was sent?")
            if was_reversed:
                text = text[::-1]
            output = cipher_fn(text)

        print(f"\n➡️  {mode_label}d output: {output}\n")

        if not yes_no("Do another?"):
            print("Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted—exiting.")
        sys.exit(0)
