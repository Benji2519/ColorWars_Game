"""Import the three authored attacks and build their continuous preview montage."""
import json
import math
import shutil
import traceback
from pathlib import Path
import unreal

ROOT=Path(unreal.Paths.project_dir()).resolve()
SRC=ROOT/'ArtSource/Characters/BaseSoldier/SwordCombo'
WORK=ROOT/'Saved/Codex/SwordCombo'
DEST='/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/Sword'
MESH='/Game/ColorWars/Characters/BaseSoldier/Meshes/SKM_BaseSoldier'
SKEL='/Game/ColorWars/Characters/BaseSoldier/Meshes/SK_BaseSoldier'
manifest=json.loads((SRC/'manifest.json').read_text())
report={'imported':[],'checks':{},'errors':[]}

def pose(seq,frame):
    return seq.get_anim_pose_at_frame(frame,unreal.AnimPoseEvaluationOptions())

def serial_transform(t):
    return {'translation':list(t.translation.to_tuple()),'rotation':list(t.rotation.to_tuple()),'scale':list(t.scale3d.to_tuple())}

try:
    skeleton=unreal.load_asset(SKEL)
    mesh=unreal.load_asset(MESH)
    assert skeleton and mesh
    # Preserve exactly the three previous copies before replacing their content.
    backup=WORK/'previous_assets'
    backup.mkdir(exist_ok=True)
    for c in manifest['clips']:
        for suffix in ('.uasset','.uexp','.ubulk'):
            old=ROOT/'Content/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/Sword'/(c['name']+suffix)
            dst=backup/old.name
            if old.exists() and not dst.exists():shutil.copy2(old,dst)
    tasks=[]
    for c in manifest['clips']:
        options=unreal.FbxImportUI()
        options.automated_import_should_detect_type=False
        options.mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION
        options.original_import_type=unreal.FBXImportType.FBXIT_ANIMATION
        options.import_animations=True
        options.import_mesh=False
        options.import_materials=False
        options.import_textures=False
        options.skeleton=skeleton
        ai=options.anim_sequence_import_data
        ai.set_editor_property('animation_length',unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
        ai.set_editor_property('use_default_sample_rate',False)
        ai.set_editor_property('custom_sample_rate',30)
        ai.set_editor_property('import_bone_tracks',True)
        ai.set_editor_property('import_uniform_scale',1.0)
        task=unreal.AssetImportTask()
        task.filename=str(SRC/(c['name']+'.fbx'))
        task.destination_path=DEST
        task.destination_name=c['name']
        task.automated=True
        task.replace_existing=True
        task.replace_existing_settings=True
        task.save=False
        task.options=options
        task.factory=unreal.FbxFactory()
        tasks.append(task)
    if '-SwordComboSkipImport' not in unreal.SystemLibrary.get_command_line():
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    sequences=[]
    for c,t in zip(manifest['clips'],tasks):
        seq=unreal.load_asset(DEST+'/'+c['name'])
        assert seq and isinstance(seq,unreal.AnimSequence),c['name']
        seq.set_preview_skeletal_mesh(mesh)
        seq.set_editor_property('enable_root_motion',False)
        # Old unarmed copies had editable additive transforms: discard those.
        try:
            seq.controller.remove_all_curves_of_type(unreal.RawCurveTrackTypes.RCT_TRANSFORM,False)
        except Exception as e:
            report.setdefault('cleanup_notes',[]).append(str(e))
        assert seq.get_skeleton()==skeleton
        assert abs(seq.get_play_length()-c['seconds'])<.04,(seq.get_name(),seq.get_play_length(),c['seconds'])
        assert unreal.EditorAssetLibrary.save_loaded_asset(seq,False)
        sequences.append(seq)
        report['imported'].append({'asset':seq.get_path_name(),'duration':seq.get_play_length(),'skeleton':seq.get_skeleton().get_path_name(),'imported_object_paths':list(t.imported_object_paths)})
    max_gap_pos=0.0
    max_gap_angle=0.0
    for i in (0,1):
        a=pose(sequences[i],manifest['clips'][i]['frames'])
        b=pose(sequences[i+1],0)
        for name in unreal.AnimPoseExtensions.get_bone_names(a):
            ta=unreal.AnimPoseExtensions.get_bone_pose(a,name,unreal.AnimPoseSpaces.WORLD)
            tb=unreal.AnimPoseExtensions.get_bone_pose(b,name,unreal.AnimPoseSpaces.WORLD)
            delta=(ta.translation-tb.translation).length()
            qa=ta.rotation;qb=tb.rotation
            dot=abs(qa.x*qb.x+qa.y*qb.y+qa.z*qb.z+qa.w*qb.w)
            angle=math.degrees(2*math.acos(min(1,max(-1,dot))))
            max_gap_pos=max(max_gap_pos,delta)
            max_gap_angle=max(max_gap_angle,angle)
    report['checks']['boundary_max_position_error_cm']=max_gap_pos
    report['checks']['boundary_max_rotation_error_degrees']=max_gap_angle
    report['pose_samples']={}
    for seq,c in zip(sequences,manifest['clips']):
        report['pose_samples'][seq.get_name()]={}
        for f in (0,c['frames']//2,c['frames']):
            p=pose(seq,f)
            report['pose_samples'][seq.get_name()][str(f)]={str(n):serial_transform(unreal.AnimPoseExtensions.get_bone_pose(p,n,unreal.AnimPoseSpaces.WORLD)) for n in unreal.AnimPoseExtensions.get_bone_names(p)}
    first=pose(sequences[0],0)
    report['checks']['first_hand_world']=serial_transform(unreal.AnimPoseExtensions.get_bone_pose(first,'hand_r',unreal.AnimPoseSpaces.WORLD))
    report['checks']['sockets']=[str(n) for n in unreal.AnimPoseExtensions.get_socket_names(first)]
    weapon=unreal.load_asset('/Game/ColorWars/Items/Weapons/Swords/Meshes/Sword_01')
    report['checks']['weapon_bounds']=str(weapon.get_bounding_box())
    deps=unreal.AssetRegistryHelpers.get_asset_registry().get_dependencies(SKEL,unreal.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True))
    report['checks']['skeleton_dependencies']=[str(d) for d in deps]
    # Independent Montage to play all three consecutively, without editing combat BP.
    montage_path=DEST+'/AM_BaseSoldier_Sword_Combo'
    montage=unreal.load_asset(montage_path) if unreal.EditorAssetLibrary.does_asset_exist(montage_path) else None
    if not montage:
        factory=unreal.AnimMontageFactory()
        factory.target_skeleton=skeleton
        factory.source_animation=sequences[0]
        montage=unreal.AssetToolsHelpers.get_asset_tools().create_asset('AM_BaseSoldier_Sword_Combo',DEST,unreal.AnimMontage,factory)
    assert montage
    segments=[];start=0.0
    for seq in sequences:
        segment=unreal.AnimSegment()
        segment.set_editor_property('anim_reference',seq)
        segment.set_editor_property('anim_start_time',0.0)
        segment.set_editor_property('anim_end_time',seq.get_play_length())
        segment.set_editor_property('anim_play_rate',1.0)
        segment.set_editor_property('looping_count',1)
        segment.import_text('(StartPos=%.9f)'%start)
        segment.set_editor_property('cached_play_length',seq.get_play_length())
        segments.append(segment)
        start+=seq.get_play_length()
    track=unreal.AnimTrack()
    track.set_editor_property('anim_segments',segments)
    slot=unreal.SlotAnimationTrack()
    slot.set_editor_property('slot_name','DefaultSlot')
    slot.set_editor_property('anim_track',track)
    montage.set_editor_property('slot_anim_tracks',[slot])
    montage.controller.set_frame_rate(unreal.FrameRate(30,1),False)
    montage.controller.set_number_of_frames(unreal.FrameNumber(round(start*30)),False)
    montage.set_preview_skeletal_mesh(mesh)
    assert unreal.EditorAssetLibrary.save_loaded_asset(montage,False)
    report['montage']={'asset':montage.get_path_name(),'duration':montage.get_play_length(),'segments':[{'asset':s.anim_reference.get_name(),'start':s.start_pos,'end':s.anim_end_time} for s in montage.get_editor_property('slot_anim_tracks')[0].anim_track.anim_segments]}
    assert abs(montage.get_play_length()-start)<.01,report['montage']
    assert max_gap_pos<.1,('Boundary position error',max_gap_pos)
    assert max_gap_angle<.5,('Boundary rotation error',max_gap_angle)
    report['success']=True
except Exception:
    report['errors'].append(traceback.format_exc())
    report['success']=False
finally:
    (WORK/'import_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    unreal.log('SWORD_IMPORT_REPORT '+json.dumps({k:v for k,v in report.items() if k!='pose_samples'}))
