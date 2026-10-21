"""Author three connected sword attacks on the original BaseSoldier rig.

Run with Blender in background, opening BaseSoldier_UE.blend first.
Uses the actual Unreal Sword_01 mesh and the exported SwordSocket transform.
"""
import bpy
import json
import math
import sys
from pathlib import Path
import numpy as np
from mathutils import Matrix, Quaternion, Vector

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / 'Saved' / 'Codex' / 'SwordCombo'
OUT = Path(__file__).resolve().parent / 'SwordCombo'
OUT.mkdir(parents=True, exist_ok=True)
data = json.loads((WORK / 'prepare.json').read_text(encoding='utf-8'))
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
body = bpy.data.objects['SK_CW_BaseSoldier_v3']
scene = bpy.context.scene
scene.render.fps = 30
scene.render.fps_base = 1.0
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.01

def ue_matrix(t):
    x,y,z,w = t['rotation']
    return Matrix.LocRotScale(Vector(t['translation']),Quaternion((w,x,y,z)),Vector(t['scale']))

C = Matrix.Diagonal((1.,-1.,1.,1.))
def mapped_bone(name, pose):
    key = name.replace('.','_').lower()
    ref = {k.lower():v for k,v in data['reference'].items()}[key]
    val = {k.lower():v for k,v in pose.items()}[key]
    return C @ ue_matrix(val) @ ue_matrix(ref).inverted() @ C @ rig.data.bones[name].matrix_local

for o in list(scene.objects):
    if o.type == 'MESH' and o != body:
        o.hide_render = True
        o.hide_set(True)

# Import the real weapon; FBX importer expresses centimetres in scene units.
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=str(WORK/'Sword_01.fbx'),use_anim=False)
scene.render.fps = 30
scene.render.fps_base = 1.0
imported_meshes = [o for o in bpy.data.objects if o not in before and o.type == 'MESH']
for obj in imported_meshes:
    if obj.name.startswith(('UCX_','UBX_','UCP_','USP_')):
        obj.hide_render=True
        obj.hide_set(True)
sword_parts = [o for o in imported_meshes if not o.name.startswith(('UCX_','UBX_','UCP_','USP_'))]
assert sword_parts, 'Sword_01 FBX contained no mesh'
bpy.ops.object.select_all(action='DESELECT')
for o in sword_parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = sword_parts[0]
if len(sword_parts) > 1:
    bpy.ops.object.join()
sword = bpy.context.view_layer.objects.active
sword.name = 'Sword_01_PREVIEW_SwordSocket'
# Normalize imported geometry into Blender centimetre coordinates.
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
coords = np.array([list(v.co) for v in sword.data.vertices])
extent = np.ptp(coords,axis=0).max()
if extent < 10:
    for v in sword.data.vertices:
        v.co *= 100
coords = np.array([list(v.co) for v in sword.data.vertices])
cov = np.cov(coords.T)
eigvals,eigvecs = np.linalg.eigh(cov)
blade = Vector(eigvecs[:,np.argmax(eigvals)])
normal = Vector(eigvecs[:,np.argmin(eigvals)])
normal = (normal - blade*normal.dot(blade)).normalized()
idle_hand = mapped_bone('hand.R',data['idle'])
idle_socket = C @ ue_matrix(data['socket_world']) @ C
sword_local = idle_hand.inverted() @ idle_socket
# Point towards the blade tip, away from the grip/pommel cluster.
grip = sword_local.inverted().translation
if (Vector(coords.mean(axis=0))-grip).dot(blade) < 0:
    blade.negate()
blade_hand = (sword_local.to_3x3() @ blade).normalized()
normal_hand = (sword_local.to_3x3() @ normal).normalized()
sword.parent = rig
sword.parent_type = 'BONE'
sword.parent_bone = 'hand.R'
# Bone parenting uses its tail as the origin, compensated here.
sword.matrix_parent_inverse = Matrix.Identity(4)
sword.matrix_basis = Matrix.Translation((0,-rig.data.bones['hand.R'].length,0)) @ sword_local
sword.hide_render = False
sword.hide_set(False)

def mat(name,color,metallic=0,roughness=.35):
    m = bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=roughness
    return m

steel=mat('SwordCombo_PreviewSteel',(.35,.55,.65),.75,.22)
sword.data.materials.clear()
sword.data.materials.append(steel)
bs=steel.node_tree.nodes.get('Principled BSDF')
tex=steel.node_tree.nodes.new('ShaderNodeTexImage')
tex.image=bpy.data.images.load(str(WORK/'T_Sword_Newbie_01_Bl_D.png'))
tex.image.pack()
steel.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
uv=steel.node_tree.nodes.new('ShaderNodeUVMap')
uv.uv_map='UVmap_0'
steel.node_tree.links.new(uv.outputs['UV'],tex.inputs['Vector'])
for poly in sword.data.polygons:poly.material_index=0

rest = {b.name:b.matrix_local.copy() for b in rig.data.bones}
for pb in rig.pose.bones:
    pb.rotation_mode='QUATERNION'
    for constraint in list(pb.constraints):
        pb.constraints.remove(constraint)
