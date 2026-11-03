"""Export a lexicon sign movement as a Babylon-ready GLB clip.

Builds the keyed arm/hand/neck animation from the SIGNS /
SIGNS_END citation poses in render_host_shots.py and exports
an armature-only .glb whose node names are the cristine DEF
bone names, so the sumerian-hosts gesture queue retargets it
by name (mergeAnimationsTo) and bakes it additive.

Clip layout (72f @ 24fps, gesture phases as comments):
  f1       rest (bind pose, all zeros — the engine base the additive
           clip composes onto is the host bind pose: the idle clip
           does not drive the arm, so sampling rest from the idle
           file mis-registers the reference frame by ~12 degrees and
           lands the hand ~10cm off the chin. zeros == bind exactly,
           so the additive delta starts at true zero)
  f12-f20  chin hold (citation start)
  f20-f44  forward-down arc
  f44-f52  palm-down end hold
  f52-f72  return to rest

Gesture config for the hosts repo gesture.json (babylon frames: the
gltf loader runs at 60fps, so blender frame f plays at f * 2.5).
The queue must DWELL the hold on the citation (chin contact), not
fly through it:
  "thank-you": in {from: 1, to: 30}, hold {from: 30, to: 50},
  out {from: 50, to: 180}

Usage:
  blender -b --factory-startup --python-exit-code 1 \
    -P scripts/blender/export_sign_clip.py -- --sign thank-you \
    --out assets/clips/sign-thank-you.glb
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import render_host_shots as rhs  # noqa: E402


def key_pose(rig, frame, arm, fingers, neck, left=None):
    import bpy
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    for key, bone in (("sh", "char:def_r_shoulder"),
                      ("el", "char:def_r_elbow"),
                      ("wr", "char:def_r_wrist")):
        pb = rig.pose.bones.get(bone)
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = arm[key]
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    for bone_name, rot in rhs.hand_specs("r", fingers):
        pb = rig.pose.bones.get(bone_name)
        if pb is None:
            continue
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = rot
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    if left is not None:
        larm, lfingers = left
        for key, bone in (("sh", "char:def_l_shoulder"),
                          ("el", "char:def_l_elbow"),
                          ("wr", "char:def_l_wrist")):
            pb = rig.pose.bones.get(bone)
            if pb is None:
                continue
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = larm[key]
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
        for bone_name, rot in rhs.hand_specs("l", lfingers):
            pb = rig.pose.bones.get(bone_name)
            if pb is None:
                continue
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = rot
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    pb = rig.pose.bones.get("char:def_c_neckB")
    pb.rotation_mode = "XYZ"
    pb.rotation_euler = neck
    pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    bpy.ops.object.mode_set(mode="OBJECT")


def bind_rest_pose(finger_bones):
    """Rest euler angles for the bake reference frame: bind pose.

    Every entry is (0, 0, 0) — the unposed bone. The engine composes
    the additive clip onto the host bind pose (the idle loop leaves
    the arm at bind, verified in-engine: stopping the idle leaves
    every arm world position unchanged to 4 decimals), so the
    reference frame must be bind, not an idle-sampled pose, for the
    additive delta to start at true zero.
    """
    return {name: (0.0, 0.0, 0.0)
            for name in ("char:def_r_shoulder", "char:def_r_elbow",
                         "char:def_r_wrist", "char:def_c_neckB",
                         "char:def_c_neckA") + tuple(finger_bones)}


def key_eulers(rig, frame, bone_rots):
    """Key explicit per-bone euler rotations (rest keys from sampling)."""
    import bpy
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    for bone_name, rot in bone_rots:
        pb = rig.pose.bones.get(bone_name)
        if pb is None:
            continue
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = rot
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    bpy.ops.object.mode_set(mode="OBJECT")


def main():
    import bpy
    argv = sys.argv[sys.argv.index("--") + 1:]
    sign = "thank-you"
    out = "assets/clips/sign-thank-you.glb"
    rig_name = "cristine"
    for i, arg in enumerate(argv):
        if arg == "--sign" and i + 1 < len(argv):
            sign = argv[i + 1]
        if arg == "--out" and i + 1 < len(argv):
            out = argv[i + 1]
        if arg == "--rig" and i + 1 < len(argv):
            rig_name = argv[i + 1]
        if arg == "--rest-from":
            raise SystemExit("--rest-from was removed: rest keys are "
                             "the bind pose, see module docstring")
    if rig_name not in rhs.RIGS:
        raise SystemExit("unknown --rig %s (choices: %s)"
                         % (rig_name, ", ".join(rhs.RIGS)))

    rhs._HOST_RIG = rig_name
    rig = rhs.load_host(rhs.host_glb())
    # Armature-only clip: drop meshes, keep bone names.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in list(bpy.data.objects):
        if obj.type == "MESH":
            bpy.data.objects.remove(obj, do_unlink=True)
    action = bpy.data.actions.new(sign)
    action.use_fake_user = True
    if rig.animation_data is None:
        rig.animation_data_create()
    rig.animation_data.action = action

    shapes = rhs._load_handshapes()
    start = rhs.SIGNS[sign]
    end = rhs.SIGNS_END[sign]
    b_hand = shapes[start["hand"]]
    # End handshape: most signs hold one shape through the clip;
    # shape-changing signs (HOW-MANY S->5) key the end shape at
    # f44/52 so the morph itself is the movement.
    e_hand = shapes[end.get("hand", start["hand"])]
    bind_hand = {finger: (0.0, 0.0, 0.0) for finger in b_hand}
    bind_hand.update({finger: (0.0, 0.0, 0.0) for finger in e_hand})
    for finger in rhs.RELAXED_HAND_R:
        bind_hand.setdefault(finger, (0.0, 0.0, 0.0))
    bind_arm = {"sh": (0.0, 0.0, 0.0), "el": (0.0, 0.0, 0.0),
                "wr": (0.0, 0.0, 0.0)}
    bind_neck = (0.0, 0.0, 0.0)

    def left_of(which, hand):
        if "lhand" not in which:
            return None
        larm = {"sh": which["lsh"], "el": which["lel"],
                "wr": which["lwr"]}
        return (larm, shapes[which[hand]])

    start_left = left_of(start, "lhand")
    end_left = left_of(end, "lhand") or start_left
    # Rest frames zero every posed finger on both sides so the
    # additive delta starts at true zero (short names expand
    # side-aware in hand_specs).
    if start_left or end_left:
        for side_shapes in (start, end):
            for key in ("lhand",):
                if key in side_shapes:
                    bind_hand.update(
                        {f: (0.0, 0.0, 0.0)
                         for f in shapes[side_shapes[key]]})
    neck_rest = rhs.HEAD_NECK[1]
    neck_nod = (0.16, 0.0, 0.10)

    # Reference frames key the bind pose: the engine composes the
    # additive clip onto the host bind pose (see module docstring).
    # Citation/end frames keep their authored poses (citation neck
    # stays at the authored rest tilt so the chin contact reads).
    key_pose(rig, 1, bind_arm, bind_hand, bind_neck,
             left=(bind_arm, bind_hand) if start_left else None)
    key_pose(rig, 12, start, b_hand, neck_rest, left=start_left)
    key_pose(rig, 20, start, b_hand, neck_rest, left=start_left)
    key_pose(rig, 44, end, e_hand, neck_nod, left=end_left)
    key_pose(rig, 52, end, e_hand, neck_nod, left=end_left)
    key_pose(rig, 72, bind_arm, bind_hand, bind_neck,
             left=(bind_arm, bind_hand) if start_left else None)

    for fc in rhs._all_fcurves(action):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"

    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, 72
    scene.render.fps = 24

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=out, export_format="GLB",
        export_animations=True, export_frame_range=True,
        export_force_sampling=True, export_nla_strips=False,
        export_anim_single_armature=True,
        export_materials="NONE", export_image_format="NONE")
    print("CLIP_OK %s action=%s" % (out, action.name))


if __name__ == "__main__":
    main()
