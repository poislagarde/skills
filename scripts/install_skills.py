#!/usr/bin/env python3
"""Link this checkout's skills into the user skill directories."""

from pathlib import Path
import sys


def install_skills(repo_root: Path, user_home: Path) -> None:
    repo_root = repo_root.resolve()
    skills = sorted(path.parent for path in repo_root.glob("*/SKILL.md"))
    if not skills:
        raise ValueError("No top-level skills found in this checkout.")

    roots = (user_home / ".agents/skills", user_home / ".claude/skills")
    links = [(root / skill.name, skill) for root in roots for skill in skills]

    # Check every destination before changing anything. Local copies or links
    # to another checkout must be reconciled explicitly, never overwritten.
    for root in roots:
        if (root.exists() or root.is_symlink()) and not root.is_dir():
            raise ValueError(f"Skill directory is not a directory: {root}")
    for destination, source in links:
        if destination.exists() or destination.is_symlink():
            if not (destination.is_symlink() and destination.resolve() == source):
                raise ValueError(f"Refusing to replace an existing install: {destination}")

    for root in roots:
        root.mkdir(parents=True, exist_ok=True)
    for destination, source in links:
        if not destination.is_symlink():
            destination.symlink_to(source, target_is_directory=True)
        print(f"Linked {destination} -> {source}")

    # Migrate only this checkout's legacy links, after both installs succeed.
    # Other skills and real directories in the legacy root remain untouched.
    for skill in skills:
        legacy = user_home / ".codex/skills" / skill.name
        if legacy.is_symlink() and legacy.resolve() == skill:
            legacy.unlink()
            print(f"Removed legacy link {legacy}")


if __name__ == "__main__":
    try:
        install_skills(Path(__file__).resolve().parent.parent, Path.home())
    except (OSError, ValueError) as error:
        sys.exit(str(error))
