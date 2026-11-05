import bpy, time
for o in bpy.data.objects:
    if o.type in ("ARMATURE", "EMPTY") and "Icosphere" not in o.name:
        pass
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
            with bpy.context.temp_override(window=window, screen=window.screen, area=area, region=region):
                bpy.ops.view3d.view_all(center=False)
for _ in range(3):
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
    time.sleep(3)
print("HOLD_READY", flush=True)
for _ in range(25):
    time.sleep(3)
