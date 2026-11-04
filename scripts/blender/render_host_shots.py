"""Host shots for README and docs. Reusable rig utility, not a one-off.

Runs headless on rocmaibox (Blender 4.4.0) against the sibling
sumerian-hosts fixtures. Renders go to the given output dir
(docs/assets/ or the asset pipeline), never /tmp.

Usage (rocmaibox, from a checkout of this repo or a copy of this file):

    blender -b --factory-startup --python-exit-code 1 \\
        -P scripts/blender/render_host_shots.py -- \\
        --out-dir docs/assets --shot full-body,signing-torso
    blender -b --factory-startup --python-exit-code 1 \\
        -P scripts/blender/render_host_shots.py -- \\
        --out-dir docs/assets --shot number-2,number-3,number-4

Shots: full-body (full body, true rest), signing-neutral (both
arms in the signing-ready stance), signing-torso (right arm
raised, flat hand, torso frame), face-neutral (110mm frontal
face framing, HEAD_NECK zeroed, bind face -- the brow-calibration
baseline), number-2/number-3/number-4 (ASL
number handshape close-ups, v0 drafts for reviewer tuning, NOT
reviewed), torso-{a,b,f,n1,n5,n2,n3,n4} (per-shape in-situ
torso framing: the location/tab witness for each chereme).

Rig facts baked in (see ADR 0003): imported hosts carry a
bindpose_offset Non-Linear Animation (NLA) strip that overrides pose
bones — the script clears animation data first. Finger flexion is
local Z negative (X is the bone roll axis). Amounts are 0.0 extended
to 1.0 full flex.
"""

import argparse
import importlib.util
import os
import sys


