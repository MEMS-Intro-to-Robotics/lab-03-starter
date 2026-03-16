#!/usr/bin/env python3
"""
Autograding validation for Lab 3: Scripting with ROS 2 Topics and Services.
Run with: pytest test_lab_3.py -v
"""

import os
import warnings

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
EXPECTED_SCREENSHOTS = {"turtlesim_letters"}
README_STARTER_FINGERPRINT = "Update this README"


def _get_images(docs_dir="docs"):
    if not os.path.isdir(docs_dir):
        return []
    return [
        f for f in os.listdir(docs_dir)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
    ]


def _read_first_line(path):
    with open(path, "r", errors="replace") as f:
        return f.readline().strip()


# ── Required files (hard fail) ──────────────────────────────


def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md not found"


def test_readme_not_empty():
    assert os.path.getsize("README.md") > 0, "README.md is empty"


def test_readme_updated():
    with open("README.md", "r", errors="replace") as f:
        content = f.read()
    assert README_STARTER_FINGERPRINT not in content, (
        "README.md still contains the starter template text. "
        "Please update it with your name, NetID, and a 1-3 line summary."
    )


def test_docs_directory_exists():
    assert os.path.isdir("docs"), "docs/ directory not found"


def test_scripts_directory_exists():
    assert os.path.isdir("scripts"), "scripts/ directory not found"


def test_turtleletter_exists():
    assert os.path.isfile(
        os.path.join("scripts", "turtleletter.sh")
    ), "scripts/turtleletter.sh not found"


def test_turtleletter_not_empty():
    path = os.path.join("scripts", "turtleletter.sh")
    assert os.path.getsize(path) > 0, "scripts/turtleletter.sh is empty"


def test_turtleletterstwo_exists():
    assert os.path.isfile(
        os.path.join("scripts", "turtleletterstwo.sh")
    ), "scripts/turtleletterstwo.sh not found"


def test_turtleletterstwo_not_empty():
    path = os.path.join("scripts", "turtleletterstwo.sh")
    assert os.path.getsize(path) > 0, "scripts/turtleletterstwo.sh is empty"


# ── Shell script quality (warnings) ─────────────────────────


def test_turtleletter_shebang():
    path = os.path.join("scripts", "turtleletter.sh")
    if not os.path.isfile(path):
        return
    line = _read_first_line(path)
    if not (line.startswith("#!") and ("bash" in line or "sh" in line)):
        warnings.warn(f"turtleletter.sh has unusual shebang: {line!r}")


def test_turtleletterstwo_shebang():
    path = os.path.join("scripts", "turtleletterstwo.sh")
    if not os.path.isfile(path):
        return
    line = _read_first_line(path)
    if not (line.startswith("#!") and ("bash" in line or "sh" in line)):
        warnings.warn(f"turtleletterstwo.sh has unusual shebang: {line!r}")


# ── Screenshots (warnings) ──────────────────────────────────


def test_screenshot_count():
    images = _get_images()
    print(f"\nFound {len(images)} image(s) in docs/:")
    for img in sorted(images):
        print(f"  - {img}")
    if len(images) < 1:
        warnings.warn("Expected at least 1 screenshot, found none")


def test_screenshot_names():
    images = _get_images()
    stems = {os.path.splitext(f)[0].lower() for f in images}
    missing = EXPECTED_SCREENSHOTS - stems
    if missing:
        warnings.warn(
            f"Screenshots with non-standard names. "
            f"Expected names not found: {', '.join(sorted(missing))}"
        )
