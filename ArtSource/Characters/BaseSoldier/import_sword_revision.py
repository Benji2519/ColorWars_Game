"""Bake modified arms over source poses, retaining root motion/settings/notifies."""
import unreal,json,math,traceback,shutil
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve()
OUT=ROOT/'ArtSource/Characters/BaseSoldier/SwordComboRevision'
WORK=ROOT/'Saved/Codex/SwordComboRevision'
DEST='/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/Sword'
manifest=json.loads((OUT/'adapted_keys.json').read_text())
source=json.loads((WORK/'source.json').read_text())
sources={c['asset']:c for c in source['clips']}
mesh=unreal.load_asset('/Game/ColorWars/Characters/BaseSoldier/Meshes/SKM_BaseSoldier')
report={'clips':[],'success':False}
opts=unreal.AnimPoseEvaluationOptions()
opts.set_editor_property('extract_root_motion',False)
opts.set_editor_property('evaluation_type',unreal.AnimDataEvalType.RAW)

def delta(a,b):
 pos=(a.translation-unreal.Vector(*b['translation'])).length()
 qa=a.rotation;qb=b['rotation'];d=abs(sum(x*y for x,y in zip(qa.to_tuple(),qb)))
 return pos,math.degrees(2*math.acos(min(1.,d)))

try:
 if '-RecreateThirdSword' in unreal.SystemLibrary.get_command_line():
  # These two assets were generated in this revision from the tentative 02 base.
  backup=WORK/'third_from_02_backup';backup.mkdir(exist_ok=True)
  for name in ('AM_BaseSoldier_Attack_Sword_03','AS_BaseSoldier_Attack_Sword_03'):
   path=DEST+'/'+name
   disk=ROOT/'Content'/Path(path.removeprefix('/Game/')).with_suffix('.uasset')
   if disk.exists():shutil.copy2(disk,backup/disk.name)
   if unreal.EditorAssetLibrary.does_asset_exist(path):assert unreal.EditorAssetLibrary.delete_asset(path)
 seqs=[]
 for c in manifest['clips']:
  src=unreal.load_asset(c['source']);sc=sources[c['source']]
  path=DEST+'/'+c['name']
  if unreal.EditorAssetLibrary.does_asset_exist(path):
   seq=unreal.load_asset(path)
   backup=WORK/'before_revision';backup.mkdir(exist_ok=True)
   disk=ROOT/'Content'/Path(path.removeprefix('/Game/')).with_suffix('.uasset')
   if disk.exists() and not (backup/disk.name).exists():shutil.copy2(disk,backup/disk.name)
  else:
   seq=unreal.EditorAssetLibrary.duplicate_asset(c['source'].split('.')[0],path)
  assert isinstance(seq,unreal.AnimSequence),path
  if '-SwordMontagesOnly' in unreal.SystemLibrary.get_command_line():
   seqs.append(seq)
   continue
  ctl=seq.controller
  ctl.open_bracket('Adapt unarmed motion for sword',False)
  ctl.remove_all_curves_of_type(unreal.RawCurveTrackTypes.RCT_TRANSFORM,False)
  ctl.set_frame_rate(unreal.FrameRate(*c['fps']),False)
  ctl.set_number_of_frames(unreal.FrameNumber(c['frames']),False)
  for name in sc['poses'][0]:
   vals=[c['keys'][f].get(name,sc['poses'][f][name]['local']) for f in range(c['frames']+1)]
   assert ctl.set_bone_track_keys(name,[unreal.Vector(*x['translation']) for x in vals],[unreal.Quat(*x['rotation']) for x in vals],[unreal.Vector(*x['scale']) for x in vals],False),name
  ctl.close_bracket(False)
  for prop in ('enable_root_motion','force_root_lock','root_motion_root_lock','use_normalized_root_motion_scale'):
   seq.set_editor_property(prop,src.get_editor_property(prop))
  seq.set_preview_skeletal_mesh(mesh)
  assert unreal.EditorAssetLibrary.save_loaded_asset(seq,False)
  # Test every frame: all unedited local tracks, including root, legs and torso.
  maxpos=0.;maxangle=0.;armchange=0.;keypos=0.;keyangle=0.
  for f in range(c['frames']+1):
   p=seq.get_anim_pose_at_frame(f,opts)
   for name in sc['poses'][f]:
    actual=unreal.AnimPoseExtensions.get_bone_pose(p,name,unreal.AnimPoseSpaces.LOCAL)
    expected=c['keys'][f].get(name,sc['poses'][f][name]['local'])
    pe,ae=delta(actual,expected);keypos=max(keypos,pe);keyangle=max(keyangle,ae)
    pe,ae=delta(actual,sc['poses'][f][name]['local'])
    if name not in manifest['edited_bones']:maxpos=max(maxpos,pe);maxangle=max(maxangle,ae)
    else:armchange=max(armchange,ae)
  info={'asset':path,'source':c['source'],'seconds':seq.get_play_length(),'root_motion':seq.get_editor_property('enable_root_motion'),'unchanged_tracks_max_cm':maxpos,'unchanged_tracks_max_degrees':maxangle,'authored_keys_max_cm':keypos,'authored_keys_max_degrees':keyangle,'max_arm_change_degrees':armchange,'advance_cm':sc['poses'][-1]['RIG_CW_BaseSoldier']['local']['translation'][1]-sc['poses'][0]['RIG_CW_BaseSoldier']['local']['translation'][1]}
  report['clips'].append(info)
  assert maxpos<.01 and maxangle<.1,info
  assert keypos<.02 and keyangle<.1,info
  assert armchange>20,info
  seqs.append(seq)
 # One montage per attack, preserving the original gameplay montage setup.
 report['montages']=[]
 for i,(seq,c) in enumerate(zip(seqs,manifest['clips'])):
  original=c['source'].split('.')[0].replace('/AS_','/AM_')
  path=DEST+'/AM_BaseSoldier_Attack_Sword_%02d'%(i+1)
  montage=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else unreal.EditorAssetLibrary.duplicate_asset(original,path)
  assert isinstance(montage,unreal.AnimMontage),path
  original_montage=unreal.load_asset(original)
  slots=list(original_montage.get_editor_property('slot_anim_tracks'))
  for slot in slots:
   track=slot.anim_track;segments=list(track.anim_segments)
   for seg in segments:
    if seg.anim_reference:
     seg.set_editor_property('anim_reference',seq)
     seg.set_editor_property('cached_play_length',seq.get_play_length())
   track.set_editor_property('anim_segments',segments);slot.set_editor_property('anim_track',track)
  montage.set_editor_property('slot_anim_tracks',slots)
  montage.controller.set_frame_rate(unreal.FrameRate(*c['fps']),False)
  montage.controller.set_number_of_frames(unreal.FrameNumber(c['frames']),False)
  montage.set_preview_skeletal_mesh(mesh)
  assert unreal.EditorAssetLibrary.save_loaded_asset(montage,False)
  assert abs(montage.get_play_length()-seq.get_play_length())<.001
  report['montages'].append({'asset':path,'seconds':montage.get_play_length()})
 report['success']=True
except Exception:
 report['error']=traceback.format_exc()
finally:
 (WORK/'import_report.json').write_text(json.dumps(report,indent=2))
 unreal.log('SWORD_REVISION_REPORT '+json.dumps(report))
