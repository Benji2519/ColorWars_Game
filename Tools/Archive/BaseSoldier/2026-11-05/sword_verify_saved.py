import json,math
from pathlib import Path
import unreal

ROOT=Path(unreal.Paths.project_dir()).resolve()
DEST='/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/Sword/'
results={}
for i,length in ((1,.7),(2,.7),(3,1.1)):
    name='AS_BaseSoldier_Attack_Sword_%02d'%i
    seq=unreal.load_asset(DEST+name)
    assert seq and abs(seq.get_play_length()-length)<1e-4
    raw=seq.get_anim_pose_at_frame(10,unreal.AnimPoseEvaluationOptions())
    options=unreal.AnimPoseEvaluationOptions()
    options.evaluation_type=unreal.AnimDataEvalType.COMPRESSED
    compressed=seq.get_anim_pose_at_frame(10,options)
    max_error=0
    for bone in ('hand_r','foot_r','foot_l','head'):
        a=unreal.AnimPoseExtensions.get_bone_pose(raw,bone,unreal.AnimPoseSpaces.WORLD)
        b=unreal.AnimPoseExtensions.get_bone_pose(compressed,bone,unreal.AnimPoseSpaces.WORLD)
        max_error=max(max_error,(a.translation-b.translation).length())
    assert max_error<.5,(name,max_error)
    results[name]={'duration':seq.get_play_length(),'raw_vs_runtime_max_error_cm':max_error,'skeleton':seq.get_skeleton().get_path_name(),'source_fbx':list(seq.get_editor_property('asset_import_data').extract_filenames())}
montage=unreal.load_asset(DEST+'AM_BaseSoldier_Sword_Combo')
assert montage and abs(montage.get_play_length()-2.5)<1e-4
slots=montage.get_editor_property('slot_anim_tracks')
assert len(slots)==1 and len(slots[0].anim_track.anim_segments)==3
segments=slots[0].anim_track.anim_segments
assert [round(s.start_pos,3) for s in segments]==[0,.7,1.4]
assert [s.anim_reference.get_name() for s in segments]==['AS_BaseSoldier_Attack_Sword_%02d'%i for i in (1,2,3)]
results['montage']={'duration':montage.get_play_length(),'slot':str(slots[0].slot_name),'segments':len(segments)}
results['success']=True
(ROOT/'Saved/Codex/SwordCombo/saved_verification.json').write_text(json.dumps(results,indent=2))
unreal.log('SWORD_SAVED_VERIFIED '+json.dumps(results))
