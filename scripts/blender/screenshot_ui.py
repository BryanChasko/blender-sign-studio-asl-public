"""True Blender UI screenshots under Xvfb (no display needed).

Loads a rig (and optional clip), frames the viewport, captures
the actual Blender window — menus, outliner, editors included.
Headless `-b` renders pixels; this screenshots the program.

Run from the repo root (COMMITTED protocol, see assets README):

    xvfb-run -a -s "-screen 0 1600x900x24" blender-5.2 \
      --factory-startup \
      -P scripts/blender/screenshot_ui.py -- \
      --rig /path/to/fiona.glb --shot viewport --out out/ui-fiona.png

Shots: `viewport` (fiona framed in the 3D view), `action`
(viewport + thank-you action loaded, for the Dope Sheet tour).
`--clip` points at the sign .glb for the `action` shot.
"""

import argparse
import sys

import bpy


def parse(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--rig", required=True)
    p.add_argument("--clip", default=None)
    p.add_argument("--shot", default="viewport",
                   choices=("viewport", "action"))
    p.add_argument("--out", required=True)
    return p.parse_args(argv)


def view_all():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for region in area.regions:
                if region.type != "WINDOW":
                    continue
                with bpy.context.temp_override(
                        window=window, screen=screen,
                        area=area, region=region):
                    bpy.ops.view3d.view_all(center=False)


def main(argv):
    args = parse(argv)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for coll in bpy.data.collections:
        for obj in list(coll.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=args.rig)
    if args.clip:
        bpy.ops.import_scene.gltf(filepath=args.clip)
        for obj in bpy.data.objects:
            if obj.type == "ARMATURE" and obj.animation_data:
                if obj.animation_data.action:
                    bpy.context.view_layer.objects.active = obj
                    break
    view_all()
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
    bpy.ops.screen.screenshot(filepath=args.out)
    print("SCREENSHOT_OK %s" % args.out)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:])
