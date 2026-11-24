"""The 3 AM Commit Message — entry program.

Writes one line (<=200 chars) to /output/entry.txt.
Stdlib only, deterministic.
"""
import os

TEXT = (
    "fix(prod): broke everything at 3am, all tests green, "
    "reverting the fix I have not written yet"
)

MAX_CHARS = 200


def validate(text):
    """Enforce the scorer's gate (RULES.txt): UTF-8 text, 1-200 chars,
    a single line, not whitespace-only, no leading/trailing
    whitespace. Raises SystemExit on any violation."""
    if not isinstance(text, str):
        raise SystemExit("entry text must be str")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        raise SystemExit("entry text is not valid UTF-8")
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            f"entry text must be 1-{MAX_CHARS} chars, got {len(text)}")
    if text != text.strip():
        raise SystemExit("entry text must not have leading/trailing whitespace")
    if not text.strip():
        raise SystemExit("entry text must not be whitespace-only")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must be a single line (no CR/LF)")
    if any(ord(c) < 0x20 for c in text):
        raise SystemExit(
            "entry text contains a control character (\\x00-\\x1f not allowed)")
    return text


def check_gate(text):
    """Backwards-compatible name for validate()."""
    return validate(text)


def write_entry(text):
    """Validate, then write text atomically to /output/entry.txt
    (or $OUTPUT_DIR) and verify by reading it back."""
    validate(text)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise SystemExit("read-back verification failed for entry.txt")
    return path


def main():
    write_entry(TEXT)


if __name__ == "__main__":
    main()
