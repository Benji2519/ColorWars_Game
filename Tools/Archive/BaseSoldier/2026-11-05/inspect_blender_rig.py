import bpy
import json

result = {
    "objects": [{"name": o.name, "type": o.type, "parent": o.parent.name if o.parent else None} for o in bpy.data.objects],
    "armatures": {},
    "actions": [a.name for a in bpy.data.actions],
}

for obj in bpy.data.objects:
    if obj.type != "ARMATURE":
        continue
    result["armatures"][obj.name] = {
        "bones": [b.name for b in obj.data.bones],
        "pose_bones": [b.name for b in obj.pose.bones],
    }

with open(r"C:\Users\sunda\Documents\Unreal Projects\ColorWars\Saved\Codex\inspect_blender_rig.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2)

