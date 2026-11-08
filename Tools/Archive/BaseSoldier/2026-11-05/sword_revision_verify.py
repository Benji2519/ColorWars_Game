import unreal,json,math
from pathlib import Path
root=Path(unreal.Paths.project_dir())
out=root/'Saved/Codex/SwordComboRevision'
m=json.loads((root/'ArtSource/Characters/BaseSoldier/SwordComboRevision/adapted_keys.json').read_text())
source={c['asset']:c for c in json.loads((out/'source.json').read_text())['clips']}
dest='/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/Sword/'
report={'clips':[]}
for c in m['clips']:
 seq=unreal.load_asset(dest+c['name']);sc=source[c['source']]
 assert abs(seq.get_play_length()-c['seconds'])<.001
 assert seq.get_editor_property('enable_root_motion')
 errors={}
 for mode in (unreal.AnimDataEvalType.RAW,unreal.AnimDataEvalType.COMPRESSED):
  opts=unreal.AnimPoseEvaluationOptions()
  opts.set_editor_property('evaluation_type',mode)
  opts.set_editor_property('extract_root_motion',False)
  maxpos=0;maxangle=0
  for f in range(c['frames']+1):
   p=seq.get_anim_pose_at_frame(f,opts)
   for n in sc['poses'][f]:
    a=unreal.AnimPoseExtensions.get_bone_pose(p,n,unreal.AnimPoseSpaces.LOCAL)
    b=c['keys'][f].get(n,sc['poses'][f][n]['local'])
    maxpos=max(maxpos,(a.translation-unreal.Vector(*b['translation'])).length())
    qa=a.rotation.to_tuple();qb=b['rotation']
    d=abs(sum(x*y for x,y in zip(qa,qb)))/math.sqrt(sum(x*x for x in qa)*sum(x*x for x in qb))
    maxangle=max(maxangle,math.degrees(2*math.acos(min(1,d))))
  assert maxpos<.15 and maxangle<.5,(c['name'],str(mode),maxpos,maxangle)
  errors[str(mode)]={'max_cm':maxpos,'max_degrees':maxangle}
 if '-VerifySequencesOnly' not in unreal.SystemLibrary.get_command_line():
  montage=unreal.load_asset(dest+c['name'].replace('AS_','AM_',1))
  assert abs(montage.get_play_length()-c['seconds'])<.001
  segments=montage.get_editor_property('slot_anim_tracks')[0].anim_track.anim_segments
  assert segments[0].anim_reference==seq
  assert abs(segments[0].anim_end_time-c['seconds'])<.001
 report['clips'].append({'name':c['name'],'source':c['source'],'duration':seq.get_play_length(),'errors':errors})
skeleton=seq.get_skeleton()
deps=[str(n) for n in unreal.AssetRegistryHelpers.get_asset_registry().get_dependencies(skeleton.get_path_name().split('.')[0],unreal.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True))]
assert '/Game/ColorWars/Items/Weapons/Swords/Meshes/Sword_01' in deps,deps
report['sword_preview_dependency']=True
report['montages_verified']='-VerifySequencesOnly' not in unreal.SystemLibrary.get_command_line()
report['success']=True
(out/'saved_verification.json').write_text(json.dumps(report,indent=2))
unreal.log('SWORD_REVISION_VERIFIED '+json.dumps(report))
