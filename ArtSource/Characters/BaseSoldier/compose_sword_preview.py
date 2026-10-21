from pathlib import Path
from PIL import Image,ImageDraw

OUT=Path(__file__).resolve().parent/'SwordCombo'
files=sorted((OUT/'PreviewFrames').glob('combo_*.png'))
assert len(files)==38,len(files)
frames=[Image.open(p).convert('RGB') for p in files]
durations=[67]*len(frames)
durations[-1]=250
frames[0].save(OUT/'BaseSoldier_SwordCombo_Preview.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
indices=[0,6,10,17,25,30]
labels=['Guardia','1 - Fendente diagonale','Passaggio 1 > 2','2 - Taglio di ritorno','3 - Caricamento','3 - Colpo dall alto']
sheet=Image.new('RGB',(960,708),(18,25,34))
draw=ImageDraw.Draw(sheet)
for cell,(idx,label) in enumerate(zip(indices,labels)):
    thumb=frames[idx].resize((320,320),Image.Resampling.LANCZOS)
    x=cell%3*320;y=cell//3*354
    sheet.paste(thumb,(x,y))
    draw.text((x+12,y+327),label,fill=(230,237,245))
sheet.save(OUT/'BaseSoldier_SwordCombo_ContactSheet.png')
print('SWORD_PREVIEW_GIF',OUT/'BaseSoldier_SwordCombo_Preview.gif')