rig.animation_data_clear()

def set_world(name,matrix):
    rig.pose.bones[name].matrix=matrix
    bpy.context.view_layer.update()

def follow_rest(name):
    pb=rig.pose.bones[name]
    if pb.parent:
        return pb.parent.matrix @ rest[pb.parent.name].inverted() @ rest[name]
    return rest[name].copy()

def align_bone(name,head,direction):
    # Minimal rotation from rest orientation keeps the imported bone roll.
    ref=rest[name].to_quaternion()
    src=ref @ Vector((0,1,0))
    rot=src.rotation_difference(direction.normalized()) @ ref
    set_world(name,Matrix.LocRotScale(head,rot,Vector((1,1,1))))

def solve_limb(upper,lower,end,target,pole,end_rotation=None):
    shoulder=follow_rest(upper).translation
    l1=rig.data.bones[upper].length
    l2=rig.data.bones[lower].length
    direction=target-shoulder
    distance=min(max(direction.length,abs(l1-l2)+.05),l1+l2-.15)
    axis=direction.normalized()
    p=pole-shoulder
    p=(p-axis*p.dot(axis)).normalized()
    along=(l1*l1-l2*l2+distance*distance)/(2*distance)
    height=math.sqrt(max(0,l1*l1-along*along))
    elbow=shoulder+axis*along+p*height
    wrist=shoulder+axis*distance
    align_bone(upper,shoulder,elbow-shoulder)
    align_bone(lower,elbow,wrist-elbow)
    if end_rotation is not None:
        set_world(end,Matrix.LocRotScale(wrist,end_rotation,Vector((1,1,1))))
    return wrist

def frame_basis(axis,normal):
    z=axis.normalized()
    x=(normal-z*normal.dot(z)).normalized()
    y=z.cross(x).normalized()
    return Matrix((x,y,z)).transposed()

local_sword_basis=frame_basis(blade_hand,normal_hand)

# Each pose specifies wrist, blade direction, body turn, lean and weight shift.
def P(wrist,blade,yaw=0,lean=4,shift=0,drop=3):
    return {'wrist':Vector(wrist),'blade':Vector(blade).normalized(),'yaw':yaw,'lean':lean,'shift':shift,'drop':drop}

ready=P((-29,-27,111),(-.25,-.30,.92),-5,4,0,3)
load1=P((-45,3,135),(-.45,.15,.88),20,0,-2,4)
hit1=P((-12,-44,112),(.62,-.70,-.35),-8,8,1,5)
end1=P((4,-23,100),(.80,-.30,-.52),-25,6,2,4)
load2=P((6,-18,116),(.75,.12,.65),-30,2,2,5)
hit2=P((-12,-43,119),(-.80,-.58,.1),0,7,-1,5)
end2=P((-44,-12,121),(-.85,-.2,.48),22,3,-2,4)
load3=P((-12,2,158),(0,.18,.98),6,-5,0,3)
hit3=P((-13,-42,105),(.05,-.9,-.43),-2,13,0,7)
low3=P((-24,-26,84),(.08,-.7,-.7),-8,10,1,6)

clips=[
    ('AS_BaseSoldier_Attack_Sword_01',[(0,ready),(7,load1),(10,load1),(15,hit1),(21,end1)]),
    ('AS_BaseSoldier_Attack_Sword_02',[(0,end1),(6,load2),(9,load2),(14,hit2),(21,end2)]),
    ('AS_BaseSoldier_Attack_Sword_03',[(0,end2),(9,load3),(12,load3),(18,hit3),(23,low3),(33,ready)]),
]

def pose_at(keys,frame):
    for i in range(len(keys)-1):
        a,pa=keys[i]; b,pb=keys[i+1]
        if frame<=b:
            t=max(0,min(1,(frame-a)/(b-a)))
            t=t*t*(3-2*t)
            return {k:(pa[k].lerp(pb[k],t) if isinstance(pa[k],Vector) else pa[k]*(1-t)+pb[k]*t) for k in pa}
    return keys[-1][1]