def _load_handshapes():
    """Pose dicts for a/b/f/n1/n5/h live in pose_handshapes.py (single
    source of truth, shared with check 2); n2/n3/n4 live in NUMBERS
    below. Merged here so clips and torso shots resolve every
    handshape key. Import by path so this script stays runnable
    standalone."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "..", "spike-finger-articulation",
                       "pose_handshapes.py")
    spec = importlib.util.spec_from_file_location("pose_handshapes", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    shapes = dict(mod.SHAPES)
    shapes.update(NUMBERS)
    return shapes


HOST_NAME = os.environ.get("HOST_NAME", "cristine")

# Fixture root for host rigs. RIG_DIR overrides the default sibling
# sumerian-hosts checkout so the pipeline runs on any workstation
# (gh issue 70); every script in this repo resolves rigs through
# rig_glb() below instead of hardcoding a home directory.
RIG_BASE = os.environ.get(
    "RIG_DIR",
    os.path.expanduser("~/code/chasko-labs/sumerian-hosts/fixtures/hosts"),
)


def rig_glb(host):
    """Fixture path for a host rig (cristine, fiona)."""
    return os.path.join(RIG_BASE, host, host + ".glb")


def _all_fcurves(action):
    """All fcurves on an action, Blender 4.x and 5.x compatible.

    Blender 5.x uses layered actions where fcurves live under
    layers[*].strips[*].channelbags[*] instead of action.fcurves.
    """
    try:
        return list(action.fcurves)
    except AttributeError:
        pass
    out = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                out.extend(channelbag.fcurves)
    return out


P = {
    "cristine_glb": rig_glb("cristine"),
    # Second-host trial (THANK-YOU chin-contact fix): HOST_NAME=fiona
    # swaps every shot to the Fiona fixture. Bone names are the shared
    # char:def_* set; proportions differ, so citation arms re-derive.
    "host_glb": rig_glb(HOST_NAME),
    "hand_res": (640, 360),
    "body_res": (960, 540),
    # Telephoto close-ups (110mm at 1.4m): excludes the face from
    # level addressee views; flattens finger perspective.
    "lens_hand": 110,
    "lens_face": 110,
    "lens_body": 50,
    "lens_full": 35,
    "lights": [("Key", (-0.4, -0.6, 0.6), 150, 0.5),
               ("Fill", (0.5, -0.3, 0.2), 60, 0.5),
               ("Rim", (0.0, 0.5, 0.4), 80, 0.5)],
    # Neutral chereme light for number close-ups: big soft frontal
    # sources, gentle rim for edge separation only (same rig as
    # pose_handshapes.py). Body shots keep the standard rig.
    "lights_soft": [("Key", (-0.3, -0.9, 0.4), 120, 1.0),
                    ("Fill", (0.5, -0.5, 0.0), 70, 1.0),
                    ("Rim", (0.0, 0.6, 0.5), 25, 0.5)],
}

FINGERS = ["fngThumb", "fngIndex", "fngMid", "fngRing", "fngPinky"]

# Chereme presets for number close-ups (mirrored in
# pose_handshapes.py -- keep the two dicts identical):
# cardinal numerals 1-5 cite PALM-IN (Vicars: isolated 1-5 are
# palm-back; the addressee sees the dorsal side), letters and
# digit-strings cite PALM-OUT. Cardinal pronation lives at the
# ELBOW (X roll is rigid distal rotation: zero mesh deformation)
# with a ZERO-twist wrist (bend only: flex + slight deviation).
# A 2.79 wrist-twist trial knotted the wrist mesh into a visible
# pinch/fold (verified damage, reverted same day) — never move
# the big rotation back to the wrist. Measured 2026-10-29,
# verified against Vicars number03 ground truth (frontality
# -0.94, knuckles out, thumb frame-left, smooth wrist).
# Letter arm is the long-standing presentation baseline from
# the cookbook (hand ~29cm forward, neutral wrist, palms flat).
# --chereme / CHEREME selects; IDLE_*/WRIST_* envs override.
CHEREMES = {
    "cardinal_numeral": {"sh": (0.0, -0.4, -0.2), "el": (-2.5, -0.5, 0.0),
                         "roll": 0.0, "flex": -1.0, "dev": 0.1},
    "letter_or_digit": {"sh": (0.0, -0.8, 0.15), "el": (0.0, -0.7, 0.0),
                        "roll": 0.0, "flex": 0.0, "dev": 0.0},
}

# Point hand (Batch-5): n1 fingers with the thumb tucked tighter
# against the palm -- in forward-point arms the n1 thumb reads as
# a dangling second digit (side-view verified). Numbers keep n1.
# Tuck values eye-verified on the YOU side view (Batch-5).
POINT_HAND = {"fngThumb": (1.1, 1.0, 0.8),
              "fngIndex": (0.05, 0.05, 0.05),
              "fngMid": (1.0, 1.0, 0.8), "fngRing": (1.0, 1.0, 0.8),
              "fngPinky": (1.0, 1.0, 0.8)}
# v0 number drafts: flexion per finger (A, B, C). Unreviewed.
# A joint may be an explicit Euler triple (thumb base needs an
# off-axis term to project laterally — see cookbook).
NUMBERS = {"p1": dict(POINT_HAND),
    "n2": {"fngThumb": (0.9, 0.7, 0.5), "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (0.05, 0.05, 0.05), "fngRing": (1.0, 1.0, 0.8),
           "fngPinky": (1.0, 1.0, 0.8)},
    "n3": {"fngThumb": ((0.35, 0.0, -0.05), 0.05, 0.05),
           "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (0.05, 0.05, 0.05), "fngRing": (1.0, 1.0, 0.8),
           "fngPinky": (1.0, 1.0, 0.8)},
    "n4": {"fngThumb": (0.9, 0.7, 0.5), "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (0.05, 0.05, 0.05), "fngRing": (0.05, 0.05, 0.05),
           "fngPinky": (0.05, 0.05, 0.05)},
    # v0 number drafts, palm-forward family: 6-9 touch one digit to
    # the thumb, palm out (Lifeprint numbers1-10; wikihow/quizlet
    # cross-check). Unreviewed.
    # 6: index+middle+ring up, pinky folded to the thumb.
    "n6": {"fngThumb": ((0.3, 0.0, -0.2), 0.5, 0.4),
           "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (0.05, 0.05, 0.05),
           "fngRing": (0.05, 0.05, 0.05),
           "fngPinky": (0.7, 0.6, 0.5)},
    # 7: pinky+middle+index up, ring folded to the thumb.
    "n7": {"fngThumb": ((0.3, 0.0, -0.2), 0.5, 0.4),
           "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (0.05, 0.05, 0.05),
           "fngRing": (0.8, 0.7, 0.6),
           "fngPinky": (0.05, 0.05, 0.05)},
    # 8: index+ring+pinky up, middle folded to the thumb.
    "n8": {"fngThumb": ((0.3, 0.0, -0.2), 0.5, 0.4),
           "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (0.8, 0.7, 0.6),
           "fngRing": (0.05, 0.05, 0.05),
           "fngPinky": (0.05, 0.05, 0.05)},
    # 9: thumb-index circle (ASLLVD labels this token F) plus
    # middle+ring+pinky up.
    "n9": {"fngThumb": ((-0.7, 0.0, -0.4), 0.5, 0.3),
           "fngIndex": ((0.0, -0.1, -0.8), 0.5, 0.3),
           "fngMid": (0.05, 0.05, 0.05),
           "fngRing": (0.05, 0.05, 0.05),
           "fngPinky": (0.05, 0.05, 0.05)},
}

FLAT_HAND = {"fngThumb": (0.08, 0.04, 0.02),
             "fngIndex": (0.01, 0.01, 0.01),
             "fngMid": (0.02, 0.015, 0.01), "fngRing": (0.035, 0.02, 0.01),
             "fngPinky": (0.05, 0.03, 0.02)}

# Relaxed hand for rest / ready / non-dominant staging: fingers
# slightly flexed with the natural cascade (curl increasing
# index -> pinky; uniform curl reads as a claw on a mannequin),
# wrists straight. Never a citation handshape. Per-hand split:
# the right hand's cascade is phase-shifted by one finger (its
# index takes the left mid value, mid takes ring, ring takes
# pinky, pinky stays at the band ceiling) so the two hands are
# no longer mirror-identical. All A values stay in 0.02-0.14.
RELAXED_HAND_L = {"fngThumb": (0.20, 0.12, 0.05),
                  "fngIndex": (0.06, 0.04, 0.02),
                  "fngMid": (0.08, 0.06, 0.03), "fngRing": (0.11, 0.08, 0.04),
                  "fngPinky": (0.14, 0.10, 0.05)}
RELAXED_HAND_R = {"fngThumb": (0.20, 0.12, 0.05),
                  "fngIndex": (0.08, 0.06, 0.03),
                  "fngMid": (0.11, 0.08, 0.04), "fngRing": (0.14, 0.10, 0.05),
                  "fngPinky": (0.14, 0.11, 0.06)}
RELAXED_HAND = RELAXED_HAND_L

# Clasped hands for interpreter neutral: A-joint flexion
# alternates index->pinky between the hands (L high/low/high/
# low, R low/high/low/high) so the extended fingertips interleave
# along the centre seam instead of colliding tip-to-tip. The
# left thumb triple is more opposed (all three joints flexed
# further) so the thumbs cross rather than mirror.
CLASP_HAND_L = {"fngThumb": (0.45, 0.30, 0.18),
                "fngIndex": (0.35, 0.24, 0.12),
                "fngMid": (0.12, 0.08, 0.04), "fngRing": (0.35, 0.24, 0.12),
                "fngPinky": (0.12, 0.08, 0.04)}
CLASP_HAND_R = {"fngThumb": (0.20, 0.12, 0.05),
                "fngIndex": (0.12, 0.08, 0.04),
                "fngMid": (0.35, 0.24, 0.12), "fngRing": (0.12, 0.08, 0.04),
                "fngPinky": (0.35, 0.24, 0.12)}

# Non-dominant arm while the dominant hand signs (torso shots):
# upper arm near the torso, elbow tucked and moderately flexed,
# hand resting at the lower signing space -- not the stiff
# unposed bind diagonal. Shoulder Z takes the same sign as the
# right side on this rig (measured; +Z abducts both arms).
NONDOM_SHOULDER = (0.0, -0.18, -0.30)
NONDOM_ELBOW = (0.0, -1.10, 0.0)

# Slight natural head set on the neck, shared by the body
# stances: real signers hold the head a few degrees off level
# (reference frames: ear-line vs shoulder-line median ~10deg,
# p25 ~6deg; our unposed head measured 0.9deg -- the mannequin
# tell). Subtle pitch + roll, never a grammatical non-manual.
HEAD_NECK = ("char:def_c_neckB", (0.08, 0.0, 0.12))

# Standing stance: the bind pose sets the ankles ~0.49m apart
# (A-frame power stance). Thigh Y -0.14 measured on the rig
# brings the ankles to +-0.155m -- under the shoulders
# (+-0.145m), a relaxed shoulder-width stand.
STANCE_LEGS = [("char:def_l_thigh", (0.0, -0.14, 0.0)),
               ("char:def_r_thigh", (0.0, -0.14, 0.0))]

# Relaxed weight shift for rest / interpreter-neutral only (never
# the active signing torso): pelvis translated toward the
# character's left (+X) foot, spine tilting back so the shoulders
# stay near centre, neck counter-tilting by the full spine total
# so the head keeps the HEAD_NECK set. Measured on the rig
# (survey_joints.py): hip centre +16mm, shoulders +2mm, so
# hip_center_shift_m = +0.014 and shoulder_height_delta_m =
# +0.013 (right shoulder lower); ankles stay within 1mm of the
# STANCE_LEGS positions because the thigh Y offsets below swing
# both ankles back -16mm against the pelvis translation (left
# leg near vertical under the shifted hip, right leg trailing).
# Spine local Z is the lateral-tilt axis; thigh local Y is the
# frontal swing axis and takes opposite signs per side.
WEIGHT_SHIFT_HIP = ("char:def_c_hip", (1.6, 0.0, 0.0))  # 1.6 local = 16mm world (0.01 rig scale)
WEIGHT_SHIFT = [("char:def_c_spineA", (0.0, 0.0, 0.032)),
                ("char:def_c_spineB", (0.0, 0.0, 0.009)),
                ("char:def_c_spineC", (0.0, 0.0, 0.003)),
                ("char:def_c_neckA", (0.0, 0.0, -0.022))]
# HEAD_NECK with the other half of the neck counter-tilt
# (-0.022 total across neckA + neckB cancels the +0.044 spine).
WEIGHT_SHIFT_HEAD_NECK = ("char:def_c_neckB", (0.08, 0.0, 0.098))
WEIGHT_SHIFT_LEGS = [("char:def_l_thigh", (0.0, -0.157, 0.0)),
                     ("char:def_r_thigh", (0.0, -0.123, 0.0))]

# Face: NO neutral face set is applied. Probe of cristine.glb
# (2026-10-30): no shape keys on any mesh (shape_keys is None
# everywhere); the face is driven by DEF bones (brow A/B/C,
# lids, jaw, lips). A symmetric bone-location set (brows/lids
# -0.30/-0.22 local Y, jaw -0.02) was tried and REVERTED the
# same day: at torso scale the brows sat asymmetric (one flat,
# one arched) and the mouth pursed -- the mirrored face bones
# do not take the same local offset symmetrically.
#
# Per-side brow calibration was measured and REVERTED (bind
# face ships, no brow constant is applied): on the face-neutral
# shot (HEAD_NECK zeroed, scripts/qa/measure_brows.py, 3x crop)
# the bind brow-peak-to-eye-line distances are char-R 177.9px /
# char-L 173.0px (gap 4.9px; character-left renders image-right,
# marker-verified via scripts/qa/sweep_brows.py). Brow location
# local-Y is vertical (+Y up, same world sign both sides: +0.5
# local = +5mm world Z per bone; the old symmetric set failed
# on skin response, not axes), and char-L +0.05 / char-R -0.05
# (A/B/C together, 0.05 steps) levels the level face to
# 176.3px / 176.1px (gap 0.2px, mouth/lid pixels unchanged).
# It does NOT ship: at signing-torso scale those offsets move
# the brow peak <1px (measured gap 7.8px -> 8.0px, visually
# indistinguishable), because the torso brow gap has the
# opposite sign and is HEAD_NECK tilt + three-quarter camera
# geometry, not brow skin. Leveling the torso image via brow
# bones would need ~0.3+ local Y and would wreck the level
# face. Revisit only with a head-set/camera change in scope.


# Selectable host rig. Paths mirror the sibling sumerian-hosts
# fixtures layout: fixtures/hosts/<rig>/<rig>.glb.
# --rig overrides the HOST_NAME env (both default cristine).
RIGS = ("cristine", "fiona")

_HOST_RIG = os.environ.get("HOST_NAME", "cristine")
if _HOST_RIG not in RIGS:
    raise SystemExit("unknown HOST_NAME %s (choices: %s)"
                     % (_HOST_RIG, ", ".join(RIGS)))


def host_glb():
    if _HOST_RIG == "cristine":
        return P["cristine_glb"]
    return rig_glb(_HOST_RIG)


def load_host(glb_path):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=glb_path)
    # Pick the newly imported rig from the current scene: stale
    # datablocks from earlier shots in the same process linger in
    # bpy.data and must not be posed instead.
    fresh = [o for o in bpy.context.scene.objects
             if o.type == "ARMATURE" and o not in before]
    rig = fresh[0] if fresh else next(
        o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    if rig.animation_data is not None:
        rig.animation_data_clear()
    return rig


def pose_bones(rig, specs):
    """specs: list of (bone_name, (x, y, z)). Returns posed count."""
    import bpy
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    posed_count = 0
    for bone_name, joint_rot in specs:
        pose_bone = rig.pose.bones.get(bone_name)
        if pose_bone is None:
            continue
        pose_bone.rotation_mode = "XYZ"
        pose_bone.rotation_euler = joint_rot
        posed_count += 1
    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode="OBJECT")
    return posed_count


def pose_locations(rig, specs):
    """specs: list of (bone_name, (x, y, z)) pose-bone locations.
    Returns posed count. Location units are rig-local (0.01 world
    scale, so 1.0 = 10mm world)."""
    import bpy
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    posed_count = 0
    for bone_name, location in specs:
        pose_bone = rig.pose.bones.get(bone_name)
        if pose_bone is None:
            continue
        pose_bone.location = location
        posed_count += 1
    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode="OBJECT")
    return posed_count


def hand_specs(side, angles):
    # A joint value is a flexion scalar (applied as (0, 0, -v)) or
    # an explicit Euler triple for joints like the thumb base that
    # need off-axis components (see cookbook "How to read a pose").
    out = []
    for finger, (curl_a, curl_b, curl_c) in angles.items():
        for joint, joint_value in (("A", curl_a), ("B", curl_b),
                                   ("C", curl_c)):
            if isinstance(joint_value, tuple):
                joint_rot = tuple(joint_value)
            else:
                joint_rot = (0, 0, -joint_value)
            out.append(("char:def_%s_%s%s" % (side, finger, joint),
                        joint_rot))
    return out


def aim_camera(target, offset, lens):
    import bpy
    camd = bpy.data.cameras.new("ShotCam")
    camd.lens = lens
    cam = bpy.data.objects.new("ShotCam", camd)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.location = (target[0] + offset[0], target[1] + offset[1],
                    target[2] + offset[2])
    emp = bpy.data.objects.new("ShotTgt", None)
    bpy.context.scene.collection.objects.link(emp)
    emp.location = target
    con = cam.constraints.new("TRACK_TO")
    con.target = emp
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"


def three_point_lights(target, rig=None):
    import bpy
    for nm, off, energy, size in (rig if rig is not None
                                 else P["lights"]):
        ld = bpy.data.lights.new(nm, "AREA")
        ld.energy = energy
        ld.size = size
        lo = bpy.data.objects.new(nm, ld)
        bpy.context.scene.collection.objects.link(lo)
        lo.location = (target[0] + off[0], target[1] + off[1],
                       target[2] + off[2])


def render_still(path, resolution):
    import bpy
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        scene.render.engine = "BLENDER_EEVEE"
    # High temporal samples: neutral light exposes EEVEE noise as
    # speckle on skin. See pose_handshapes.py.
    try:
        scene.eevee.taa_render_samples = 64
    except Exception:
        pass
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def world_of(rig, bone):
    import bpy
    bpy.context.view_layer.update()
    return rig.matrix_world @ rig.pose.bones[bone].head


def shot_full_body(out):
    import bpy
    rig = load_host(host_glb())
    specs = hand_specs("l", RELAXED_HAND_L) + hand_specs("r", RELAXED_HAND_R)
    # True rest stance (research doc section 5): tall spine, upper
    # arms hanging at the sides with abduction under 20 deg, elbows
    # only slightly bent, wrists straight, loose fingers. Hands rest
    # at the thighs -- this is the between-signs rest a native
    # signer returns to, not a raised ready pose. Shoulder Z is
    # mirrored per side (same-sign Z abducted one arm and adducted
    # the other, the old asymmetric stance).
    # FULL_ARM="shy,shz,el" overrides for posing trials (true axes:
    # shoulder Y- = forward flexion, elbow Y- = flexion).
    import os
    try:
        shoulder_y, shoulder_z, elbow_flex = (
            float(value) for value in os.environ["FULL_ARM"].split(","))
    except KeyError:
        shoulder_y, shoulder_z, elbow_flex = (-0.08, -0.35, -0.30)
    # NOTE: shoulder Z carries the SAME sign on both sides of
    # this rig (measured: +Z abducts both arms); do not mirror it.
    specs += [("char:def_l_shoulder", (0, shoulder_y, shoulder_z)),
              ("char:def_r_shoulder", (0, shoulder_y, shoulder_z)),
              ("char:def_l_elbow", (0, elbow_flex, 0)),
              ("char:def_r_elbow", (0, elbow_flex, 0)),
              WEIGHT_SHIFT_HEAD_NECK] + WEIGHT_SHIFT + WEIGHT_SHIFT_LEGS
    posed_count = pose_bones(rig, specs)
    posed_count += pose_locations(rig, [WEIGHT_SHIFT_HIP])
    aim_target = (0.0, 0.0, 1.05)
    aim_camera(aim_target, (0.0, -5.2, 0.6), P["lens_full"])
    three_point_lights(aim_target)
    render_still(out, P["body_res"])
    print("RENDER_OK %s posed=%d" % (out, posed_count))


def shot_signing_neutral(out):
    """Interpreter neutral: the between-signs stance a working
    interpreter actually holds -- hands gently clasped at the
    waist in front of the torso, upper arms hanging relaxed,
    elbows soft, feet shoulder-width. NOT raised forearms: a
    frozen guard stance is a gaming idle, and reference photos
    of interpreters at rest show hands low, central, and loose
    (reference-images/interpreter/, Wikimedia Commons)."""
    rig = load_host(host_glb())
    specs = hand_specs("l", CLASP_HAND_L) + hand_specs("r", CLASP_HAND_R)
    # Measured on the rig (joint sweep): shoulder X twist turns
    # the flexed forearm medially; X ~1.0-1.15 with elbow
    # -0.82/-0.90 lands the wrists at (+-0.10, -0.11, 1.13) --
    # meeting at the waist, ~11cm in front of the body, right
    # hand a touch higher (a loose clasp, not a mirror pose).
    specs += [("char:def_l_shoulder", READY_POSE["l_shoulder"]),
              ("char:def_r_shoulder", READY_POSE["r_shoulder"]),
              ("char:def_l_elbow", READY_POSE["l_elbow"]),
              ("char:def_r_elbow", READY_POSE["r_elbow"]),
              WEIGHT_SHIFT_HEAD_NECK] + WEIGHT_SHIFT + WEIGHT_SHIFT_LEGS
    posed_count = pose_bones(rig, specs)
    posed_count += pose_locations(rig, [WEIGHT_SHIFT_HIP])
    aim_target = (0.0, 0.0, 1.05)
    aim_camera(aim_target, (0.0, -5.2, 0.6), P["lens_full"])
    three_point_lights(aim_target)
    render_still(out, P["body_res"])
    print("RENDER_OK %s posed=%d" % (out, posed_count))


# Rest / ready stances shared by the stills and the transition
# animation (single source of truth, values as measured in
# shot_full_body / shot_signing_neutral).
REST_POSE = {"l_shoulder": (0.0, -0.08, -0.35),
             "r_shoulder": (0.0, -0.08, -0.35),
             "l_elbow": (0.0, -0.30, 0.0),
             "r_elbow": (0.0, -0.30, 0.0),
             "r_wrist": (0.0, 0.0, 0.0)}
READY_POSE = {"l_shoulder": (1.05, -0.15, -0.30),
              "r_shoulder": (1.15, -0.15, -0.30),
              "l_elbow": (0.0, -0.82, 0.0),
              "r_elbow": (0.0, -0.90, 0.0),
              "r_wrist": (0.0, 0.0, 0.0)}

# Natural signing pose: right arm raised forward into signing space,
# both hands flat. True axes (measured 2026-10-29): shoulder Y-
# flexes forward, elbow Y- flexes. All pre-fix X-twist/Z-deviation
# values parked the hand BEHIND the body (side-view verified).
# See CHANGELOG and docs/cookbook.md for details.
SIGNING_TORSO_POSE = [(0.0, -0.6, -0.18), (0, -1.45, 0)]
# Wrist roll presenting the palm to the front camera (neutral wrist
# faces the palm down with the arm forward; calibrated by render).
TORSO_WRIST_ROLL = 1.5


def shot_signing_torso(out, hand_angles=None, arm=None, left=None):
    """Torso framing with the right arm raised. hand_angles selects
    the handshape (default FLAT_HAND demo): per-shape in-situ
    renders carry the location/tab witness that close-ups lack.
    arm=(shoulder, elbow, wrist) overrides the demo arm -- sign
    poses (SIGNS) pass their citation location arm. left=(angles,
    arm) stages the non-dominant side for two-handed signs
    (default: relaxed hand, tucked elbow)."""
    rig = load_host(host_glb())
    hand = hand_angles if hand_angles is not None else FLAT_HAND
    if left is None:
        specs = hand_specs("l", RELAXED_HAND_L) + hand_specs("r", hand)
    else:
        specs = hand_specs("l", left[0]) + hand_specs("r", hand)
    if arm is None:
        sh, el = SIGNING_TORSO_POSE
        arm = (sh, el, (TORSO_WRIST_ROLL, 0, 0))
    specs += [("char:def_r_shoulder", arm[0]),
              ("char:def_r_elbow", arm[1]),
              ("char:def_r_wrist", arm[2])]
    if left is None:
        specs += [("char:def_l_shoulder", NONDOM_SHOULDER),
                  ("char:def_l_elbow", NONDOM_ELBOW)]
    else:
        specs += [("char:def_l_shoulder", left[1][0]),
                  ("char:def_l_elbow", left[1][1]),
                  ("char:def_l_wrist", left[1][2])]
    specs += [HEAD_NECK]
    posed_count = pose_bones(rig, specs)
    neck = world_of(rig, "char:def_c_neckB")
    wrist = world_of(rig, "char:def_r_wrist")
    aim_target = ((neck[0] + wrist[0]) / 2, (neck[1] + wrist[1]) / 2,
           (neck[2] + wrist[2]) / 2 + 0.10)
    print("TARGET: (%.3f, %.3f, %.3f)" % aim_target)
    aim_camera(aim_target, (0.35, -2.0, 0.45), P["lens_body"])
    three_point_lights(aim_target)
    render_still(out, P["body_res"])
    print("RENDER_OK %s posed=%d" % (out, posed_count))


def brow_location_specs(l_y, r_y):
    """Pose-bone location specs for the six brow bones (local Y is
    vertical on this rig: +Y raises the brow, measured; 1.0 local
    = 10mm at the bone, ~8mm at the brow skin peak for A/B/C
    together). One Y per side, applied to A/B/C together so the
    brow moves as a unit and keeps its arch."""
    out = []
    for side, y in (("l", l_y), ("r", r_y)):
        for joint in ("A", "B", "C"):
            out.append(("char:def_%s_brow%s" % (side, joint),
                        (0.0, y, 0.0)))
    return out


def shot_face_neutral(out, brow_y=None):
    """Frontal face framing for brow calibration: 110mm telephoto
    on the face centre (brow/eye band measured on the rig: brows
    z~1.66, eyes z~1.63, chin z~1.54), HEAD_NECK zeroed so head
    tilt cannot confound brow height, standard three-point lights.
    brow_y is an (l_y, r_y) pair of brow location offsets for
    calibration sweeps; the shipped shot renders the bind face
    (brow_y=None)."""
    rig = load_host(host_glb())
    posed_count = pose_bones(rig, [(HEAD_NECK[0], (0.0, 0.0, 0.0))])
    if brow_y is not None:
        posed_count += pose_locations(
            rig, brow_location_specs(*brow_y))
    aim_target = (0.0, -0.05, 1.615)
    aim_camera(aim_target, (0.0, -1.25, 0.02), P["lens_face"])
    three_point_lights(aim_target)
    render_still(out, P["body_res"])
    print("RENDER_OK %s posed=%d" % (out, posed_count))


def shot_number(name, out, profile=False):
    rig = load_host(host_glb())
    # Right side only: close-ups frame the right hand (see
    # pose_handshapes.py — a posed left arm intrudes at rest).
    specs = hand_specs("r", NUMBERS[name])
    # Signing Idle baseline: both arms raised into the chest signing
    # box BEFORE handshape values (shoulder + elbow), so the hand
    # presents palm-forward with fingers up instead of dangling at
    # the hip. Same stance as the full-body shot.
    # True axis map, measured 2026-10-29 (see pose_handshapes.py):
    # shoulder Y- = forward flexion, elbow Y- = flexion.
    # Presentation arms (see pose_handshapes.py): supinated so the
    # palm faces the addressee at eye level. Left arm parked behind
    # the back (hanging left grazes profiles).
    chereme = os.environ.get("CHEREME", "cardinal_numeral")
    if chereme not in CHEREMES:
        raise SystemExit("unknown CHEREME %r, want one of %s"
                         % (chereme, sorted(CHEREMES)))
    preset = CHEREMES[chereme]
    try:
        shoulder_rot = tuple(float(v)
                             for v in os.environ["IDLE_SH"].split(","))
    except KeyError:
        shoulder_rot = preset["sh"]
    try:
        elbow_rot = tuple(float(v)
                          for v in os.environ["IDLE_EL"].split(","))
    except KeyError:
        elbow_rot = preset["el"]
    for side in ("r",):
        specs += [("char:def_%s_shoulder" % side, shoulder_rot),
                  ("char:def_%s_elbow" % side, elbow_rot)]
    specs += [("char:def_l_shoulder", (0.0, 0.35, -0.1)),
              ("char:def_l_elbow", (0.0, -0.1, 0.0))]
    # Preset wrist (roll about X = twist, Y = deviation,
    # flex about Z) with env overrides for trials.
    wrist_roll = float(os.environ.get("WRIST_ROLL", str(preset["roll"])))
    wrist_flex = float(os.environ.get("WRIST_FLEX", str(preset["flex"])))
    wrist_dev = float(os.environ.get("WRIST_DEV", str(preset["dev"])))
    if wrist_roll or wrist_flex or wrist_dev:
        specs += [("char:def_r_wrist",
                   (wrist_roll, wrist_dev, wrist_flex))]
    posed_count = pose_bones(rig, specs)
    import bpy
    bpy.context.view_layer.update()
    # NOTE: def-bone tails are unusable for aiming (centimeter-unit
    # rig at 0.01 object scale; rest tails sit meters from their
    # heads). Aim with joint heads only; skinning cancels rest length
    # so rotation posing is unaffected.
    #
    # Number-shot camera: bone-derived viewpoint so every
    # still reads fingers-up; palm vs dorsal follows the chereme
    # preset (cardinal = dorsal, see cookbook).
    from mathutils import Matrix, Vector
    rig_matrix = rig.matrix_world
    wrist_head = rig_matrix @ rig.pose.bones["char:def_r_wrist"].head
    # Frame from the METACARPAL row (see pose_handshapes.py): the
    # fingertip joint sits inside the curl on fists and lands the
    # camera inside the body.
    middle_knuckle_head = (rig_matrix
                           @ rig.pose.bones["char:def_r_fngMidA"].head)
    middle_tip_head = (rig_matrix
                       @ rig.pose.bones["char:def_r_fngMidC"].head)
    index_knuckle_head = (rig_matrix
                          @ rig.pose.bones["char:def_r_fngIndexA"].head)
    pinky_knuckle_head = (rig_matrix
                          @ rig.pose.bones["char:def_r_fngPinkyA"].head)
    finger_dir = (middle_knuckle_head - wrist_head).normalized()
    # Bone-derived viewpoint: the camera sits on the palm normal
    # (knuckle-row cross finger-direction, facing the front) with
    # finger direction mapped to frame-up. A fixed-viewpoint trial
    # 2026-10-24 clipped fingertips and sprawled the forearm
    # (evidence kept in the PR); per-pose derivation keeps every
    # plate readable while the identical lens, distance, and idle
    # stance keep the set comparable.
    palm_normal = (finger_dir.cross(
        pinky_knuckle_head - index_knuckle_head)).normalized()
    if palm_normal.dot(Vector((0, -1, 0))) < 0:
        palm_normal = -palm_normal
    # The camera always stays on the addressee side; dorsal vs
    # palm follows the chereme preset (cardinal = dorsal). A
    # behind-signer trial knob (FLIP_SIDE) was removed 2026-10-29:
    # it photographed the signer's view of a palm-out hand, which
    # is not the palm-in citation (see scorecard).
    hand_len = (middle_tip_head - wrist_head).length
    cam_target = wrist_head + finger_dir * (hand_len * 0.55)
    if profile:
        # Profile: orbit 90 deg about finger direction (same math
        # as pose_handshapes.py): re-aimed at the fingers (0.75,
        # not the 0.55 front target), leveled, outward from the
        # midline, elevation per chereme (cardinals look UP ~20deg
        # from below: the hand sits at chin height and a level
        # sightline hits the face dead-center; letters look down
        # ~8deg).
        view_dir = finger_dir.cross(palm_normal)
        view_dir = Vector((view_dir.x, view_dir.y, 0.0))
        if view_dir.length < 1e-6:
            view_dir = Vector((1.0, 0.0, 0.0))
        view_dir = view_dir.normalized()
        if view_dir.x * cam_target.x < 0:
            view_dir = -view_dir
        if chereme == "cardinal_numeral":
            # Cardinals bias the orbit toward the back (+Y): the
            # palm normal's lateral tilt keeps this near edge-on
            # (~7deg), and the behind-side camera drifts the
            # past-hand sightline forward of the face (verified).
            # Letters keep the unbiased outward side.
            view_dir = (view_dir + Vector((0.0, 0.4, 0.0))).normalized()
            elev = 0.0
        else:
            elev = 0.15
        view_dir = (view_dir + Vector((0.0, 0.0, elev))).normalized()
    else:
        view_dir = palm_normal
        if chereme == "cardinal_numeral":
            # Cardinals shoot 10deg medial-of-straight: the tucked
            # elbow and shoulder sit medial-behind the hand, and a
            # dead-frontal camera frames them beside it (verified
            # clutter) while the medial angle hides the elbow
            # behind the hand mass and pushes the shoulder past
            # the frame edge. Dorsal still dominates (98%
            # frontal); letters keep the straight front.
            import math
            medial = -math.copysign(0.18, cam_target.x)
            view_dir = (view_dir
                        + Vector((medial, 0.0, 0.0))).normalized()
    cam_distance = float(os.environ.get("PALM_DIST", "1.4"))
    cam_loc = cam_target + view_dir * cam_distance
    print("CAM: loc=(%.3f, %.3f, %.3f) tgt=(%.3f, %.3f, %.3f) %s" % (
        cam_loc[0], cam_loc[1], cam_loc[2],
        cam_target[0], cam_target[1], cam_target[2],
        "ADDRESSEE-SIDE" if cam_loc[1] < cam_target[1]
        else "BEHIND-SIGNER"))
    cam_forward = (cam_loc - cam_target).normalized()
    cam_up = (finger_dir
              - cam_forward * finger_dir.dot(cam_forward)).normalized()
    cam_right = cam_up.cross(cam_forward).normalized()
    cam_up = cam_forward.cross(cam_right).normalized()
    cam_data = bpy.data.cameras.new("ShotCam")
    cam_data.lens = 150 if profile else P["lens_hand"]
    cam = bpy.data.objects.new("ShotCam", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    cam_matrix = Matrix.Identity(4)
    cam_matrix.col[0].xyz = cam_right
    cam_matrix.col[1].xyz = cam_up
    cam_matrix.col[2].xyz = cam_forward
    cam_matrix.col[3].xyz = cam_loc
    cam.matrix_world = cam_matrix
    bpy.context.scene.camera = cam
    three_point_lights(cam_target, P["lights_soft"])
    render_still(out, P["hand_res"])
    print("RENDER_OK %s posed=%d" % (out, posed_count))


def shot_posture_transition(out):
    """Rest -> ready -> active -> ready -> rest over 96f @ 24fps.

    Reuses REST_POSE / READY_POSE and the active pose from
    shot_signing_torso (SIGNING_TORSO_POSE + NONDOM_* + wrist roll
    + HEAD_NECK). Keys shoulder/elbow/wrist/neck bones with bezier
    interpolation; fingers are keyed too -- relaxed at rest/ready,
    FLAT_HAND on the active (right) hand so the active hold
    matches the shipped signing-torso still instead of arriving
    as a claw. The neck set drifts a few degrees between holds
    (no locked mannequin head). Renders every 2nd frame plus the
    exact hold frames at body resolution into out/ (a directory),
    plus side-view stills of the three holds for elbow/mesh QA.
    """
    import bpy
    rig = load_host(host_glb())
    pose_bones(rig, STANCE_LEGS)
    sh, el = SIGNING_TORSO_POSE
    active = {"l_shoulder": NONDOM_SHOULDER, "r_shoulder": sh,
              "l_elbow": NONDOM_ELBOW, "r_elbow": el,
              "r_wrist": (TORSO_WRIST_ROLL, 0.0, 0.0)}
    bone_map = {"l_shoulder": "char:def_l_shoulder",
                "r_shoulder": "char:def_r_shoulder",
                "l_elbow": "char:def_l_elbow",
                "r_elbow": "char:def_r_elbow",
                "r_wrist": "char:def_r_wrist"}
    keys = [(1, REST_POSE), (20, REST_POSE), (38, READY_POSE),
            (60, active), (78, READY_POSE), (96, REST_POSE)]
    # Slight neck drift between holds (a few degrees of pitch /
    # turn / roll around the HEAD_NECK set, keyed with the arms).
    neck_drift = {1: (0.08, 0.0, 0.12), 20: (0.08, 0.0, 0.12),
                  38: (0.10, 0.05, 0.10), 60: (0.06, -0.04, 0.14),
                  78: (0.10, 0.05, 0.10), 96: (0.08, 0.0, 0.12)}
    # Weight shift keys with rest/ready only; the active hold is
    # centred (zero spine/neckA, STANCE_LEGS, no hip offset), so
    # the bezier keys ease the shift in and out with the arms.
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    neck_bone = HEAD_NECK[0]
    for frame, pose in keys:
        shifted = pose is not active
        for key, bone_name in bone_map.items():
            pb = rig.pose.bones.get(bone_name)
            if pb is None:
                continue
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = pose[key]
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
        pb = rig.pose.bones.get(neck_bone)
        if pb is not None:
            pb.rotation_mode = "XYZ"
            drift = neck_drift[frame]
            if shifted:
                drift = (drift[0], drift[1], drift[2] - 0.022)
            pb.rotation_euler = drift
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
        shift_specs = (WEIGHT_SHIFT + WEIGHT_SHIFT_LEGS if shifted
                       else [(bone, (0.0, 0.0, 0.0))
                             for bone, _ in WEIGHT_SHIFT]
                       + STANCE_LEGS)
        for bone_name, rot in shift_specs:
            pb = rig.pose.bones.get(bone_name)
            if pb is None:
                continue
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = rot
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
        hip_bone, hip_loc = WEIGHT_SHIFT_HIP
        pb = rig.pose.bones.get(hip_bone)
        if pb is not None:
            pb.location = hip_loc if shifted else (0.0, 0.0, 0.0)
            pb.keyframe_insert(data_path="location", frame=frame)
        # Fingers: FLAT on the active right hand, CLASP at the
        # neutral (ready) holds, relaxed at rest; left mirrors
        # the same state with its own dict.
        if pose is active:
            right_angles, left_angles = FLAT_HAND, RELAXED_HAND_L
        elif pose is READY_POSE:
            right_angles, left_angles = CLASP_HAND_R, CLASP_HAND_L
        else:
            right_angles, left_angles = RELAXED_HAND_R, RELAXED_HAND_L
        for bone_name, rot in (hand_specs("r", right_angles)
                               + hand_specs("l", left_angles)):
            pb = rig.pose.bones.get(bone_name)
            if pb is None:
                continue
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = rot
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    bpy.ops.object.mode_set(mode="OBJECT")
    if rig.animation_data and rig.animation_data.action:
        for fc in _all_fcurves(rig.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = "AUTO_CLAMPED"
                kp.handle_right_type = "AUTO_CLAMPED"
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, 96
    try:
        scene.render.fps = 24
    except Exception:
        pass
    aim_target = (0.0, 0.0, 1.05)
    aim_camera(aim_target, (0.0, -5.2, 0.6), P["lens_full"])
    three_point_lights(aim_target)
    os.makedirs(out, exist_ok=True)
    count = 0
    for frame in sorted(set(range(1, 97, 2)) | {38, 60, 78}):
        scene.frame_set(frame)
        render_still(os.path.join(
            out, "frame_%04d.png" % frame), P["body_res"])
        count += 1
    # Side-view hold stills (same poses, camera orbited to +X).
    cam = bpy.context.scene.camera
    cam.location = (aim_target[0] + 5.2, aim_target[1],
                    aim_target[2] + 0.6)
    for label, frame in (("rest", 1), ("ready", 38), ("active", 60)):
        scene.frame_set(frame)
        render_still(os.path.join(out, "side-%s.png" % label),
                     P["body_res"])
    scene.frame_set(1)
    print("RENDER_OK %s frames=%d" % (out, count))


# Lexicon sign poses (working down docs/lexicon.md in order).
# Each entry: handshape key into pose_handshapes.SHAPES plus the
# citation location arm (shoulder, elbow, wrist), derived by
# joint sweep against the citation formation and verified on
# the torso render. Movement is NOT certified by a still (see
# docs/ai-review.md): these are authored key poses.
SIGNS = {
    # HELLO: flat hand beside the forehead, fingers up, palm
    # out (+0.86 frontality measured), then moves outward.
    "hello": {"hand": "b", "sh": (-0.4, -0.95, -0.15),
              "el": (0.0, -1.5, 0.0), "wr": (1.2, 0.0, 0.0)},
    # THANK-YOU (start pose): flat hand at the chin, fingers
    # up, palm toward the signer (-0.69 frontality; pronation
    # shared between the elbow roll, shoulder twist (which also
    # swings the hand to the midline), and -0.45 wrist flexion),
    # then moves forward/down. Checked against Vicars
    # thank-you-01 (fingertips touching the lips): chin-contact
    # fix 2026-11-03, coordinate descent on fiona to gap_lips 13.7mm
    # (was 62.0mm: the hand sat ~55mm lateral of the midline).
    # probe: tip (-0.0128, -0.0508, 1.5505)
    # vs lips (0, -0.056, 1.555). contact verified on the zoomed
    # render, no mesh penetration.
    "thank-you": {"hand": "b", "sh": (1.1, -0.3, -1.0),
                  "el": (-1.9, -1.4, -0.1), "wr": (-0.2, 0.0, -0.45)},
    # Numbers ONE-FIVE share the cardinal-numeral arm (palm-in,
    # dorsal to the addressee, hand in the chest signing box;
    # verified against the Vicars number03 ground truth): the
    # handshape alone distinguishes them. YES/NO/QUESTION stage
    # in the same box; their movement lives in SIGNS_END.
    "one": {"hand": "n1", "sh": (0.0, -0.6, -0.9),
            "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.4)},
    "two": {"hand": "n2", "sh": (0.0, -0.6, -0.9),
            "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.4)},
    "three": {"hand": "n3", "sh": (0.0, -0.6, -0.9),
              "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.4)},
    "four": {"hand": "n4", "sh": (0.0, -0.6, -0.9),
             "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.4)},
    "five": {"hand": "n5", "sh": (0.0, -0.6, -0.9),
             "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.4)},
    # YES: S fist staged in the box, tipped up; the nod flexes
    # the wrist down in SIGNS_END (Lifeprint yes: knock the fist
    # up and down at the wrist).
    "yes": {"hand": "s", "sh": (0.0, -0.6, -0.9),
            "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.1)},
    # NO: H hand staged in the box, fingers level; the snap
    # flexes the wrist down in SIGNS_END (Lifeprint no: snap the
    # index/middle down toward the thumb).
    "no": {"hand": "h", "sh": (0.0, -0.6, -0.9),
           "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.2)},
    # QUESTION: index up staged in the box; the draw curves the
    # wrist sideways in SIGNS_END (Lifeprint question: trace a
    # question mark in the air).
    "question": {"hand": "n1", "sh": (0.0, -0.6, -0.9),
                 "el": (-2.0, -0.5, 0.0), "wr": (0.0, 0.1, -0.4)},
    # Numbers SIX-NINE cite palm-forward (Lifeprint numbers1-10;
    # the flexion arm stages them high, palm out, fingers up --
    # sweep mode palmar). FIRST/SECOND share the arm: index/V up,
    # palm forward, twist in SIGNS_END (Lifeprint first/second).
    "six": {"hand": "n6", "sh": (0.0, -0.9, 0.0),
            "el": (0.5, -1.5, 0.0), "wr": (0.5, 0.1, 0.2)},
    "seven": {"hand": "n7", "sh": (0.0, -0.9, 0.0),
              "el": (0.5, -1.5, 0.0), "wr": (0.5, 0.1, 0.2)},
    "eight": {"hand": "n8", "sh": (0.0, -0.9, 0.0),
              "el": (0.5, -1.5, 0.0), "wr": (0.5, 0.1, 0.2)},
    "nine": {"hand": "n9", "sh": (0.0, -0.9, 0.0),
             "el": (0.5, -1.5, 0.0), "wr": (0.5, 0.1, 0.2)},
    "first": {"hand": "n1", "sh": (0.0, -0.9, 0.0),
              "el": (0.5, -1.5, 0.0), "wr": (0.5, 0.1, 0.2)},
    "second": {"hand": "n2", "sh": (0.0, -0.9, 0.0),
               "el": (0.5, -1.5, 0.0), "wr": (0.5, 0.1, 0.2)},
    # HOW-MANY: two-handed (ASLLVD: dominant+non-dominant start S,
    # end 5). Both open hands face up, staged front-low (sweep mode
    # palms-up). Left side mirrors the right (same Z abducts both).
    "how-many": {"hand": "s", "sh": (0.0, -0.3, -0.9),
                 "el": (-1.0, -0.5, 0.0), "wr": (-0.5, 0.1, -0.4),
                 "lhand": "s", "lsh": (0.0, -0.3, -0.9),
                 "lel": (-1.0, -0.5, 0.0), "lwr": (-0.5, 0.1, -0.4)},
    # Batch-5 point family (ME/YOU/THIS/WHERE/WHO/TRUE): dominant
    # index (n1) staged by the point sweep (align + proximity).
    # YOU/WHERE share the forward-point arm.
    "you": {"hand": "p1", "sh": (0.3, -0.6, -0.9),
            "el": (0.0, -0.5, 0.0), "wr": (0.0, 0.1, 0.4)},
    "where": {"hand": "p1", "sh": (0.3, -0.6, -0.9),
              "el": (-0.3, -0.5, 0.0), "wr": (0.0, 0.1, 0.4)},
    "this": {"hand": "p1", "sh": (0.3, -0.3, -0.9),
             "el": (0.0, -0.5, 0.0), "wr": (0.5, 0.1, 0.4)},
    # WHO: compromise staging (elbow-Y flexion brings the hand to
    # face height but biases the finger left; ely -0.7 keeps the
    # index near-level 30cm out, tip at mouth height; the circle
    # lives in the END offset, movement uncertified).
    "who": {"hand": "p1", "sh": (0.3, -1.2, 0.0),
            "el": (0.0, -0.7, 0.0), "wr": (0.0, 0.1, 0.2)},
    "true": {"hand": "p1", "sh": (0.3, -1.2, 0.0),
             "el": (0.0, -0.5, 0.0), "wr": (0.5, 0.1, 0.4)},
    # ME: lowered thank-you arm (palm-to-signer roll) with deep
    # wrist pitch: fingertip lands on the upper chest, finger
    # pointing back at the body (coordinate descent on stills:
    # sh x 1.1->0.7, wrist x ->1.7, elbow y -1.4->-1.0 to drop the
    # hand off the chin; eye-verified contact, no mesh pinch).
    "me": {"hand": "p1", "sh": (0.7, -0.3, -1.0),
           "el": (-1.9, -1.0, -0.1), "wr": (1.7, 0.0, -0.45)},
}


def _arm_override(prefix, fallback):
    """Joint-sweep trials: SIGN_SH/SIGN_EL/SIGN_WR envs as x,y,z
    override one arm joint for this run (see cookbook joint-sweep
    method). Unset envs keep the SIGNS values."""
    raw = os.environ.get(prefix)
    if raw is None:
        return fallback
    return tuple(float(v) for v in raw.split(","))


def shot_sign(name, out):
    sign = SIGNS[name]
    hand = _load_handshapes()[sign["hand"]]
    arm = (_arm_override("SIGN_SH", sign["sh"]),
           _arm_override("SIGN_EL", sign["el"]),
           _arm_override("SIGN_WR", sign["wr"]))
    left = None
    if "lhand" in sign:
        left = (_load_handshapes()[sign["lhand"]],
                (_arm_override("SIGN_LSH", sign["lsh"]),
                 _arm_override("SIGN_LEL", sign["lel"]),
                 _arm_override("SIGN_LWR", sign["lwr"])))
    return shot_signing_torso(out, hand, arm=arm, left=left)


# Movement end-holds for sign animations: the terminal arm of
# the citation movement, derived the same way as SIGNS (joint
# sweep against the citation end frame).
# THANK-YOU end: hand forward-down at chest height, fingers
# forward, palm down (measured wrist (-0.183,-0.204,1.242),
# fingers (0.18,-0.98,0.08), palm (0.19,-0.05,-0.98)) — the
# Vicars thank-you-02 frame.
SIGNS_END = {
    "thank-you": {"sh": (0.4, -0.3, -0.55), "el": (0.0, -0.85, 0.0),
                  "wr": (0.9, 0.0, 0.0)},
    # HELLO end: the wave finishes a hand-width outward of the
    # forehead, still high, palm out (same wrist as the citation;
    # the travel is shoulder abduction, not a drop).
    "hello": {"sh": (-0.4, -0.95, -0.45), "el": (0.0, -1.5, 0.0),
              "wr": (1.2, 0.0, 0.0)},
    # Numbers: static holds, a small settle separates end from
    # start so the clip reads held, not frozen.
    "one": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.5, 0.0),
            "wr": (0.0, 0.1, -0.35)},
    "two": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.5, 0.0),
            "wr": (0.0, 0.1, -0.35)},
    "three": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.5, 0.0),
              "wr": (0.0, 0.1, -0.35)},
    "four": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.5, 0.0),
             "wr": (0.0, 0.1, -0.35)},
    "five": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.5, 0.0),
             "wr": (0.0, 0.1, -0.35)},
    # YES end: fist nodded down at the wrist.
    "yes": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.5, 0.0),
            "wr": (0.0, 0.1, -0.6)},
    # NO end: wrist snapped down, fingers toward the thumb.
    "no": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.5, 0.0),
           "wr": (0.0, 0.1, -0.7)},
    # QUESTION end: wrist curved sideways, mid-draw.
    "question": {"sh": (0.0, -0.6, -0.9), "el": (-2.0, -0.4, 0.0),
                 "wr": (0.0, 0.5, -0.4)},
    # Numbers: static holds, a small settle separates end from start.
    "six": {"sh": (0.0, -0.9, 0.0), "el": (0.5, -1.5, 0.0),
            "wr": (0.5, 0.1, 0.15)},
    "seven": {"sh": (0.0, -0.9, 0.0), "el": (0.5, -1.5, 0.0),
              "wr": (0.5, 0.1, 0.15)},
    "eight": {"sh": (0.0, -0.9, 0.0), "el": (0.5, -1.5, 0.0),
              "wr": (0.5, 0.1, 0.15)},
    "nine": {"sh": (0.0, -0.9, 0.0), "el": (0.5, -1.5, 0.0),
             "wr": (0.5, 0.1, 0.15)},
    # FIRST/SECOND end: wrist twisted from the citation.
    "first": {"sh": (0.0, -0.9, 0.0), "el": (0.5, -1.5, 0.0),
              "wr": (0.9, 0.1, 0.2)},
    "second": {"sh": (0.0, -0.9, 0.0), "el": (0.5, -1.5, 0.0),
               "wr": (0.9, 0.1, 0.2)},
    # HOW-MANY end: both fists open to 5s, palms up, slight widening.
    "how-many": {"hand": "n5", "sh": (0.0, -0.3, -0.9),
                 "el": (-1.0, -0.5, 0.0), "wr": (-0.5, 0.3, -0.4),
                 "lhand": "n5", "lsh": (0.0, -0.3, -0.9),
                 "lel": (-1.0, -0.5, 0.0), "lwr": (-0.5, 0.3, -0.4)},
    # Batch-5 ends: small settles; YOU pushes forward, WHERE offsets
    # laterally (mid-shake), WHO shifts (mid-circle), TRUE pushes out
    # from the mouth, ME presses to the chest. Movement uncertified.
    "you": {"sh": (0.3, -0.6, -0.9), "el": (0.1, -0.5, 0.0),
            "wr": (0.0, 0.1, 0.4)},
    "where": {"sh": (0.3, -0.6, -0.9), "el": (-0.3, -0.5, 0.0),
              "wr": (0.0, 0.1, 0.7)},
    "this": {"sh": (0.3, -0.3, -0.9), "el": (0.0, -0.5, 0.0),
             "wr": (0.5, 0.1, 0.35)},
    "who": {"sh": (0.3, -1.2, -0.15), "el": (0.0, -0.7, 0.0),
            "wr": (0.0, 0.1, 0.2)},
    "true": {"sh": (0.3, -1.2, 0.0), "el": (0.1, -0.5, 0.0),
             "wr": (0.5, 0.1, 0.4)},
    "me": {"sh": (0.7, -0.3, -1.0), "el": (-1.9, -0.95, -0.1),
           "wr": (1.65, 0.0, -0.45)},
}


def shot_sign_end(name, out):
    sign = SIGNS_END[name]
    hand = _load_handshapes()[sign.get("hand", SIGNS[name]["hand"])]
    left = None
    if "lhand" in sign:
        left = (_load_handshapes()[sign["lhand"]],
                (sign["lsh"], sign["lel"], sign["lwr"]))
    return shot_signing_torso(
        out, hand, arm=(sign["sh"], sign["el"], sign["wr"]), left=left)


def shot_sign_move(name, out):
    """Sign movement clip: THANK-YOU start -> forward-down arc
    -> end hold, 48f @ 24fps (~2s). Keys the citation start arm
    (SIGNS), the end arm (SIGNS_END), and a slight head nod;
    fingers stay in the citation handshape throughout (the end
    frame keeps the flat hand). Bezier interpolation; renders
    every frame to out/ for the mp4 encode:
    ffmpeg -framerate 24 -pattern_type glob -i 'frame_*.png'
    -c:v libx264 -pix_fmt yuv420p <name>.mp4
    """
    import bpy
    rig = load_host(host_glb())
    hand = _load_handshapes()[SIGNS[name]["hand"]]
    specs = (hand_specs("l", RELAXED_HAND_L) + hand_specs("r", hand)
             + [("char:def_l_shoulder", NONDOM_SHOULDER),
                ("char:def_l_elbow", NONDOM_ELBOW)]
             + STANCE_LEGS)
    pose_bones(rig, specs)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    start = SIGNS[name]
    end = SIGNS_END[name]
    keys = [(1, start, HEAD_NECK[1]),
            (12, start, HEAD_NECK[1]),
            (36, end, (0.16, 0.0, 0.10)),
            (48, end, (0.16, 0.0, 0.10))]
    for frame, pose, neck in keys:
        for key, bname in (("sh", "char:def_r_shoulder"),
                           ("el", "char:def_r_elbow"),
                           ("wr", "char:def_r_wrist")):
            pb = rig.pose.bones.get(bname)
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = pose[key]
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
        pb = rig.pose.bones.get("char:def_c_neckB")
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = neck
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    bpy.ops.object.mode_set(mode="OBJECT")
    if rig.animation_data and rig.animation_data.action:
        for fc in _all_fcurves(rig.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = "AUTO_CLAMPED"
                kp.handle_right_type = "AUTO_CLAMPED"
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, 48
    try:
        scene.render.fps = 24
    except Exception:
        pass
    # Frame the whole movement: chin start to chest end.
    aim_target = (-0.09, -0.14, 1.42)
    aim_camera(aim_target, (0.3, -2.1, 0.4), P["lens_body"])
    three_point_lights(aim_target)
    os.makedirs(out, exist_ok=True)
    count = 0
    for frame in range(1, 49):
        scene.frame_set(frame)
        render_still(os.path.join(out, "frame_%04d.png" % frame),
                     P["body_res"])
        count += 1
    scene.frame_set(1)
    print("RENDER_OK %s frames=%d" % (out, count))


def _torso_shots():
    """Per-shape in-situ torso renders (tab witness per chereme)."""
    hands = dict(_load_handshapes())
    hands.update(NUMBERS)
    out = {}
    for key, angles in hands.items():
        out["torso-%s" % key] = (
            "spike-host-torso-%s.png" % key,
            lambda o, a=angles: shot_signing_torso(o, a))
    return out


SHOTS = {
    "full-body": ("spike-host-full-body.png", shot_full_body),
    "signing-neutral": ("spike-host-signing-neutral.png",
                        shot_signing_neutral),
    "signing-torso": ("spike-host-signing-torso.png",
                      lambda out: shot_signing_torso(out)),
    "sign-hello": ("spike-sign-hello.png",
                   lambda out: shot_sign("hello", out)),
    "sign-thank-you": ("spike-sign-thank-you.png",
                       lambda out: shot_sign("thank-you", out)),
    "sign-thank-you-end": ("spike-sign-thank-you-end.png",
                           lambda out: shot_sign_end("thank-you", out)),
    "sign-thank-you-move": ("sign-thank-you-move",
                            lambda out: shot_sign_move("thank-you", out)),
    "sign-hello-end": ("spike-sign-hello-end.png",
                       lambda out: shot_sign_end("hello", out)),
    "sign-yes": ("spike-sign-yes.png",
                 lambda out: shot_sign("yes", out)),
    "sign-yes-end": ("spike-sign-yes-end.png",
                     lambda out: shot_sign_end("yes", out)),
    "sign-no": ("spike-sign-no.png",
                lambda out: shot_sign("no", out)),
    "sign-no-end": ("spike-sign-no-end.png",
                    lambda out: shot_sign_end("no", out)),
    "sign-question": ("spike-sign-question.png",
                      lambda out: shot_sign("question", out)),
    "sign-question-end": ("spike-sign-question-end.png",
                          lambda out: shot_sign_end("question", out)),
    "sign-one": ("spike-sign-one.png",
                 lambda out: shot_sign("one", out)),
    "sign-two": ("spike-sign-two.png",
                 lambda out: shot_sign("two", out)),
    "sign-three": ("spike-sign-three.png",
                   lambda out: shot_sign("three", out)),
    "sign-four": ("spike-sign-four.png",
                  lambda out: shot_sign("four", out)),
    "sign-five": ("spike-sign-five.png",
                  lambda out: shot_sign("five", out)),
    "sign-six": ("spike-sign-six.png",
                 lambda out: shot_sign("six", out)),
    "sign-seven": ("spike-sign-seven.png",
                   lambda out: shot_sign("seven", out)),
    "sign-eight": ("spike-sign-eight.png",
                   lambda out: shot_sign("eight", out)),
    "sign-nine": ("spike-sign-nine.png",
                  lambda out: shot_sign("nine", out)),
    "sign-first": ("spike-sign-first.png",
                   lambda out: shot_sign("first", out)),
    "sign-first-end": ("spike-sign-first-end.png",
                       lambda out: shot_sign_end("first", out)),
    "sign-second": ("spike-sign-second.png",
                    lambda out: shot_sign("second", out)),
    "sign-second-end": ("spike-sign-second-end.png",
                        lambda out: shot_sign_end("second", out)),
    "sign-how-many": ("spike-sign-how-many.png",
                      lambda out: shot_sign("how-many", out)),
    "sign-how-many-end": ("spike-sign-how-many-end.png",
                          lambda out: shot_sign_end("how-many", out)),
    "sign-me": ("spike-sign-me.png", lambda out: shot_sign("me", out)),
    "sign-me-end": ("spike-sign-me-end.png",
                    lambda out: shot_sign_end("me", out)),
    "sign-you": ("spike-sign-you.png",
                 lambda out: shot_sign("you", out)),
    "sign-you-end": ("spike-sign-you-end.png",
                     lambda out: shot_sign_end("you", out)),
    "sign-this": ("spike-sign-this.png",
                  lambda out: shot_sign("this", out)),
    "sign-this-end": ("spike-sign-this-end.png",
                      lambda out: shot_sign_end("this", out)),
    "sign-where": ("spike-sign-where.png",
                   lambda out: shot_sign("where", out)),
    "sign-where-end": ("spike-sign-where-end.png",
                       lambda out: shot_sign_end("where", out)),
    "sign-who": ("spike-sign-who.png",
                 lambda out: shot_sign("who", out)),
    "sign-who-end": ("spike-sign-who-end.png",
                     lambda out: shot_sign_end("who", out)),
    "sign-true": ("spike-sign-true.png",
                  lambda out: shot_sign("true", out)),
    "sign-true-end": ("spike-sign-true-end.png",
                      lambda out: shot_sign_end("true", out)),
    "face-neutral": ("spike-host-face-neutral.png",
                     lambda out: shot_face_neutral(out)),
    "posture-transition": ("posture-transition",
                           shot_posture_transition),
    "number-2": ("spike-hand-number-2.png", lambda out: shot_number("n2", out)),
    "number-3": ("spike-hand-number-3.png", lambda out: shot_number("n3", out)),
    "number-4": ("spike-hand-number-4.png", lambda out: shot_number("n4", out)),
    "number-6": ("spike-hand-number-6.png", lambda out: shot_number("n6", out)),
    "number-7": ("spike-hand-number-7.png", lambda out: shot_number("n7", out)),
    "number-8": ("spike-hand-number-8.png", lambda out: shot_number("n8", out)),
    "number-9": ("spike-hand-number-9.png", lambda out: shot_number("n9", out)),
    "number-2-prof": ("spike-hand-number-2-prof.png",
                      lambda out: shot_number("n2", out, profile=True)),
    "number-3-prof": ("spike-hand-number-3-prof.png",
                      lambda out: shot_number("n3", out, profile=True)),
    "number-4-prof": ("spike-hand-number-4-prof.png",
                      lambda out: shot_number("n4", out, profile=True)),
}
SHOTS.update(_torso_shots())


def main(argv):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--out-dir", required=True)
    arg_parser.add_argument("--shot", default=",".join(
        ["full-body", "signing-torso", "number-2", "number-3", "number-4",
         "number-2-prof", "number-3-prof", "number-4-prof"]))
    arg_parser.add_argument("--chereme", default=None,
                            choices=sorted(CHEREMES))
    arg_parser.add_argument("--rig", default="cristine", choices=list(RIGS))
    args = arg_parser.parse_args(argv)
    global _HOST_RIG
    _HOST_RIG = args.rig
    if args.chereme is not None:
        os.environ["CHEREME"] = args.chereme
    os.makedirs(args.out_dir, exist_ok=True)
    for shot_name in args.shot.split(","):
        shot_name = shot_name.strip()
        fname, fn = SHOTS[shot_name]
        fn(os.path.join(args.out_dir, fname))
    print("DONE shots=%s" % args.shot)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
