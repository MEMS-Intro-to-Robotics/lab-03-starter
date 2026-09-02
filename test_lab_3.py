#!/usr/bin/env python3
"""Automated repository checks for Lab 3: Scripting with ROS 2 Topics and Services.

Run with: pytest test_lab_3.py -v

These checks establish that the deliverables are present and well-formed. They
do not judge whether a script draws a recognizable letter, whether the
screenshot shows both letters in distinct colors, or whether the discussion
answers are correct; course staff grade those from the report.
"""

from __future__ import annotations

import struct
import subprocess
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

REQUIRED_SCRIPTS = (
    "turtleletter.sh",
    "turtleletterstwo.sh",
)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
EXPECTED_SCREENSHOT = "turtlesim_letters"

README_STARTER_FINGERPRINT = "Update this README"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _png_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


def _images(repo: Path) -> list[Path]:
    docs = repo / "docs"
    if not docs.is_dir():
        return []
    return [p for p in docs.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]


def check_required_files(repo: Path) -> list[str]:
    """Layout and artifacts: the deliverables exist and are readable.

    Deliberately not checked: what the scripts contain. A student who reached
    the required end state with their own approach did the lab.
    """
    errors: list[str] = []

    readme = repo / "README.md"
    if not readme.is_file():
        errors.append("Missing required file: README.md")
    elif readme.stat().st_size == 0:
        errors.append("Required file is empty: README.md")
    elif README_STARTER_FINGERPRINT in _read_text(readme):
        errors.append(
            "README.md still contains the starter text; replace it with your "
            "name, NetID, and a short summary of your work"
        )

    for directory in ("docs", "scripts"):
        if not (repo / directory).is_dir():
            errors.append(f"Missing required directory: {directory}/")

    for name in REQUIRED_SCRIPTS:
        path = repo / "scripts" / name
        if not path.is_file():
            errors.append(f"Missing required script: scripts/{name}")
        elif path.stat().st_size == 0:
            errors.append(f"Required script is empty: scripts/{name}")

    images = _images(repo)
    if not images:
        errors.append(
            "No screenshot found in docs/; save the turtlesim window showing "
            "both letters as docs/turtlesim_letters.png"
        )
    else:
        # Any image counts as the deliverable. The filename is a convention,
        # not the skill, so a non-standard name warns rather than fails.
        for image in images:
            if image.suffix.lower() == ".png" and _png_dimensions(image) is None:
                errors.append(f"docs/{image.name} is not a valid PNG image")
        stems = {p.stem.casefold() for p in images}
        if EXPECTED_SCREENSHOT not in stems:
            warnings.warn(
                f"No screenshot named {EXPECTED_SCREENSHOT}.png in docs/; "
                f"found: {', '.join(sorted(p.name for p in images))}"
            )

    for name in REQUIRED_SCRIPTS:
        path = repo / "scripts" / name
        if not path.is_file():
            continue
        first_line = _read_text(path).splitlines()[0].strip() if path.stat().st_size else ""
        if not (first_line.startswith("#!") and ("bash" in first_line or "sh" in first_line)):
            warnings.warn(f"scripts/{name} has an unusual shebang: {first_line!r}")

    return errors


def check_repository_hygiene(repo: Path) -> list[str]:
    if not (repo / ".git").exists():
        return ["Run the grading script inside the cloned Git repository; .git is missing"]

    result = _run_git(repo, "ls-files")
    if result.returncode != 0:
        return ["Could not inspect tracked files with 'git ls-files'"]

    forbidden_names = {"__pycache__", ".pytest_cache", ".DS_Store", "Thumbs.db"}
    tracked = [Path(line) for line in result.stdout.splitlines() if line]
    prohibited = [
        path.as_posix()
        for path in tracked
        if set(path.parts) & forbidden_names or path.suffix in {".pyc", ".pyo"}
    ]
    if prohibited:
        return ["Generated artifacts are tracked: " + ", ".join(prohibited)]
    return []


def _assert_no_errors(errors: list[str]) -> None:
    assert not errors, "\n- " + "\n- ".join(errors)


def test_required_files_and_layout() -> None:
    _assert_no_errors(check_required_files(REPO_ROOT))


def test_repository_hygiene() -> None:
    _assert_no_errors(check_repository_hygiene(REPO_ROOT))
