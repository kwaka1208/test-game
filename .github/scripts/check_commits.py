"""Check that commit messages (or a PR title) follow Conventional Commits."""
import json
import os
import re
import sys

TYPES = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
PATTERN = re.compile(r"^(?P<type>[a-z]+)(\([\w\-]+\))?!?: (?P<subject>.+)$")
PAST_TENSE = re.compile(r"^[a-z]+ed$")


def check(message):
    """Return (errors, warnings) for the first line of a message."""
    first = message.strip().splitlines()[0] if message.strip() else ""
    if first.startswith("Merge "):
        return [], []
    errors, warnings = [], []
    m = PATTERN.match(first)
    if not m:
        errors.append("Use the form `type: subject` (example: `feat: add a library room`).")
        return errors, warnings
    if m.group("type") not in TYPES:
        errors.append(f"Unknown type `{m.group('type')}`. Use one of: {', '.join(TYPES)}.")
    subject = m.group("subject")
    first_word = subject.split()[0]
    if first_word[0].isupper():
        warnings.append("Start the subject with a lowercase letter.")
    if PAST_TENSE.match(first_word.lower()):
        warnings.append(f"`{first_word}` looks like past tense. Use the base form of the verb "
                        "(for example `add`, not `added`).")
    if subject.endswith("."):
        warnings.append("Do not end the subject with a period.")
    if len(first) > 72:
        errors.append(f"Too long ({len(first)} characters). Keep it under 50 if you can.")
    elif len(first) > 50:
        warnings.append(f"A little long ({len(first)} characters). Try to keep it under 50.")
    return errors, warnings


def main():
    event = os.environ.get("EVENT_NAME", "")
    if event == "pull_request":
        items = [("PR title", os.environ.get("PR_TITLE", ""))]
    else:
        commits = json.loads(os.environ.get("COMMITS_JSON") or "[]") or []
        items = [(c.get("id", "")[:7], c.get("message", "")) for c in commits]

    lines = ["| Commit | Message | Result |", "|---|---|---|"]
    failed = False
    for ref, message in items:
        first = message.strip().splitlines()[0] if message.strip() else "(empty)"
        errors, warnings = check(message)
        if errors:
            failed = True
            status = "❌ " + " ".join(errors)
        elif warnings:
            status = "⚠️ " + " ".join(warnings)
        else:
            status = "✅ Good!"
        print(f"{ref} | {first} | {status}")
        lines.append(f"| {ref} | `{first}` | {status} |")

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## Commit message check\n\n" + "\n".join(lines) + "\n")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
