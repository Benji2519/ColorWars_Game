import bpy,json
from pathlib import Path
from mathutils import Vector
root=Path(r'C:\Users\sunda\Documents\Unreal Projects\ColorWars')
scene=bpy.context.scene
rig=bpy.data.objects['RIG_CW_BaseSoldier']
sword=bpy.data.objects['Sword_01_PREVIEW_SwordSocket']
scene.frame_set(0)
d=json.loads((root/'ArtSource/Characters/BaseSoldier/SwordCombo/manifest.json').read_text())
axis=Vector(d['blade_local'])
hand=rig.pose.bones['hand.R'].matrix.translation
pts=[v.co.dot(axis) for v in sword.data.vertices]
hand_local=sword.matrix_world.inverted() @ hand
report={'sword_matrix':[list(r) for r in sword.matrix_world],'bone_hand_matrix':[list(r) for r in rig.pose.bones['hand.R'].matrix],'actual_blade_world':list((sword.matrix_world.to_3x3() @ axis).normalized()),'actual_hand':list(hand),'grip_axis_projection':hand_local.dot(axis),'mesh_axis_minmax':[min(pts),max(pts)],'mesh_axis_mean':sum(pts)/len(pts),'vertices':len(pts),'uv_layers':list(sword.data.uv_layers.keys())}
(root/'Saved/Codex/SwordCombo/preview_info.json').write_text(json.dumps(report,indent=2))
