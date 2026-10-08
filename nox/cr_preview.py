from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math
from cristiano import stadium,PARTS
blocks=stadium();cells={}
for (X,Y,Z),b in blocks.items():
 x,y,z=X-32,Y-2,Z-45
 if b=='minecraft:air' or (z>0 and y>5):continue
 if (x,z) not in cells or cells[(x,z)][0]<y:cells[(x,z)]=(y,b)
colors={'green_concrete':(42,124,67),'white_concrete':(240,239,219),'smooth_sandstone':(189,158,112),'cut_sandstone':(162,135,91),'smooth_quartz':(206,206,201),'iron_block':(177,190,198),'polished_andesite':(105,116,123),'blue_concrete':(34,66,129),'blue_stained_glass':(50,131,164),'sea_lantern':(152,235,230)}
im=Image.new('RGB',(1400,1050),(21,25,37));d=ImageDraw.Draw(im)
def p(x,z,y):return (700+(x-z)*7,510+(x+z)*3.5-y*9)
solid={(X-32,Y-2,Z-45):v for (X,Y,Z),v in blocks.items() if v!='minecraft:air' and not (Z-45>0 and Y-2>5)}
for (x,y,z),b in sorted(solid.items(),key=lambda q:(q[0][0]+q[0][2],q[0][1])):
 c=colors[b.split(':')[1]]
 if (x+1,y,z) not in solid:d.polygon([p(x+1,z,y+1),p(x+1,z+1,y+1),p(x+1,z+1,y),p(x+1,z,y)],fill=tuple(int(v*.65) for v in c))
 if (x,y,z+1) not in solid:d.polygon([p(x,z+1,y+1),p(x+1,z+1,y+1),p(x+1,z+1,y),p(x,z+1,y)],fill=tuple(int(v*.82) for v in c))
 if (x,y+1,z) not in solid:d.polygon([p(x,z,y+1),p(x+1,z,y+1),p(x+1,z+1,y+1),p(x,z+1,y+1)],fill=c)
f=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',32);sm=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',20)
d.text((55,30),'사막의 베르나베우 · 크리스티아누',font=f,fill=(238,219,170))
d.text((55,80),'생성 구조 템플릿 기반 컷어웨이 · 전면 상부를 생략해 피치와 관중석을 표시',font=sm,fill=(168,184,201))
d.rounded_rectangle((45,870,1355,1000),20,fill=(32,40,58))
d.text((70,895),'65 × 91 블록  |  은빛 외벽  |  다층 관중석  |  전광판 링  |  열린 지붕',font=sm,fill=(236,227,204))
d.text((70,940),'골대·중앙선·측면 엄폐물 포함. 게임 스크린샷이 아닌 템플릿 블록 렌더입니다.',font=sm,fill=(156,179,197))
out=Path(__file__).resolve().parent/'output/Cristiano-Bernabeu-Preview.png';im.save(out)
print(out)
