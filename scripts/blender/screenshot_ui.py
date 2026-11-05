"""True Blender UI screenshot, session half of the protocol.

Opens the .blend that prepare_ui_blend.py built, hides the
armature, frames the mesh, settles the draws, then HOLDS the
window open so you can capture it from outside. The internal
screenshot operator returns black under Xvfb — capture with
ImageMagick's `import -window root` instead, then kill this
process. Full protocol (run from the repo root, one display):

    Xvfb :98 -screen 0 1600x900x24 &
    LIBGL_ALWAYS_SOFTWARE=1 DISPLAY=:98 blender-5.2 \
      out/ui-fiona.blend --factory-startup \
      -P scripts/blender/screenshot_ui.py -- --hold 75 &
    sleep 40
    DISPLAY=:98 import -window root out/ui-fiona.png
    kill <blender pid>

Why hidden: the fixture's hundred-unit bones display
degenerately under software GL (a solid blob even in STICK
mode), and its 2 m proxy mesh occludes the rig. Hide both for
the working view; renders never draw bones anyway. Details in
assets/README.md ("True UI screenshots").
"""

import argparse
import sys
import time

import bpy


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--hold", type=int, default=75)
    p.add_argument("--shot", default="mesh",
                   choices=("mesh", "action"))
    args = p.parse_args(argv)
    if args.shot == "action":
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.ui_type == "TIMELINE":
                    area.ui_type = "DOPESHEET"
    for o in bpy.data.objects:
        if o.type == "ARMATURE":
            o.hide_viewport = True
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != "VIEW_3D":
                continue
            for region in area.regions:
                if region.type != "WINDOW":
                    continue
                with bpy.context.temp_override(
                        window=window, screen=window.screen,
                        area=area, region=region):
                    bpy.ops.view3d.view_all(center=False)
    for _ in range(3):
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
        time.sleep(3)
    print("HOLD_READY", flush=True)
    time.sleep(args.hold)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:])
