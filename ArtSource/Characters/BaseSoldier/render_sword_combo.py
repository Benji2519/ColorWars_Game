import bpy
from pathlib import Path

OUT=Path(__file__).resolve().parent/'SwordCombo'
scene=bpy.context.scene
scene.render.resolution_x=512
scene.render.resolution_y=512
scene.render.resolution_percentage=100
scene.render.fps=30
scene.render.fps_base=1
scene.render.engine='CYCLES'
scene.cycles.samples=8
scene.render.use_persistent_data=True
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(OUT/'PreviewFrames'/'combo_')
scene.frame_step=2
scene.render.fps=15
bpy.ops.render.render(animation=True)
print('SWORD_COMBO_FRAMES_COMPLETE',scene.render.filepath)
