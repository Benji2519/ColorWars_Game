import bpy
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parent/'SwordComboRevision'
scene=bpy.context.scene
rig=bpy.data.objects['RIG_CW_BaseSoldier']
scene.render.resolution_x=512;scene.render.resolution_y=512
scene.cycles.samples=6
scene.render.use_persistent_data=True
ground=bpy.data.objects['Combo_PreviewGround']
mat=ground.data.materials[0]
nodes=mat.node_tree.nodes
checker=nodes.new('ShaderNodeTexChecker');checker.inputs['Color1'].default_value=(.09,.11,.14,1);checker.inputs['Color2'].default_value=(.12,.15,.19,1)
checker.inputs['Scale'].default_value=1/70
tex=nodes.new('ShaderNodeTexCoord');mat.node_tree.links.new(tex.outputs['Object'],checker.inputs['Vector'])
mat.node_tree.links.new(checker.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
scene.camera.data.ortho_scale=365
for f in range(0,scene.frame_end+1,2):
 scene.frame_set(f)
 chest=rig.pose.bones['chest'].matrix.translation
 look=Vector((chest.x,chest.y,120))
 scene.camera.location=look+Vector((240,-400,170))
 scene.camera.rotation_euler=(look-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/'Frames'/('combo_%03d.png'%f))
 bpy.ops.render.render(write_still=True)
print('REVISION_RENDER_COMPLETE')
