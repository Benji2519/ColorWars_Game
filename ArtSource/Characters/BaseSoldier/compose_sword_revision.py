from pathlib import Path
from PIL import Image,ImageDraw
out=Path(__file__).resolve().parent/'SwordComboRevision'
files=sorted((out/'Frames').glob('combo_*.png'))
assert len(files)==56,len(files)
frames=[]
for file in files:
 frame=int(file.stem.split('_')[-1])
 image=Image.open(file).convert('RGB')
 draw=ImageDraw.Draw(image)
 label='01 - Fendente' if frame<30 else '02 - Ritorno' if frame<60 else '03 - Dall alto'
 draw.rectangle((0,0,512,26),fill=(19,26,34))
 draw.text((12,8),label+' | Base: attacchi unarmed + Root Motion',fill=(240,240,240))
 frames.append(image)
frames[0].save(out/'SwordCombo_Revised.gif',save_all=True,append_images=frames[1:],duration=[67]*55+[300],loop=0,optimize=True)
sheet=Image.new('RGB',(1024,1072),(19,26,34))
for i,idx in enumerate((3,8,18,23,37,44)):
 im=frames[idx].resize((341,341))
 sheet.paste(im,(i%3*341,i//3*367))
sheet=sheet.crop((0,0,1024,708))
sheet.save(out/'SwordCombo_Revised_Poses.png')
print(out/'SwordCombo_Revised.gif')
