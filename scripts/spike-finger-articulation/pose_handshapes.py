"""Day-1 spike, part 2: draft A/B/F/1/5 handshapes for reviewer tuning.

Runs headless on rocmaibox (Blender 4.4.0) against the sibling
sumerian-hosts fixture. NOT a reviewed result: angles below are first
pass drafts for ASLLVD + fluent-signer tuning. See architecture decision record (ADR) 0003.

Usage (rocmaibox, from a checkout of this repo or a copy of this file):

    blender -b --factory-startup --python-exit-code 1 \\
        -P scripts/spike-finger-articulation/pose_handshapes.py -- \\
        --out-dir docs/assets

Writes docs/assets/spike-hand-{a,b,f,n1,n5}.png plus matching
spike-hand-{shape}-prof.png profiles (same pose, camera orbited 90
deg about finger direction) plus prints the angle table to stdout.
Renders go to the asset pipeline or docs/assets, never /tmp.

Handshape drafts (curl 0.0 = extended, 1.0 = full flex, X-axis on
A/B/C joints). Spread is not yet articulated; fingers read as a group
until abduction is validated on the rig.
"""

import argparse
import os
import sys

P = {
    "cristine_glb": os.path.expanduser(
        "~/code/chasko-labs/sumerian-hosts/fixtures/hosts/cristine/cristine.glb"
    ),
    "resolution": (640, 360),
    # Telephoto close-ups (110mm at 1.4m): a level addressee view
    # keeps the face angularly adjacent at 70mm/0.9m (verified
    # intrusion); the longer lens excludes it and flattens finger
    # perspective (good for cheremes).
    "lens": 110,
}

# Draft angles: {handshape: {finger: (A, B, C)}} as flexion amounts
# 0.0 = extended, 1.0 = full flex. Applied about local Z, negative =
# toward the palm (flexion axis found empirically on rocmaibox: X is
# the bone roll axis and barely moves the fingertip; Z-0.9 closed the
# fingertip-to-palm distance from 0.1365 to 0.0546). Right hand;
# mirrored to left by the runner. v0 drafts for reviewer tuning,
# NOT reviewed.

# Chereme presets for close-ups (mirrored in
# render_host_shots.py -- keep the two dicts identical):
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
SHAPES = {
    # A: fist, thumb up alongside
    "a": {"fngThumb": (0.35, 0.2, 0.15), "fngIndex": (1.0, 1.0, 0.8),
          "fngMid": (1.0, 1.0, 0.8), "fngRing": (1.0, 1.0, 0.8),
          "fngPinky": (1.0, 1.0, 0.8)},
    # B: flat hand, thumb across palm (approx: thumb partial curl)
    "b": {"fngThumb": (0.4, 0.2, 0.1), "fngIndex": (0.05, 0.05, 0.05),
          "fngMid": (0.05, 0.05, 0.05), "fngRing": (0.05, 0.05, 0.05),
          "fngPinky": (0.05, 0.05, 0.05)},
    # F: thumb-index circle, others extended. Tip contact solved
    # from bone measurements 2026-10-24 (11.7 mm bone-tip gap):
    # thumb base carries an off-axis term, index-A curls deeper.
    "f": {"fngThumb": ((-0.9, 0.0, -0.5), 0.5, 0.3),
          "fngIndex": ((0.0, 0.0, -0.9), 0.6, 0.4),
          "fngMid": (0.05, 0.05, 0.05), "fngRing": (0.05, 0.05, 0.05),
          "fngPinky": (0.05, 0.05, 0.05)},
    # 1: index up, rest tucked
    "n1": {"fngThumb": (0.9, 0.7, 0.5), "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (1.0, 1.0, 0.8), "fngRing": (1.0, 1.0, 0.8),
           "fngPinky": (1.0, 1.0, 0.8)},
    # 5: open hand
    "n5": {"fngThumb": (0.05, 0.05, 0.05), "fngIndex": (0.05, 0.05, 0.05),
           "fngMid": (0.05, 0.05, 0.05), "fngRing": (0.05, 0.05, 0.05),
           "fngPinky": (0.05, 0.05, 0.05)},
}


