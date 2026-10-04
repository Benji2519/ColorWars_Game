"""Replace only v2 hand geometry with seamless cartoon mittens, save as v3."""
import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector, Quaternion

OUT=Path(__file__).resolve().parent
PREVIEW=OUT.parents[2]/'Design'/'Characters'
NAME='CW_BaseSoldier_v3'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CW_BaseSoldier_v2.blend'))
bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene
hero=bpy.data.objects['SK_CW_BaseSoldier_v2']
rig=bpy.data.objects['RIG_CW_BaseSoldier']
source=bpy.data.collections['01_EDITABLE_PARTS']
export=bpy.data.collections['02_CHARACTER_AND_RIG']
skin=bpy.data.materials['Skin']
hand_groups={g.index for g in hero.vertex_groups if g.name.startswith(('hand.','finger_','thumb.'))}
remaining_before=[tuple(v.co) for v in hero.data.vertices if not any(g.group in hand_groups and g.weight>0 for g in v.groups)]
# Edit the existing mesh so that body geometry, materials and UVs are preserved.
bpy.ops.object.mode_set(mode='OBJECT') if bpy.context.object and bpy.context.object.mode!='OBJECT' else None
bpy.ops.object.select_all(action='DESELECT'); hero.select_set(True); bpy.context.view_layer.objects.active=hero
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.object.mode_set(mode='OBJECT')
for v in hero.data.vertices: v.select=any(g.group in hand_groups and g.weight>0 for g in v.groups)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.delete(type='VERT'); bpy.ops.object.mode_set(mode='OBJECT')
assert [tuple(v.co) for v in hero.data.vertices]==remaining_before
for ob in list(source.objects):
    if ob.get('weight_region','').startswith(('hand.','finger_','thumb.')): bpy.data.objects.remove(ob,do_unlink=True)

hands=[]
for sign,side in [(1,'L'),(-1,'R')]:
    # z, half width, half depth, center x, center y, integrated thumb bulge.
    rows=[(.650,.006,.006,.552,-.052,0),(.656,.031,.021,.552,-.052,0),
          (.672,.056,.036,.55,-.051,0),(.694,.068,.043,.546,-.047,0),
          (.708,.073,.047,.54,-.043,.023),(.728,.077,.049,.537,-.04,.039),
          (.750,.079,.049,.535,-.037,.027),(.773,.073,.046,.53,-.034,.010),
          (.797,.060,.037,.521,-.03,0),(.823,.044,.030,.516,-.029,0)]
    n=24; verts=[]
    pivot=Vector((sign*.518,-.03,.815))
    for z,rx,ry,cx,cy,bulge in rows:
        for i in range(n):
            t=math.tau*i/n
            sn=math.sin(t); cs=math.cos(t)
            bump=bulge*max(0,-sn)**8
            p=Vector((sign*(cx+rx*sn-bump),cy-ry*cs,z))
            verts.append(tuple(pivot+1.23*(p-pivot)))
    faces=[tuple(reversed(range(n)))]
    for j in range(len(rows)-1):
        for i in range(n): faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    faces.append(tuple((len(rows)-1)*n+i for i in range(n)))
    data=bpy.data.meshes.new('Mitten.'+side); data.from_pydata(verts,[],faces); data.materials.append(skin); data.update()
    bm=bmesh.new(); bm.from_mesh(data)
    for _ in range(2):
        bmesh.ops.smooth_vert(bm,verts=[v for v in bm.verts if v.co.z<.79],factor=.45,use_axis_x=True,use_axis_y=True,use_axis_z=True)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(data); bm.free()
    for p in data.polygons: p.use_smooth=True
    ob=bpy.data.objects.new('Mitten.'+side,data); export.objects.link(ob)
    ob['weight_region']='hand.'+side
    vg=ob.vertex_groups.new(name='hand.'+side); vg.add(list(range(len(verts))),1,'REPLACE')
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.015); bpy.ops.object.mode_set(mode='OBJECT')
    original=ob.copy(); original.data=ob.data.copy(); source.objects.link(original); original.name='Mitten_Source.'+side
    hands.append(ob)

