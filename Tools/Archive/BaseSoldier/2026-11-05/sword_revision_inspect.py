import unreal,json
from pathlib import Path
out=Path(unreal.Paths.project_dir())/'Saved/Codex/SwordComboRevision'
out.mkdir(exist_ok=True)
base='/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/'
def tr(t):return {'translation':list(t.translation.to_tuple()),'rotation':list(t.rotation.to_tuple()),'scale':list(t.scale3d.to_tuple())}
result={'clips':[],'docs':{}}
opts=unreal.AnimPoseEvaluationOptions()
opts.set_editor_property('extract_root_motion',False)
opts.set_editor_property('retrieve_additive_as_full_pose',True)
for i in (1,2,3):
 a=unreal.load_asset(base+'AS_BaseSoldier_Attack_%02d'%i)
 fps=a.data_model_interface.get_frame_rate()
 n=a.data_model_interface.get_number_of_frames()
 c={'asset':a.get_path_name(),'duration':a.get_play_length(),'frames':n,'fps':[fps.numerator,fps.denominator],'settings':{},'poses':[]}
 for key in ('enable_root_motion','force_root_lock','root_motion_root_lock','use_normalized_root_motion_scale'):
  c['settings'][key]=str(a.get_editor_property(key))
 for f in range(n+1):
  p=a.get_anim_pose_at_frame(f,opts)
  c['poses'].append({str(b):{'world':tr(unreal.AnimPoseExtensions.get_bone_pose(p,b,unreal.AnimPoseSpaces.WORLD)),'local':tr(unreal.AnimPoseExtensions.get_bone_pose(p,b,unreal.AnimPoseSpaces.LOCAL))} for b in unreal.AnimPoseExtensions.get_bone_names(p)})
 result['clips'].append(c)
result['docs']['controller']=str(unreal.AnimDataController.set_bone_track_keys.__doc__)
(out/'source.json').write_text(json.dumps(result))
unreal.log('SWORD_REVISION_INSPECT_DONE')
