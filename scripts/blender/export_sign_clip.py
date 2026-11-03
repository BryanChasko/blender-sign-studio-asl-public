"""Export a lexicon sign movement as a Babylon-ready GLB clip.

Builds the keyed arm/hand/neck animation from the SIGNS /
SIGNS_END citation poses in render_host_shots.py and exports
an armature-only .glb whose node names are the cristine DEF
bone names, so the sumerian-hosts gesture queue retargets it
by name (mergeAnimationsTo) and bakes it additive.

Clip layout (72f @ 24fps, gesture phases as comments):
  f1       rest (reference frame for the additive bake)
  f12-f20  chin hold (citation start)
  f20-f44  forward-down arc
  f44-f52  palm-down end hold
  f52-f72  return to rest

Gesture config for the hosts repo gesture.json:
  "thank-you": in {from: 12, to: 44}, hold {from: 44, to: 52},
  out {from: 52, to: 72}

Usage:
  blender -b --factory-startup --python-exit-code 1 \
    -P scripts/blender/export_sign_clip.py -- --sign thank-you \
    --out assets/clips/sign-thank-you.glb
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import render_host_shots as rhs  # noqa: E402


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


def key_pose(rig, frame, arm, fingers, neck):
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
    pb = rig.pose.bones.get("char:def_c_neckB")
    pb.rotation_mode = "XYZ"
    pb.rotation_euler = neck
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
    action = bpy.data.actions.new("thank-you")
    action.use_fake_user = True
    if rig.animation_data is None:
        rig.animation_data_create()
    rig.animation_data.action = action

    b_hand = rhs._load_handshapes()[rhs.SIGNS[sign]["hand"]]
    rest = {"sh": (0.0, -0.08, -0.35), "el": (0.0, -0.30, 0.0),
            "wr": (0.0, 0.0, 0.0)}
    start = rhs.SIGNS[sign]
    end = rhs.SIGNS_END[sign]
    neck_rest = rhs.HEAD_NECK[1]
    neck_nod = (0.16, 0.0, 0.10)

    key_pose(rig, 1, rest, rhs.RELAXED_HAND_R, neck_rest)
    key_pose(rig, 12, start, b_hand, neck_rest)
    key_pose(rig, 20, start, b_hand, neck_rest)
    key_pose(rig, 44, end, b_hand, neck_nod)
    key_pose(rig, 52, end, b_hand, neck_nod)
    key_pose(rig, 72, rest, rhs.RELAXED_HAND_R, neck_rest)

    for fc in _all_fcurves(action):
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


main()
