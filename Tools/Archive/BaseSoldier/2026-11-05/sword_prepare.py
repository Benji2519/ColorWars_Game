import json
from pathlib import Path
import unreal

OUT = Path(unreal.Paths.project_saved_dir()) / 'Codex' / 'SwordCombo'
OUT.mkdir(parents=True, exist_ok=True)
BASE = '/Game/ColorWars/Characters/BaseSoldier'
mesh = unreal.load_asset(BASE + '/Meshes/SKM_BaseSoldier')
idle = unreal.load_asset(BASE + '/Animations/Anim/Idle/Weapons/AS_BaseSoldier_Idle_Sword')
sword = unreal.load_asset('/Game/ColorWars/Items/Weapons/Swords/Meshes/Sword_01')
skeleton = idle.get_skeleton()

def transform(t):
    return {'translation': list(t.translation.to_tuple()), 'rotation': list(t.rotation.to_tuple()), 'scale': list(t.scale3d.to_tuple())}

report = {'skeleton': skeleton.get_path_name(), 'mesh': mesh.get_path_name(), 'sword_class': sword.get_class().get_name(), 'docs': {}}
for cls, methods in [(unreal.AnimSequence, ['get_anim_pose_at_frame']), (unreal.AnimPoseExtensions, ['get_bone_pose','get_reference_pose','get_socket_pose']), (unreal.AnimDataController,['set_bone_track_keys','set_number_of_frames','add_bone_track'])]:
    for name in methods:
        report['docs'][cls.__name__+'.'+name] = str(getattr(cls,name).__doc__)
pose = idle.get_anim_pose_at_frame(0, unreal.AnimPoseEvaluationOptions())
ref = unreal.AnimPoseExtensions.get_reference_pose(skeleton)
report['reference'] = {str(n): transform(unreal.AnimPoseExtensions.get_bone_pose(ref,n,unreal.AnimPoseSpaces.WORLD)) for n in unreal.AnimPoseExtensions.get_bone_names(ref)}
report['idle'] = {str(n): transform(unreal.AnimPoseExtensions.get_bone_pose(pose,n,unreal.AnimPoseSpaces.WORLD)) for n in unreal.AnimPoseExtensions.get_bone_names(pose)}
report['socket'] = transform(unreal.AnimPoseExtensions.get_socket_pose(pose,'SwordSocket',unreal.AnimPoseSpaces.LOCAL))
report['socket_world'] = transform(unreal.AnimPoseExtensions.get_socket_pose(pose,'SwordSocket',unreal.AnimPoseSpaces.WORLD))
report['skeleton_preview_dir'] = [x for x in dir(skeleton) if 'preview' in x.lower() or 'socket' in x.lower()]
for asset, filename in [(sword,'Sword_01.fbx')]:
    task = unreal.AssetExportTask()
    task.object = asset
    task.filename = str(OUT / filename)
    task.automated = True
    task.prompt = False
    task.replace_identical = True
    options = unreal.FbxExportOption()
    options.ascii = False
    task.options = options
    report[filename] = unreal.Exporter.run_asset_export_task(task)
with open(OUT/'prepare.json','w',encoding='utf-8') as f:
    json.dump(report,f,indent=2)
unreal.log('SWORD_PREPARE_COMPLETE')
