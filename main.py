#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes one Wi-Fi network name to /output/entry.txt. The name has to
land a joke and imply a whole story in the few words a passer-by sees
in a phone's network list, and the sealed gate only accepts UTF-8 text
of 1 to 32 characters that is not only whitespace.

The story, in exactly 32 characters:

    She took the dog, left the Wi-Fi

A breakup told as an asset split: she walked out with the dog, and
what the narrator kept was the Wi-Fi. Situation, two characters and
one event, with the punchline landing on the last word — the network
is the consolation prize. No stock Wi-Fi joke, no password gag, no
"FBI Surveillance Van"; the twist is the trade itself.

Stdlib only. No network, no randomness, deterministic: the same
32 characters every run.
"""

import os
import sys

# The entry. Counted by hand and by the gate check below: 32 chars.
STORY = "She took the dog, left the Wi-Fi"

# The sealed gate: 1 to 32 characters, not only whitespace.
MIN_CHARS = 1
MAX_CHARS = 32


def char_count(text):
    """Count characters the way the gate does: Unicode code points."""
    return len(text)


def gate_problems(text):
    """Return a list of every gate violation, empty when the text is valid."""
    problems = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if char_count(text) < MIN_CHARS:
        problems.append("entry is empty (needs at least 1 character)")
    if char_count(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the 32-character limit"
            % char_count(text)
        )
    if text.strip() == "":
        problems.append("entry is only whitespace")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8")
    return problems


def resolve_output_dir():
    """Pick the output directory the way the harness expects.

    MAKEFUN_OUTPUT_DIR first (the grader convention), then the
    OUTPUT_DIR fallback, then /output as the last resort.
    """
    for env_name in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        candidate = os.environ.get(env_name)
        if candidate:
            return candidate
    return "/output"


def write_entry(text, output_dir):
    """Write the story to entry.txt and read it back to prove the round-trip."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8") as handle:
        written_back = handle.read()
    if written_back != text:
        raise SystemExit(
            "round-trip mismatch: wrote %r, read back %r"
            % (text, written_back)
        )
    return path


def main(argv):
    """Validate the story against the gate, then write it out.

    With --check, only validate and report the character budget
    without writing anything — handy for a quick gate sanity check.
    """
    problems = gate_problems(STORY)
    if problems:
        for problem in problems:
            print("gate: " + problem, file=sys.stderr)
        return 1
    if "--check" in argv[1:]:
        print(
            "gate OK: %d characters, %d of the 32-character budget spare"
            % (char_count(STORY), MAX_CHARS - char_count(STORY))
        )
        return 0
    output_dir = resolve_output_dir()
    path = write_entry(STORY, output_dir)
    print(
        "wrote entry.txt: %d characters, %r" % (char_count(STORY), STORY)
    )
    print("path: " + path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