def render_shape(shape, out_path, profile=False):
    import bpy

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=P["cristine_glb"])
    rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    # Imported hosts carry a bindpose_offset action on a Non-Linear
    # Animation (NLA) strip that
    # overrides pose-bone transforms at render time. Strip it so hand
    # articulation actually deforms the mesh.
    if rig.animation_data is not None:
        rig.animation_data_clear()
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    angles = SHAPES[shape]
    posed_count = 0
    # Right side only: close-ups frame the right hand. Posing the
    # left arm identically parks it inside the profile camera's
    # view at rest (verified intrusion 2026-10-29); the left side
    # stays in bind pose, out of frame.
    for side in ("r",):
        for finger, (curl_a, curl_b, curl_c) in angles.items():
            for joint, joint_value in (("A", curl_a), ("B", curl_b),
                                       ("C", curl_c)):
                finger_bone = rig.pose.bones.get(
                    "char:def_%s_%s%s" % (side, finger, joint))
                if finger_bone is None:
                    continue
                finger_bone.rotation_mode = "XYZ"
                # Scalar = flexion amount; explicit triple = Euler
                # (thumb base needs off-axis terms — see cookbook).
                if isinstance(joint_value, tuple):
                    finger_bone.rotation_euler = tuple(joint_value)
                else:
                    finger_bone.rotation_euler = (0, 0, -joint_value)
                posed_count += 1
    # Signing Idle baseline: the arm raises into the chest
    # signing box BEFORE handshape values, so the hand presents
    # in signing space. Arm and wrist come from the chereme
    # preset (cardinal numerals default palm-in, letters default
    # palm-out); envs override for trials.
    default_chereme = ("cardinal_numeral" if shape.startswith("n")
                       else "letter_or_digit")
    chereme = os.environ.get("CHEREME", default_chereme)
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
        for bone_name, arm_rot in (
                ("char:def_%s_shoulder" % side, shoulder_rot),
                ("char:def_%s_elbow" % side, elbow_rot)):
            bone = rig.pose.bones.get(bone_name)
            if bone is None:
                continue
            bone.rotation_mode = "XYZ"
            bone.rotation_euler = arm_rot
            posed_count += 1
    # Park the left arm behind the back: a hanging left arm grazes
    # the elevated profile sightline (verified 2026-10-29). Close-ups
    # frame the right hand only.
    for bone_name, arm_rot in (
            ("char:def_l_shoulder", (0.0, 0.35, -0.1)),
            ("char:def_l_elbow", (0.0, -0.1, 0.0))):
            arm_bone = rig.pose.bones.get(bone_name)
            if arm_bone is None:
                continue
            arm_bone.rotation_mode = "XYZ"
            arm_bone.rotation_euler = arm_rot
            posed_count += 1
    # Preset wrist (roll about X = twist, Y = deviation,
    # flex about Z) with env overrides for trials.
    wrist_roll = float(os.environ.get("WRIST_ROLL",
                                      str(preset["roll"])))
    wrist_flex = float(os.environ.get("WRIST_FLEX",
                                      str(preset["flex"])))
    wrist_dev = float(os.environ.get("WRIST_DEV",
                                     str(preset["dev"])))
    if wrist_roll or wrist_flex or wrist_dev:
        for side in ("r",):
            wrist_bone = rig.pose.bones.get("char:def_%s_wrist" % side)
            if wrist_bone is None:
                continue
            wrist_bone.rotation_mode = "XYZ"
            wrist_bone.rotation_euler = (wrist_roll, wrist_dev,
                                         wrist_flex)
            posed_count += 1
    bpy.context.view_layer.update()
    # Bone-derived viewpoint: the camera sits on the palm normal
    # with finger direction mapped to frame-up, so every close-up
    # reads fingers-up; palm vs dorsal follows the chereme preset
    # (cardinal = dorsal). A fixed-viewpoint trial
    # 2026-10-24 clipped fingertips and sprawled the forearm; the
    # identical lens, distance, and idle stance keep the set
    # comparable while per-pose derivation keeps every plate
    # readable. Aim with joint heads only (def-bone tails are
    # unusable on this rig).
    from mathutils import Matrix, Vector
    rig_matrix = rig.matrix_world
    wrist_head = rig_matrix @ rig.pose.bones["char:def_r_wrist"].head
    # Frame from the METACARPAL row (knuckle heads), not the
    # fingertip joint: for fists the tip joint sits inside the curl
    # and the derived camera lands inside the body (verified
    # 2026-10-29 — the A close-up framed the hip). Knuckles give a
    # stable hand direction for open and curled shapes alike.
    middle_knuckle_head = (rig_matrix
                           @ rig.pose.bones["char:def_r_fngMidA"].head)
    middle_tip_head = (rig_matrix
                       @ rig.pose.bones["char:def_r_fngMidC"].head)
    index_knuckle_head = (rig_matrix
                          @ rig.pose.bones["char:def_r_fngIndexA"].head)
    pinky_knuckle_head = (rig_matrix
                          @ rig.pose.bones["char:def_r_fngPinkyA"].head)
    finger_dir = (middle_knuckle_head - wrist_head).normalized()
    palm_normal = (finger_dir.cross(
        pinky_knuckle_head - index_knuckle_head)).normalized()
    if palm_normal.dot(Vector((0, -1, 0))) < 0:
        palm_normal = -palm_normal
    hand_len = (middle_tip_head - wrist_head).length
    cam_target = wrist_head + finger_dir * (hand_len * 0.55)
    cam_distance = float(os.environ.get("PALM_DIST", "1.4"))
    if profile:
        # Profile: orbit 90 deg about finger direction so the palm
        # plane reads edge-on (knuckle-row axis), same target,
        # distance, and finger-up framing as the front still.
        # Leveled: the raw orbit can dip below the hand and frame
        # the face from underneath (verified 2026-10-29), so the
        # world-vertical component is removed for a true side view.
        view_dir = finger_dir.cross(palm_normal)
        view_dir = Vector((view_dir.x, view_dir.y, 0.0))
        if view_dir.length < 1e-6:
            view_dir = Vector((1.0, 0.0, 0.0))
        view_dir = view_dir.normalized()
        # Outward from the body midline: the midline-side view looks
        # straight through the torso (verified 2026-10-29). The camera
        # must sit further from the midline than the hand it frames.
        if view_dir.x * cam_target.x < 0:
            view_dir = -view_dir
        # Cardinals bias the orbit toward the back (+Y): the
        # palm normal's lateral tilt keeps this near edge-on
        # (~7deg), and the behind-side camera drifts the
        # past-hand sightline forward of the face (verified).
        # Letters keep the unbiased outward side.
        if chereme == "cardinal_numeral":
            view_dir = (view_dir + Vector((0.0, 0.4, 0.0))).normalized()
            elev = 0.0
        else:
            elev = 0.15
        view_dir = (view_dir + Vector((0.0, 0.0, elev))).normalized()
    else:
        view_dir = palm_normal
        if chereme == "cardinal_numeral":
            # Cardinals shoot 10deg medial-of-straight (tucked
            # elbow hides behind the hand; shoulder past the
            # frame edge — see render_host_shots.py).
            import math
            medial = -math.copysign(0.18, cam_target.x)
            view_dir = (view_dir
                        + Vector((medial, 0.0, 0.0))).normalized()
    cam_loc = cam_target + view_dir * cam_distance
    cam_forward = (cam_loc - cam_target).normalized()
    cam_up = (finger_dir
              - cam_forward * finger_dir.dot(cam_forward)).normalized()
    cam_right = cam_up.cross(cam_forward).normalized()
    cam_up = cam_forward.cross(cam_right).normalized()
    bpy.ops.object.mode_set(mode="OBJECT")
    cam_data = bpy.data.cameras.new("HandCam")
    # Profiles run tighter (150 vs 110): they are detail witnesses,
    # and the wider lens catches the far arm at the frame edge.
    cam_data.lens = 150 if profile else P["lens"]
    cam = bpy.data.objects.new("HandCam", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam_matrix = Matrix.Identity(4)
    cam_matrix.col[0].xyz = cam_right
    cam_matrix.col[1].xyz = cam_up
    cam_matrix.col[2].xyz = cam_forward
    cam_matrix.col[3].xyz = cam_loc
    cam.matrix_world = cam_matrix
    # Neutral chereme light: big soft frontal sources, gentle rim
    # for edge separation only. No dramatic contrast — curled
    # digits and thumb contact must read, not hide in shadow.
    for light_name, light_off, light_energy, light_size in (
            ("Key", (-0.3, -0.9, 0.4), 120, 1.0),
            ("Fill", (0.5, -0.5, 0.0), 70, 1.0),
            ("Rim", (0.0, 0.6, 0.5), 25, 0.5)):
        light_data = bpy.data.lights.new(light_name, "AREA")
        light_data.energy = light_energy
        light_data.size = light_size
        light_obj = bpy.data.objects.new(light_name, light_data)
        bpy.context.scene.collection.objects.link(light_obj)
        light_obj.location = (cam_target[0] + light_off[0],
                              cam_target[1] + light_off[1],
                              cam_target[2] + light_off[2])
    scene = bpy.context.scene
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        scene.render.engine = "BLENDER_EEVEE"
    # High temporal samples: neutral light exposes EEVEE noise as
    # speckle on skin that reads as surface detail. Renders stay
    # under a minute; chereme stills must be clean.
    try:
        scene.eevee.taa_render_samples = 64
    except Exception:
        pass
    scene.render.resolution_x, scene.render.resolution_y = P["resolution"]
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print("RENDER_OK %s posed=%d" % (out_path, posed_count))
    return posed_count


def main(argv):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--out-dir", required=True)
    arg_parser.add_argument("--shapes", default=",".join(SHAPES))
    arg_parser.add_argument("--chereme", default=None,
                            choices=sorted(CHEREMES))
    args = arg_parser.parse_args(argv)
    if args.chereme is not None:
        os.environ["CHEREME"] = args.chereme
    os.makedirs(args.out_dir, exist_ok=True)
    print("SHAPE_TABLE_V0 (curl A/B/C per finger):")
    for shape_key in SHAPES:
        print("  %s: %s" % (shape_key, SHAPES[shape_key]))
    total = 0
    for shape_key in args.shapes.split(","):
        shape_key = shape_key.strip()
        posed_count = render_shape(
            shape_key,
            os.path.join(args.out_dir, "spike-hand-%s.png" % shape_key))
        total += posed_count
        prof_count = render_shape(
            shape_key,
            os.path.join(args.out_dir,
                         "spike-hand-%s-prof.png" % shape_key),
            profile=True)
        total += prof_count
    print("DONE shapes=%d" % len(args.shapes.split(",")))
    sys.exit(0 if total > 0 else 2)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
