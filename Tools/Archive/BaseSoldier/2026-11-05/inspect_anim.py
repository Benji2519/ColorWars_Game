import json
import unreal

paths = [
    "/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Idle/Weapons/AS_BaseSoldier_Idle_Sword",
    "/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Parry/Weapon/AS_BaseSoldier_Parry_Sword",
    "/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/AS_BaseSoldier_Attack_01",
]

result = {}
for path in paths:
    asset = unreal.load_asset(path)
    item = {"object": str(asset), "class": asset.get_class().get_name() if asset else None}
    if asset:
        item["methods"] = [x for x in dir(asset) if any(k in x.lower() for k in ("controller", "data", "frame", "bone", "length", "rate"))]
        item["all_methods"] = dir(asset)
        try:
            item["frames"] = unreal.AnimationBlueprintLibrary.get_num_frames(asset)
        except Exception as exc:
            item["frames_error"] = str(exc)
        try:
            item["bones"] = [str(x) for x in unreal.AnimationBlueprintLibrary.get_animation_track_names(asset)]
        except Exception as exc:
            item["bones_error"] = str(exc)
    result[path] = item

result["unreal_animation_names"] = [x for x in dir(unreal) if any(k in x.lower() for k in ("anim", "controller", "skeleton"))]
for class_name in result["unreal_animation_names"]:
    try:
        cls = getattr(unreal, class_name)
        result["class_" + class_name] = [x for x in dir(cls) if any(k in x.lower() for k in ("bone", "frame", "bracket", "curve", "key", "model", "controller"))]
    except Exception as exc:
        result["class_" + class_name] = [str(exc)]
with open(r"C:\Users\sunda\Documents\Unreal Projects\ColorWars\Saved\Codex\inspect_anim.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2)
unreal.log_warning("CODEX INSPECT COMPLETE")