bpy.ops.object.select_all(action='DESELECT'); hero.select_set(True)
for ob in hands: ob.select_set(True)
bpy.context.view_layer.objects.active=hero; bpy.ops.object.join(); hero.name='SK_CW_BaseSoldier_v3'
assert [tuple(v.co) for v in hero.data.vertices[:len(remaining_before)]]==remaining_before
hero['stage']='v3 rounded mitten hands with integrated thumbs; each hand follows its hand bone'
scene['ModelNotes']='v3: only hand geometry replaced. V2 preserved. Original 30-bone hierarchy retained; digit bones intentionally unused.'
hero.data.calc_loop_triangles()
stats={'triangles':len(hero.data.loop_triangles),'vertices':len(hero.data.vertices),'bones':len(rig.data.bones),
       'non_hand_vertices_unchanged':True,'hand_style':'single closed mitten surface with integrated thumb',
       'digit_bones':'retained for compatibility, unused','unreal_import_tested':False}
assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in hero.data.vertices)
bm=bmesh.new(); bm.from_mesh(hero.data)
stats['nonmanifold_edges']=sum(not e.is_manifold for e in bm.edges)
stats['degenerate_faces']=sum(f.calc_area()<1e-12 for f in bm.faces); bm.free()
assert stats['nonmanifold_edges']==0 and stats['degenerate_faces']==0
camera=scene.camera; camera.location=(3,-6,2.4)
def look(p): camera.rotation_euler=(Vector(p)-camera.location).to_track_quat('-Z','Y').to_euler()
look((0,0,.95)); camera.data.ortho_scale=2.35
scene.render.resolution_x=1100; scene.render.resolution_y=1100
scene.render.filepath=str(PREVIEW/(NAME+'_hero.png'))
bpy.ops.object.select_all(action='DESELECT'); hero.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active=hero
bpy.ops.export_scene.fbx(filepath=str(OUT/(NAME+'.fbx')),use_selection=True,object_types={'ARMATURE','MESH'},add_leaf_bones=False,
    bake_anim=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,mesh_smooth_type='FACE',use_armature_deform_only=False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(NAME+'.blend')))
bpy.ops.render.render(write_still=True)
# Close-up includes the bracers so the wrist attachment is visible.
camera.location=(2,-5,1.3); look((.55,-.03,.72)); camera.data.ortho_scale=.50
scene.render.resolution_x=850; scene.render.resolution_y=850
scene.render.filepath=str(PREVIEW/(NAME+'_hand_detail.png')); bpy.ops.render.render(write_still=True)
# Reimport the new FBX in a disposable scene, leaving the saved .blend untouched.
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(OUT/(NAME+'.fbx')))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']; rigs=[o for o in bpy.context.scene.objects if o.type=='ARMATURE']
assert len(meshes)==1 and len(rigs)==1
imported=meshes[0]; imported.data.calc_loop_triangles()
assert len(imported.data.loop_triangles)==stats['triangles']
assert len(rigs[0].data.bones)==stats['bones']
assert all(abs(sum(g.weight for g in v.groups)-1)<1e-4 for v in imported.data.vertices)
for side in ['L','R']:
    pb=rigs[0].pose.bones['hand.'+side]; pb.rotation_mode='QUATERNION'; pb.rotation_quaternion=Quaternion((1,0,0),.5)
bpy.context.view_layer.update()
evaluated=imported.evaluated_get(bpy.context.evaluated_depsgraph_get()); m=evaluated.to_mesh()
assert all(math.isfinite(c) for v in m.vertices for c in v.co); evaluated.to_mesh_clear()
stats['fbx_roundtrip']='PASS'; stats['hand_pose_numeric_check']='PASS'
(OUT/(NAME+'_validation.json')).write_text(json.dumps(stats,indent=2))
print('VALIDATION '+json.dumps(stats))
