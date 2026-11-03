"""
Body-pose naturalness review system.

Uses MediaPipe PoseLandmarker to extract biomechanical metrics and compares
them to an envelope (empirical or literature-based thresholds).

Output: per-render JSON report with overall verdict, per-metric scores, and
front_viewer_assessment with naturalness_score and viewer_perception string.

Usage:
  python3 scripts/qa/body_pose_review.py path/to/render.png path/to/envelope.json

Exit 0 for pass, 1 for warn, 2 for fail (or on model not found).
"""

import json
import sys
from pathlib import Path

try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
except ImportError:
    print("mediapipe not installed", file=sys.stderr)
    sys.exit(1)


# Landmark indices from the spec
POSE_LANDMARKS = {
    "nose": 0,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
}


def compute_angle(a, b, c):
    """Angle at point b formed by segments ba and bc, in degrees."""
    import math
    ba = (a.x - b.x, a.y - b.y, a.z - b.z)
    bc = (c.x - b.x, c.y - b.y, c.z - b.z)
    dot = ba[0] * bc[0] + ba[1] * bc[1] + ba[2] * bc[2]
    norm_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2 + ba[2] ** 2)
    norm_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2 + bc[2] ** 2)
    if norm_ba == 0 or norm_bc == 0:
        return 0.0
    cos_angle = max(-1.0, min(1.0, dot / (norm_ba * norm_bc)))
    return math.degrees(math.acos(cos_angle))


def compute_shoulder_elevation(shoulder, hip):
    """Normalized shoulder elevation: (shoulder.y - hip.y) / (shoulder.y + hip.y + eps)."""
    eps = 1e-6
    return (shoulder.y - hip.y) / (shoulder.y + hip.y + eps)


