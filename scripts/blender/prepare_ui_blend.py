"""Build the .blend that the UI screenshot opens (headless).

Deletes the default cube, imports the rig (and optional clip),
frames nothing — the screenshot script does that in the GUI.
Run headless first, then open the result under Xvfb:

    blender-5.2 -b --factory-startup \
      -P scripts/blender/prepare_ui_blend.py -- \
      --rig /path/to/fiona.glb --out out/ui-fiona.blend
"""

import argparse
import sys

import bpy


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--rig", required=True)
    p.add_argument("--clip", default=None)
    p.add_argument("--out", required=True)
    args = p.parse_args(argv)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=args.rig)
    # The fixture ships a ~2 m proxy mesh ("Icosphere") that
    # occludes the rig in the viewport. The clips never touch it.
    # Hide it so the working view shows Fiona; adjust the name if
    # a future fixture renames it (the screenshot reveals it).
    proxy = bpy.data.objects.get("Icosphere")
    if proxy is not None:
        proxy.hide_viewport = True
    for obj in bpy.data.objects:
        if obj.type == "ARMATURE":
            # Sumerian armatures arrive in ENVELOPE display: hundred-unit
            # bones blow the envelopes into a solid-looking blob that
            # fills view_selected. Sticks show the real skeleton and
            # frame at true size. Renders never draw bones either way.
            obj.data.display_type = "STICK"
    if args.clip:
        rigs_before = {o.name for o in bpy.data.objects
                       if o.type == "ARMATURE"}
        bpy.ops.import_scene.gltf(filepath=args.clip)
        rigs = [o for o in bpy.data.objects
                if o.type == "ARMATURE" and o.name not in rigs_before]
        rig = rigs[0] if rigs else next(
            (o for o in bpy.data.objects if o.type == "ARMATURE"), None)
        if rig is not None and rig.animation_data:
            act = rig.animation_data.action
            if act is not None:
                for o in bpy.data.objects:
                    if o.type == "ARMATURE" and o is not rig:
                        if o.animation_data is None:
                            o.animation_data_create()
                        o.animation_data.action = act
                        bpy.context.scene.frame_set(36)
    bpy.ops.wm.save_as_mainfile(filepath=args.out)
    print("BLEND_OK %s" % args.out)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:])
