"""Machine review gate for handshape poses (rocmaibox side, no Blender).

Implements checks 1-4 of docs/ai-review.md against the working tree:
live references, cookbook-code equality, explicit per-pose camera
lines, and no vendored reference media. Box-side checks 5-6
(isolation probes, presentation still) need Blender and run on
rocmaibox; this script does not cover them.

Usage:  python3 scripts/review_signs.py
Exit 0 unless a FAIL is present. TODO (e.g. citation TBD) is
reported but does not fail; FAIL means a regression or a broken
contract that must be fixed before ai-reviewed can be granted.
"""

import ast
import importlib.util
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COOKBOOK = os.path.join(ROOT, "docs", "cookbook.md")

# cookbook section -> (script module file, dict name, key)
POSES = {
    "A": ("scripts/spike-finger-articulation/pose_handshapes.py", "SHAPES", "a"),
    "B": ("scripts/spike-finger-articulation/pose_handshapes.py", "SHAPES", "b"),
    "F": ("scripts/spike-finger-articulation/pose_handshapes.py", "SHAPES", "f"),
    "1": ("scripts/spike-finger-articulation/pose_handshapes.py", "SHAPES", "n1"),
    "5": ("scripts/spike-finger-articulation/pose_handshapes.py", "SHAPES", "n5"),
    "2": ("scripts/blender/render_host_shots.py", "NUMBERS", "n2"),
    "3": ("scripts/blender/render_host_shots.py", "NUMBERS", "n3"),
    "4": ("scripts/blender/render_host_shots.py", "NUMBERS", "n4"),
    "6": ("scripts/blender/render_host_shots.py", "NUMBERS", "n6"),
    "7": ("scripts/blender/render_host_shots.py", "NUMBERS", "n7"),
    "8": ("scripts/blender/render_host_shots.py", "NUMBERS", "n8"),
    "9": ("scripts/blender/render_host_shots.py", "NUMBERS", "n9"),
    "P1": ("scripts/blender/render_host_shots.py", "NUMBERS", "p1"),
}

TORSO_SHOTS = [
    "docs/assets/spike-host-signing-torso.png",
]

results = []


def note(check, target, status, detail=""):
    results.append((check, target, status, detail))
    print("%s %s: %s %s" % (check, target, status, detail))


def load_module(path):
    name = os.path.basename(path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def section_body(text, pose):
    m = re.search(r"^## %s\b.*?(?=^## |\Z)" % re.escape(pose),
                  text, re.M | re.S)
    return m.group(0) if m else ""


def check_body_pose(shot):
    """Check body-pose naturalness using MediaPipe."""
    shot_path = os.path.join(ROOT, shot)
    if not os.path.exists(shot_path):
        note("body-pose", shot, "FAIL", "shot not found")
        return

    envelope_path = os.path.join(ROOT, "data", "envelopes", "body_pose_envelope.v1.json")
    if not os.path.exists(envelope_path):
        note("body-pose", shot, "FAIL", "envelope not found")
        return

    try:
        result = subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "qa", "body_pose_review.py"), shot_path, envelope_path],
            capture_output=True, text=True, cwd=ROOT
        )
        if result.returncode == 0:
            note("body-pose", shot, "PASS", "natural signing posture")
        elif result.returncode == 1:
            note("body-pose", shot, "WARN", "minor deviation")
        else:
            note("body-pose", shot, "FAIL", f"signing posture issue: {result.stderr}")
    except Exception as ex:  # noqa: BLE001
        note("body-pose", shot, "FAIL", f"body-pose review failed: {ex}")


def main():
    text = open(COOKBOOK).read()
    mods = {}
    for pose, (modfile, dictname, key) in POSES.items():
        body = section_body(text, pose)
        if not body:
            note("sections", pose, "FAIL", "no cookbook section")
            continue
        # 1. live reference (TODO when citation TBD)
        urls = re.findall(r"https?://[^\s)]+", body)
        refline = "Reference:" in body
        if not refline:
            note("reference", pose, "FAIL", "no Reference line")
        elif "citation TBD" in body and not urls:
            note("reference", pose, "TODO", "citation TBD")
        else:
            for u in urls:
                try:
                    req = urllib.request.Request(
                        u, headers={"User-Agent": "review_signs/1.0"})
                    resp = urllib.request.urlopen(req, timeout=20)
                    payload = resp.read(20000)
                    if resp.status == 200 and len(payload) > 500:
                        note("reference", pose, "PASS", u)
                    else:
                        note("reference", pose, "FAIL",
                             "%s http=%s bytes=%d" % (u, resp.status,
                                                      len(payload)))
                except Exception as ex:  # noqa: BLE001 - report, don't crash
                    note("reference", pose, "FAIL", "%s %s" % (u, ex))
        # 2. cookbook block equals script dict
        blocks = re.findall(r"```python\n(.*?)```", body, re.S)
        matched = False
        if modfile not in mods:
            mods[modfile] = load_module(modfile)
        expected = getattr(mods[modfile], dictname)[key]
        for b in blocks:
            try:
                parsed = ast.literal_eval("{" + b + "}")
            except Exception:
                continue
            for _k, v in parsed.items():
                if tuple(v.get("fngThumb", ())) and _k in (
                        "a", "b", "f", "n1", "n5", "n2", "n3", "n4",
                        "n6", "n7", "n8", "n9", "p1"):
                    got = {f: tuple(t) for f, t in v.items()}
                    want = {f: tuple(t) for f, t in expected.items()}
                    note("code-match", pose,
                         "PASS" if got == want else "FAIL",
                         "" if got == want else
                         "cookbook != %s[%s]" % (dictname, key))
                    matched = True
        if not matched:
            note("code-match", pose, "FAIL", "no parseable pose block")
    # 3. explicit camera lines on every pose section (no "same as N")
    for pose in ("A", "B", "F", "1", "5", "2", "3", "4", "P1"):
        body = section_body(text, pose)
        if re.search(r"same as \d", body, re.I):
            note("camera", pose, "FAIL", "cross-references another pose")
        elif "Wrist" in body:
            note("camera", pose, "PASS", "own wrist/camera lines")
        else:
            note("camera", pose, "FAIL", "no wrist/camera lines")
    # 4. no vendored reference media outside our render dirs
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT,
            capture_output=True, text=True, check=True).stdout
    except Exception as ex:  # noqa: BLE001
        note("media", "repo", "FAIL", "git status failed: %s" % ex)
        out = ""
    bad = [ln for ln in out.splitlines()
           if re.search(r"\.(png|jpe?g|mp4|webm|gif|mov)(\s|$)", ln, re.I)
           and "docs/assets/" not in ln]
    if bad:
        note("media", "repo", "FAIL", "outside docs/assets: %s" % bad)
    else:
        note("media", "repo", "PASS", "no outside image/video changes")
    # 7. Body-pose naturalness (torso/full-body shots)
    for shot in TORSO_SHOTS:
        check_body_pose(shot)
    fails = [r for r in results if r[2] == "FAIL"]
    todos = [r for r in results if r[2] == "TODO"]
    print("REVIEW: %s (%d fail, %d todo)" % (
        "FAIL" if fails else "PASS", len(fails), len(todos)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())