def apply_pose(p):
    for pb in rig.pose.bones:
        pb.matrix_basis=Matrix.Identity(4)
    bpy.context.view_layer.update()
    yaw=math.radians(p['yaw'])
    pelvis=rest['pelvis'].copy()
    pelvis.translation += Vector((p['shift'],0,-p['drop']))
    pelvis=Matrix.Translation(pelvis.translation) @ Matrix.Rotation(yaw*.25,4,'Z') @ rest['pelvis'].to_3x3().to_4x4()
    set_world('pelvis',pelvis)
    for name,weight in [('spine',.40),('chest',.35)]:
        base=follow_rest(name)
        rot=Matrix.Rotation(yaw*weight,4,'Z') @ Matrix.Rotation(math.radians(p['lean'])*weight,4,'X')
        base=Matrix.Translation(base.translation) @ rot @ base.to_3x3().to_4x4()
        set_world(name,base)
    # Head follows the action while remaining aimed towards the opponent.
    base=follow_rest('neck')
    set_world('neck',Matrix.Translation(base.translation) @ Matrix.Rotation(-yaw*.55,4,'Z') @ base.to_3x3().to_4x4())
    for side in ('R','L'):
        target=Vector((-16,8,18) if side=='R' else (16,-9,18))
        solve_limb('thigh.'+side,'shin.'+side,'foot.'+side,target,Vector((target.x,-45,42)),rest['foot.'+side].to_quaternion())
    hand_rot=(frame_basis(p['blade'],Vector((0,-1,.15))) @ local_sword_basis.inverted()).to_quaternion()
    solve_limb('upper_arm.R','forearm.R','hand.R',p['wrist'],Vector((-65,-10,112)),hand_rot)
    # Free hand stays in guard and reacts subtly with the body.
    left=Vector((26,-23,112+p['lean']*.1))
    leftrot=mapped_bone('hand.L',data['idle']).to_quaternion()
    solve_limb('upper_arm.L','forearm.L','hand.L',left,Vector((56,-5,105)),leftrot)
    # Preserve the closed grip from the existing sword idle, relative to each parent.
    for pb in rig.pose.bones:
        if pb.name.startswith(('finger','thumb')):
            pose_m=mapped_bone(pb.name,data['idle'])
            parent_m=mapped_bone(pb.parent.name,data['idle'])
            set_world(pb.name,pb.parent.matrix @ parent_m.inverted() @ pose_m)

manifest={'clips':[], 'sword_extent_cm':np.ptp(coords,axis=0).tolist(),'blade_local':list(blade),'blade_hand':list(blade_hand)}
for name,keys in clips:
    action=bpy.data.actions.new(name)
    action.use_fake_user=True
    rig.animation_data_create()
    rig.animation_data.action=action
    end=keys[-1][0]
    for frame in range(end+1):
        scene.frame_set(frame)
        apply_pose(pose_at(keys,frame))
        for pb in rig.pose.bones:
            pb.keyframe_insert('location',frame=frame,group=pb.name)
            pb.keyframe_insert('rotation_quaternion',frame=frame,group=pb.name)
            pb.keyframe_insert('scale',frame=frame,group=pb.name)
    scene.frame_start=0; scene.frame_end=end
    bpy.ops.object.select_all(action='DESELECT')
    rig.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.fbx(filepath=str(OUT/(name+'.fbx')),use_selection=True,object_types={'ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=False,bake_anim_force_startend_keying=True,bake_anim_step=1,bake_anim_simplify_factor=0,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',use_armature_deform_only=False)
    manifest['clips'].append({'name':name,'frames':end,'seconds':end/30,'file':str(OUT/(name+'.fbx'))})

# One continuous review action with shared boundary frames, matching the clips.
action=bpy.data.actions.new('SwordCombo_01_02_03_PREVIEW')
action.use_fake_user=True
rig.animation_data.action=action
frame_offset=0
for name,keys in clips:
    for frame in range(keys[-1][0]+1):
        scene.frame_set(frame_offset+frame)
        apply_pose(pose_at(keys,frame))
        for pb in rig.pose.bones:
            pb.keyframe_insert('location',frame=frame_offset+frame,group=pb.name)
            pb.keyframe_insert('rotation_quaternion',frame=frame_offset+frame,group=pb.name)
            pb.keyframe_insert('scale',frame=frame_offset+frame,group=pb.name)
    frame_offset+=keys[-1][0]
scene.frame_start=0;scene.frame_end=frame_offset

# Studio setup at centimetre scale; source meshes and rig stay untouched on disk.
for o in scene.objects:
    if o.type=='LIGHT':
        o.hide_render=True
world=scene.world or bpy.data.worlds.new('SwordComboWorld')
scene.world=world
world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.055,.075,.10,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.45
def area(name,location,power,size):
    d=bpy.data.lights.new(name,'AREA');d.energy=power*10000;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=location
    o.rotation_euler=(Vector((0,0,95))-o.location).to_track_quat('-Z','Y').to_euler()
area('Combo_Key',(130,-220,300),1500,160)
area('Combo_Fill',(-180,-100,170),950,150)
area('Combo_Rim',(80,160,260),1900,130)
bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,0))
ground=bpy.context.object;ground.name='Combo_PreviewGround';ground.data.materials.append(mat('Combo_Ground',(.07,.09,.12),0,.8))
cam=bpy.data.objects.new('Combo_PreviewCamera',bpy.data.cameras.new('Combo_PreviewCamera'))
scene.collection.objects.link(cam)
cam.location=(270,-430,245)
cam.rotation_euler=(Vector((0,-10,120))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=340;cam.data.clip_end=3000
scene.camera=cam
scene.render.engine='CYCLES'
scene.cycles.samples=24
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX'
scene.view_settings.exposure=-1.4
scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'BaseSoldier_SwordCombo.blend'))
with open(OUT/'manifest.json','w') as f:json.dump(manifest,f,indent=2)
for frame in (() if '--skip-render' in sys.argv else (0,7,15,21,28,35,42,51,60,65,75)):
    scene.frame_set(frame)
    scene.render.filepath=str(WORK/('preview_%03d.png'%frame))
    bpy.ops.render.render(write_still=True)
print('SWORD_COMBO_AUTHORED',json.dumps(manifest))