def point_in_signing_space(landmarks, width_px, height_px):
    """
    Check if hands are within the signing space rectangle.
    Signing space: between shoulders horizontally, below neck, above hips.
    """
    nose = landmarks[POSE_LANDMARKS["nose"]]
    left_shoulder = landmarks[POSE_LANDMARKS["left_shoulder"]]
    right_shoulder = landmarks[POSE_LANDMARKS["right_shoulder"]]
    left_hip = landmarks[POSE_LANDMARKS["left_hip"]]
    right_hip = landmarks[POSE_LANDMARKS["right_hip"]]

    y_min = (left_shoulder.y + right_shoulder.y) / 2
    y_max = (left_hip.y + right_hip.y) / 2
    x_min = min(left_shoulder.x, right_shoulder.x)
    x_max = max(left_shoulder.x, right_shoulder.x)

    for wrist_idx in [POSE_LANDMARKS["left_wrist"], POSE_LANDMARKS["right_wrist"]]:
        w = landmarks[wrist_idx]
        if not (x_min <= w.x <= x_max and y_min <= w.y <= y_max):
            return False
    return True


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <render.png> <envelope.json>", file=sys.stderr)
        sys.exit(1)

    render_path = Path(sys.argv[1])
    envelope_path = Path(sys.argv[2])

    if not render_path.exists():
        print(f"Render not found: {render_path}", file=sys.stderr)
        sys.exit(1)

    if not envelope_path.exists():
        print(f"Envelope not found: {envelope_path}", file=sys.stderr)
        sys.exit(1)

    # Check for MediaPipe model
    model_path = Path.home() / ".cache" / "mediapipe" / "pose_landmarker.task"
    if not model_path.exists():
        print(
            f"Model not found at {model_path}. "
            "Download from https://developers.google.com/mediapipe/solutions/vision/pose_landmarker",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load envelope
    with open(envelope_path) as f:
        envelope = json.load(f)

    # Initialize PoseLandmarker
    base_options = python.BaseOptions(model_asset_path=str(model_path))
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False,
        num_poses=1,
    )
    detector = vision.PoseLandmarker.create_from_options(options)

    # Run inference
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=load_image(render_path))
    detection_result = detector.detect(mp_image)

    if not detection_result.pose_landmarks:
        print("No pose detected", file=sys.stderr)
        sys.exit(1)

    landmarks = detection_result.pose_landmarks[0]

    # Compute metrics
    metrics = {}

    # Elbow flexion (left and right)
    metrics["elbow_flexion_left"] = compute_angle(
        landmarks[POSE_LANDMARKS["left_shoulder"]],
        landmarks[POSE_LANDMARKS["left_elbow"]],
        landmarks[POSE_LANDMARKS["left_wrist"]],
    )
    metrics["elbow_flexion_right"] = compute_angle(
        landmarks[POSE_LANDMARKS["right_shoulder"]],
        landmarks[POSE_LANDMARKS["right_elbow"]],
        landmarks[POSE_LANDMARKS["right_wrist"]],
    )

    # Shoulder flexion (forward bend) - simplified using y coordinate
    left_shoulder = landmarks[POSE_LANDMARKS["left_shoulder"]]
    right_shoulder = landmarks[POSE_LANDMARKS["right_shoulder"]]
    nose = landmarks[POSE_LANDMARKS["nose"]]
    metrics["shoulder_flexion_left"] = compute_angle(
        left_shoulder,
        nose,
        right_shoulder,  # approximate forward lean
    )
    metrics["shoulder_flexion_right"] = metrics["shoulder_flexion_left"]

    # Shoulder abduction/abduction (normalized)
    metrics["shoulder_elevation_left"] = compute_shoulder_elevation(
        left_shoulder, landmarks[POSE_LANDMARKS["left_hip"]]
    )
    metrics["shoulder_elevation_right"] = compute_shoulder_elevation(
        right_shoulder, landmarks[POSE_LANDMARKS["right_hip"]]
    )

    # Lateral splay (elbow-out angle)
    metrics["lateral_splay_left"] = compute_angle(
        landmarks[POSE_LANDMARKS["left_shoulder"]],
        landmarks[POSE_LANDMARKS["left_elbow"]],
        type("P", (), {"x": left_shoulder.x - 0.1, "y": left_shoulder.y, "z": 0})(),
    )
    metrics["lateral_splay_right"] = compute_angle(
        landmarks[POSE_LANDMARKS["right_shoulder"]],
        landmarks[POSE_LANDMARKS["right_elbow"]],
        type("P", (), {"x": right_shoulder.x + 0.1, "y": right_shoulder.y, "z": 0})(),
    )

    # Wrist deviation (bend angle)
    metrics["wrist_deviation_left"] = compute_angle(
        landmarks[POSE_LANDMARKS["left_elbow"]],
        landmarks[POSE_LANDMARKS["left_wrist"]],
        type("P", (), {"x": landmarks[POSE_LANDMARKS["left_wrist"]].x, "y": landmarks[POSE_LANDMARKS["left_wrist"]].y - 0.1, "z": 0})(),
    )
    metrics["wrist_deviation_right"] = compute_angle(
        landmarks[POSE_LANDMARKS["right_elbow"]],
        landmarks[POSE_LANDMARKS["right_wrist"]],
        type("P", (), {"x": landmarks[POSE_LANDMARKS["right_wrist"]].x, "y": landmarks[POSE_LANDMARKS["right_wrist"]].y - 0.1, "z": 0})(),
    )

    # Palm-forward visibility (simplified)
    left_wrist = landmarks[POSE_LANDMARKS["left_wrist"]]
    right_wrist = landmarks[POSE_LANDMARKS["right_wrist"]]
    left_elbow = landmarks[POSE_LANDMARKS["left_elbow"]]
    right_elbow = landmarks[POSE_LANDMARKS["right_elbow"]]

    # If wrist is significantly above elbow, palm likely forward
    metrics["palm_forward_left"] = 1.0 if left_wrist.y < left_elbow.y - 0.05 else 0.5
    metrics["palm_forward_right"] = 1.0 if right_wrist.y < right_elbow.y - 0.05 else 0.5
    metrics["palm_forward_visible_ratio"] = (metrics["palm_forward_left"] + metrics["palm_forward_right"]) / 2

    # Signing-space bounds
    width_px = mp_image.width
    height_px = mp_image.height
    metrics["hands_in_signing_space"] = point_in_signing_space(landmarks, width_px, height_px)

    # Compare to envelope
    verdicts = []
    for name, value in metrics.items():
        if isinstance(value, bool):
            continue  # Skip boolean metrics
        env = envelope.get(name, {})
        p5 = env.get("p5", env.get("threshold_min", 0))
        p95 = env.get("p95", env.get("threshold_max", 100))
        if p5 <= value <= p95:
            verdict = "pass"
        elif name in ["elbow_flexion_left", "elbow_flexion_right"] and (value < 50 or value > 130):
            verdict = "fail"
        elif name in ["lateral_splay_left", "lateral_splay_right"] and value > 35:
            verdict = "fail"
        elif name in ["shoulder_elevation_left", "shoulder_elevation_right"] and value > 0.12:
            verdict = "fail"
        elif name in ["wrist_deviation_left", "wrist_deviation_right"] and value > 25:
            verdict = "fail"
        else:
            verdict = "warn"
        verdicts.append((name, value, p5, p95, verdict))

    # Overall verdict
    if any(v[4] == "fail" for v in verdicts):
        overall_verdict = "fail"
    elif any(v[4] == "warn" for v in verdicts):
        overall_verdict = "warn"
    else:
        overall_verdict = "pass"

    # Front viewer assessment
    naturalness_score = sum(1 for v in verdicts if v[4] == "pass") / len([v for v in verdicts if not isinstance(v[1], bool)])
    flags = [v[0] for v in verdicts if v[4] != "pass"]
    perception = build_perception_string(metrics, verdicts)

    report = {
        "render": str(render_path),
        "overall_verdict": overall_verdict,
        "metrics": {
            name: {"value": val, "range": [p5, p95], "verdict": v}
            for name, val, p5, p95, v in verdicts
        },
        "front_viewer_assessment": {
            "naturalness_score": round(naturalness_score, 2),
            "flags": flags,
            "viewer_perception": perception,
        },
    }

    # Output
    print(json.dumps(report, indent=2))
    sys.exit(0 if overall_verdict == "pass" else (1 if overall_verdict == "warn" else 2))


def load_image(path):
    """Load image as numpy array (RGB)."""
    import cv2
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def build_perception_string(metrics, verdicts):
    """Generate natural-language viewer perception."""
    parts = []
    if metrics.get("hands_in_signing_space"):
        parts.append("hands within signing space")
    else:
        parts.append("hands outside signing space")

    if any(v[4] == "fail" for v in verdicts if v[0].startswith("elbow")):
        parts.append("elbows too bent or extended")

    if any(v[4] == "fail" for v in verdicts if v[0].startswith("lateral_splay")):
        parts.append("elbows too far out")

    if any(v[4] == "fail" for v in verdicts if v[0].startswith("shoulder")):
        parts.append("shoulders raised or in wrong position")

    if any(v[4] == "fail" for v in verdicts if v[0].startswith("wrist")):
        parts.append("wrists bent incorrectly")

    if not parts:
        parts.append("natural signing posture")

    return "; ".join(parts)


if __name__ == "__main__":
    main()
