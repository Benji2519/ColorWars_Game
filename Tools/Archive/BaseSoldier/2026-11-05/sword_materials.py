import unreal,json
from pathlib import Path
OUT=Path(unreal.Paths.project_saved_dir())/'Codex'/'SwordCombo'
sword=unreal.load_asset('/Game/ColorWars/Items/Weapons/Swords/Meshes/Sword_01')
report={'materials':[],'api':{}}
for slot in sword.get_editor_property('static_materials'):
    mat=slot.get_editor_property('material_interface')
    item={'slot':str(slot.get_editor_property('material_slot_name')),'material':mat.get_path_name(),'textures':{}}
    for name in unreal.MaterialEditingLibrary.get_texture_parameter_names(mat):
        tex=unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(mat,name)
        if not tex:continue
        fn=str(OUT/(tex.get_name()+'.png'))
        t=unreal.AssetExportTask();t.object=tex;t.filename=fn;t.automated=True;t.prompt=False;t.replace_identical=True
        t.exporter=unreal.TextureExporterPNG()
        ok=unreal.Exporter.run_asset_export_task(t)
        item['textures'][str(name)]={'asset':tex.get_path_name(),'file':fn,'exported':ok}
    report['materials'].append(item)
for cls in (unreal.FbxImportUI,unreal.AnimSequenceFactory,unreal.AnimMontageFactory,unreal.AnimSegment,unreal.SlotAnimationTrack,unreal.AnimTrack,unreal.CompositeSection):
    report['api'][cls.__name__]=str(cls.__doc__)+'\n'+','.join(dir(cls))
skel=unreal.load_asset('/Game/ColorWars/Characters/BaseSoldier/Meshes/SK_BaseSoldier')
for obj,name in [(skel,'skeleton'),(sword,'sword')]:
    for prop in ('preview_attached_asset_container','sockets'):
        try:report[name+'_'+prop]=str(obj.get_editor_property(prop))
        except Exception as e:report[name+'_'+prop]=str(e)
(OUT/'materials.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
unreal.log('SWORD_MATERIALS_COMPLETE')
