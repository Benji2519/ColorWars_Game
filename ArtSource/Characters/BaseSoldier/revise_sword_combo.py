"""Adapt upper-body sword actions over the unmodified sampled unarmed motion."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Matrix,Vector,Quaternion

HERE=Path(__file__).resolve().parent
# Reuse the original rig/weapon setup and the two-bone solver only.
setup=(HERE/'create_sword_combo.py').read_text()
exec(compile(setup.split('# Each pose specifies')[0],str(HERE/'create_sword_combo.py'),'exec'))
OUT=HERE/'SwordComboRevision'
OUT.mkdir(exist_ok=True)
WORK=ROOT/'Saved/Codex/SwordComboRevision'
source=json.loads((WORK/'source.json').read_text())
refkeys={k.lower():k for k in data['reference']}
source_indices=[0,1,2]
edited=[b.name for b in rig.pose.bones if b.name.startswith(('upper_arm','forearm','hand','finger','thumb'))]

def serial(m):
 t,q,s=m.decompose()
 return {'translation':list(t),'rotation':[q.x,q.y,q.z,q.w],'scale':list(s)}

def source_pose(c,f):
 p={k:v['world'] for k,v in c['poses'][f].items()}
 for pb in rig.pose.bones:
  set_world(pb.name,mapped_bone(pb.name,p))

def smooth(a,b,t):
 t=max(0,min(1,t));t=t*t*(3-2*t)
 return a.lerp(b,t)

# Hand positions are offsets from the moving chest; blade directions are in
# component space. These keys adapt the strikes while body/steps stay sourced.
guard=((-28,-25,6),(-.16,-.45,.88))
left_exit=((22,-27,-4),(.88,-.42,-.30))
right_exit=((-43,-20,15),(-.90,-.36,.23))
keys=[
 [(0,guard),(.20,((-43,13,31),(-.58,.30,.76))),(.29,((-47,9,33),(-.64,.18,.75))),(.43,((-21,-45,13),(-.10,-.98,-.16))),(.59,((25,-32,-3),(.90,-.35,-.28))),(.76,left_exit),(1,left_exit)],
 [(0,left_exit),(.18,((27,2,17),(.93,.22,.28))),(.29,((29,-2,17),(.92,.12,.36))),(.43,((-2,-49,10),(.08,-.98,.15))),(.60,((-43,-27,15),(-.92,-.30,.25))),(.77,right_exit),(1,right_exit)],
 [(0,right_exit),(.22,((-12,12,53),(-.04,.69,.72))),(.32,((-10,10,54),(.02,.66,.75))),(.47,((-10,-46,34),(0,-.94,.35))),(.60,((-11,-40,-12),(.06,-.61,-.79))),(.73,((-15,-29,-20),(.10,-.40,-.91))),(1,guard)],
]

def desired(i,t):
 for (a,pa),(b,pb) in zip(keys[i],keys[i][1:]):
  if t<=b:
   u=(t-a)/(b-a)
   return smooth(Vector(pa[0]),Vector(pb[0]),u),smooth(Vector(pa[1]),Vector(pb[1]),u).normalized()
 return Vector(keys[i][-1][1][0]),Vector(keys[i][-1][1][1])

def apply(i,c,f):
 source_pose(c,f)
 chest=rig.pose.bones['chest'].matrix.translation.copy()
 offset,axis=desired(i,f/c['frames'])
 target=chest+offset
 # Source torso motion already drives the shoulder, preserving its character.
 handrot=(frame_basis(axis,Vector((0,-1,.18))) @ local_sword_basis.inverted()).to_quaternion()
 solve_limb('upper_arm.R','forearm.R','hand.R',target,chest+Vector((-68,-12,-10)),handrot)
 lefttarget=chest+Vector((25,-20,-4))
 solve_limb('upper_arm.L','forearm.L','hand.L',lefttarget,chest+Vector((57,4,-19)),mapped_bone('hand.L',data['idle']).to_quaternion())
 for pb in rig.pose.bones:
  if pb.name.startswith(('finger','thumb')):
   m=mapped_bone(pb.name,data['idle']);parent=mapped_bone(pb.parent.name,data['idle'])
   set_world(pb.name,pb.parent.matrix @ parent.inverted() @ m)

def unreal_world(name):
 key=refkeys[name.replace('.','_').lower()]
 return C @ rig.pose.bones[name].matrix @ rest[name].inverted() @ C @ ue_matrix(data['reference'][key])

manifest={'clips':[],'edited_bones':[refkeys[n.replace('.','_').lower()] for n in edited]}
for i,si in enumerate(source_indices):
 c=source['clips'][si]
 name='AS_BaseSoldier_Attack_Sword_%02d'%(i+1)
 action=bpy.data.actions.new(name);action.use_fake_user=True
 rig.animation_data_create();rig.animation_data.action=action
 samples=[]
 for f in range(c['frames']+1):
  scene.frame_set(f);apply(i,c,f)
  frame={}
  for n in edited:
   parent=rig.pose.bones[n].parent.name
   frame[refkeys[n.replace('.','_').lower()]]=serial(unreal_world(parent).inverted() @ unreal_world(n))
  samples.append(frame)
  for pb in rig.pose.bones:
   for prop in ('location','rotation_quaternion','scale'):pb.keyframe_insert(prop,frame=f,group=pb.name)
 manifest['clips'].append({'name':name,'source':c['asset'],'frames':c['frames'],'seconds':c['duration'],'fps':c['fps'],'keys':samples})

# Preview stitches the travel continuously; individual assets keep original roots.
action=bpy.data.actions.new('SwordCombo_Adapted_PREVIEW');action.use_fake_user=True
rig.animation_data.action=action
frame_offset=0;travel=Vector((0,0,0))
for i,si in enumerate(source_indices):
 c=source['clips'][si]
 for f in range(c['frames']+1):
  scene.frame_set(frame_offset+f);apply(i,c,f)
  for pb in rig.pose.bones:
   if pb.parent is None:
    m=pb.matrix.copy();m.translation+=travel;set_world(pb.name,m)
  for pb in rig.pose.bones:
   for prop in ('location','rotation_quaternion','scale'):pb.keyframe_insert(prop,frame=frame_offset+f,group=pb.name)
 # Track source armature displacement, including its sign conversion.
 p0=c['poses'][0]['RIG_CW_BaseSoldier']['world']['translation']
 p1=c['poses'][-1]['RIG_CW_BaseSoldier']['world']['translation']
 travel+=C.to_3x3() @ (Vector(p1)-Vector(p0))
 frame_offset+=c['frames']
scene.frame_start=0;scene.frame_end=frame_offset
(OUT/'adapted_keys.json').write_text(json.dumps(manifest))
# Use the established preview studio, without its old animation generation.
studio=setup.split('# Studio setup at centimetre scale;')[1].split('\n',1)[1].split('scene.frame_set(0)')[0]
exec(compile(studio,str(HERE/'create_sword_combo.py'),'exec'))
cam.location=(310,-490,255)
cam.rotation_euler=(Vector((0,-80,95))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=420
scene.render.resolution_x=640;scene.render.resolution_y=640
scene.cycles.samples=12
scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'BaseSoldier_SwordCombo_Adapted.blend'))
if '--render' in sys.argv:
 for f in (6,13,18,36,43,48,72,84,90):
  scene.frame_set(min(f,frame_offset));scene.render.filepath=str(OUT/('pose_%03d.png'%f));bpy.ops.render.render(write_still=True)
print('SWORD_ADAPTED',[(c['name'],c['source'],c['seconds']) for c in manifest['clips']])
