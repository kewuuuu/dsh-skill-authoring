#!/usr/bin/env python3
"""Check a skill directory against the skill-authoring checklist.

Usage:
  python check_skill.py <skill-dir>
  python check_skill.py --all <skills-dir>

Exit code 1 when any ERROR is reported. Warnings are advisory.
"""
import argparse
import os
import re
import sys

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ABS_PATH_RE = re.compile(r"([A-Za-z]:[\\/]|/(?:c|d)/Users|/d/engine)", re.I)
AUX_FILES = ("README.md", "CHANGELOG.md", "INSTALLATION.md")
BACKTICK = chr(96)


def parse_frontmatter(text):
    m = FRONT_RE.match(text)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def check_skill(path):
    name = os.path.basename(os.path.abspath(path))
    issues = []
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        return name, [("ERROR", "E1", "SKILL.md missing")], 0, 0
    with open(skill_md, "r", encoding="utf-8") as fh:
        text = fh.read()
    lines = text.count("\n") + 1
    fm = parse_frontmatter(text)
    if fm is None:
        issues.append(("ERROR", "E2", "missing YAML frontmatter (file must start with --- and close it)"))
        fm = {}
    skill_name = fm.get("name", "").strip()
    desc = fm.get("description", "").strip()

    if not skill_name:
        issues.append(("ERROR", "E2", "frontmatter has no name"))
    else:
        if skill_name != name:
            issues.append(("ERROR", "E3", "name '%s' != directory '%s'" % (skill_name, name)))
        if not KEBAB_RE.match(skill_name):
            issues.append(("ERROR", "E4", "name '%s' is not kebab-case" % skill_name))

    if not desc:
        issues.append(("ERROR", "E2", "frontmatter has no description"))
    else:
        if len(desc) > 1024:
            issues.append(("ERROR", "E5", "description is %d chars, over the 1024 limit" % len(desc)))
        if len(desc) < 40:
            issues.append(("WARN", "W1", "description is only %d chars, may not trigger" % len(desc)))
        if re.match(r"^(i |i can\b|i will\b)", desc, re.I):
            issues.append(("WARN", "W2", "description uses first person; use third person"))
        if "\n" in desc:
            issues.append(("WARN", "W3", "description spans lines; keep it on one line"))

    if lines > 300:
        issues.append(("WARN", "W4", "SKILL.md is %d lines, over 300; move specs to references/" % lines))
    elif lines > 150:
        issues.append(("WARN", "W5", "SKILL.md is %d lines, over the 150 target" % lines))

    for aux in AUX_FILES:
        if os.path.isfile(os.path.join(path, aux)):
            issues.append(("WARN", "W6", "skill dir contains %s; maintainer docs should not ship with the skill" % aux))

    for target in LINK_RE.findall(text):
        target = target.strip().split("#")[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "/")):
            continue
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        if not os.path.exists(os.path.join(path, target)):
            issues.append(("WARN", "W7", "relative link points to a missing file: %s" % target))

    for idx, line in enumerate(text.splitlines(), start=1):
        if ABS_PATH_RE.search(line) and BACKTICK not in line:
            issues.append(("WARN", "W8", "SKILL.md:%d has an absolute path (an instance fact); consider moving it out" % idx))
            break

    return name, issues, lines, len(desc)


def report(path):
    name, issues, lines, desc_len = check_skill(path)
    errors = sum(1 for level, _, _ in issues if level == "ERROR")
    warns = len(issues) - errors
    print("skill: %s  (%s)" % (name, os.path.abspath(path)))
    print("  SKILL.md %d lines, description %d chars" % (lines, desc_len))
    if not issues:
        print("  ok    no findings")
    for level, code, msg in issues:
        print("  %-5s [%s] %s" % (level, code, msg))
    print("  summary: %d error(s), %d warning(s)" % (errors, warns))
    return errors, warns


def main():
    ap = argparse.ArgumentParser(description="Check SKILL.md structure and hygiene")
    ap.add_argument("path", nargs="?", help="skill directory")
    ap.add_argument("--all", dest="all_dir", help="parent directory containing several skills")
    args = ap.parse_args()

    if not args.path and not args.all_dir:
        ap.print_help()
        return 2

    errors_total = 0
    warns_total = 0
    if args.all_dir:
        root = args.all_dir
        found = [d for d in sorted(os.listdir(root))
                 if os.path.isfile(os.path.join(root, d, "SKILL.md"))]
        for d in found:
            e, w = report(os.path.join(root, d))
            errors_total += e
            warns_total += w
            print("")
        print("checked %d skill(s): %d error(s), %d warning(s)" % (len(found), errors_total, warns_total))
    else:
        e, w = report(args.path)
        errors_total += e
        warns_total += w

    return 1 if errors_total else 0


if __name__ == "__main__":
    sys.exit(main())
