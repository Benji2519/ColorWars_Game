import bpy, json
from pathlib import Path
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
out = {'rig_matrix':[list(r) for r in rig.matrix_world], 'bones':{}, 'scene_scale':bpy.context.scene.unit_settings.scale_length}
for b in rig.data.bones:
    out['bones'][b.name] = {'head':list(b.head_local),'tail':list(b.tail_local),'matrix':[list(r) for r in b.matrix_local], 'parent': b.parent.name if b.parent else None}
out['objects'] = {o.name:{'hide_render':o.hide_render,'location':list(o.location),'scale':list(o.scale),'dimensions':list(o.dimensions)} for o in bpy.data.objects if o.type in ('MESH','CAMERA')}
with open(Path(bpy.data.filepath).parents[2]/'ignore.json','w') if False else open(r'C:\Users\sunda\Documents\Unreal Projects\ColorWars\Saved\Codex\SwordCombo\rig.json','w') as f:
    json.dump(out,f,indent=2)
print('SWORD_RIG_INSPECTED')
