import json
import unreal

asset = unreal.load_asset("/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Idle/Weapons/AS_BaseSoldier_Idle_Sword")
model = asset.data_model_interface
controller = asset.controller
result = {
    "model": str(model),
    "controller": str(controller),
    "model_interface": str(asset.data_model_interface),
    "model_dir": dir(model) if model else [],
    "controller_dir": dir(controller) if controller else [],
}

if model:
    result["frame_rate"] = str(model.get_frame_rate())
    result["frames"] = model.get_number_of_frames()
    result["keys"] = model.get_number_of_keys()
    result["track_names"] = [str(x) for x in model.get_bone_track_names()]

for track in model.get_bone_animation_tracks() if model else []:
    name = track.get_editor_property("name")
    if str(name) not in ("root", "pelvis", "spine", "chest", "clavicle_l", "upper_arm_l", "forearm_l", "hand_l", "clavicle_r", "upper_arm_r", "forearm_r", "hand_r"):
        continue
    item = {"dir": dir(track), "repr": str(track)}
    for prop in ("name", "bone_tree_index", "internal_track_data"):
        try:
            value = track.get_editor_property(prop)
            item[prop] = str(value)
            if prop == "internal_track_data":
                item["raw_dir"] = dir(value)
                item["positions"] = [str(x) for x in unreal.RawAnimSequenceTrackExtensions.get_positional_keys(value)]
                item["rotations"] = [str(x) for x in unreal.RawAnimSequenceTrackExtensions.get_rotational_keys(value)]
                item["scales"] = [str(x) for x in unreal.RawAnimSequenceTrackExtensions.get_scale_keys(value)]
        except Exception as exc:
            item[prop + "_error"] = str(exc)
    result[str(name)] = item

with open(r"C:\Users\sunda\Documents\Unreal Projects\ColorWars\Saved\Codex\inspect_tracks.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2)

