"""Export BaseSoldier using centimetre scene units for Unreal Engine."""

import bpy
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "BaseSoldier.blend"
OUTPUT_BLEND = HERE / "BaseSoldier_UE.blend"
OUTPUT_FBX = HERE / "BaseSoldier_UE.fbx"

bpy.ops.wm.open_mainfile(filepath=str(SOURCE))

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 0.01

rig = next(obj for obj in scene.objects if obj.type == "ARMATURE")
mesh = next(
    obj
    for obj in scene.objects
    if obj.type == "MESH" and obj.name.startswith("SK_CW_BaseSoldier")
)

# Convert metre-based coordinates to centimetre-based coordinates while
# preserving the character's real-world size.
bpy.ops.object.select_all(action="DESELECT")
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
# The skinned mesh is parented to the armature, so scaling the armature also
# scales the mesh. Scaling both would apply the conversion twice.
rig.scale = (100.0, 100.0, 100.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_BLEND))

bpy.ops.object.select_all(action="DESELECT")
rig.select_set(True)
mesh.select_set(True)
bpy.context.view_layer.objects.active = mesh
bpy.ops.export_scene.fbx(
    filepath=str(OUTPUT_FBX),
    use_selection=True,
    object_types={"ARMATURE", "MESH"},
    add_leaf_bones=False,
    bake_anim=False,
    axis_forward="-Y",
    axis_up="Z",
    apply_unit_scale=True,
    apply_scale_options="FBX_SCALE_UNITS",
    mesh_smooth_type="FACE",
    use_armature_deform_only=False,
)

print(f"UNREAL_EXPORT={OUTPUT_FBX}")
print(f"SCENE_SCALE_LENGTH={scene.unit_settings.scale_length}")
print(f"MESH_DIMENSIONS_BU={tuple(round(v, 6) for v in mesh.dimensions)}")
print(
    "PELVIS_HEAD_BU="
    f"{tuple(round(v, 6) for v in rig.data.bones['pelvis'].head_local)}"
)
