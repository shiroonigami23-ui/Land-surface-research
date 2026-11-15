"""Build data/species.json from sp/*.txt. Line: Name|Scientific|Where|Habitat|Diet|IUCN|Summary[|sound description]"""
import json, re, glob
IU={"LC":"Least Concern","NT":"Near Threatened","VU":"Vulnerable","EN":"Endangered","CR":"Critically Endangered","DD":"Data Deficient","NE":"Not Evaluated","EW":"Extinct in the Wild","EX":"Extinct"}
SND={ # group -> (default description, vocal?)
"Big cats & wild cats":("Roars, growls, chuffs and moans; small cats hiss, mew and purr. Roaring is possible only in Panthera cats with a stretchy larynx.",True),
"Elephants, rhinos & large herbivores":("Trumpets, rumbles and snorts; elephants also make infrasonic rumbles below human hearing that travel several kilometres.",True),
"Primates":("Hoots, screams, barks, songs and alarm calls; gibbons sing duets, howler monkeys are among the loudest land animals.",True),
"Bears, dogs & other carnivores":("Growls, barks, howls, yips and huffs depending on the species.",True),
"Hoofed mammals":("Bellows, grunts, bleats, snorts and in deer the autumn rut calls (roars and bugles).",True),
"Small mammals":("Squeaks, chirps, chatter and alarm whistles; bats call in ultrasound mostly above human hearing.",True),
"Marsupials & monotremes":("Grunts, hisses, screeches and bellows; koalas make a surprisingly deep bellow.",True),
"Birds":("Songs and calls used to claim territory and attract mates; each species has its own recognisable voice.",True),
"Birds of prey":("Whistles, screams, yelps and screeches; owls hoot or screech at night.",True),
"Reptiles":("Mostly silent; many hiss when threatened. Crocodilians, tokay geckos and some tortoises are the vocal exceptions.",False),
"Amphibians":("Croaks, trills, peeps and chirps; male frogs call in choruses to attract females, often after rain.",True),
"Insects & other invertebrates":("Many are silent; crickets, cicadas and katydids sing by rubbing or vibrating body parts, and bees and mosquitoes hum with their wingbeats.",False),
"Trees":("Silent to our ears. Leaves rustle in the wind, and studies show stressed plants emit faint ultrasonic clicks (Khait et al., Cell 2023), far too high to hear.",False),
"Flowers & other plants":("Silent to our ears. Stressed plants emit faint ultrasonic clicks recorded by microphones (Khait et al., Cell 2023), but nothing a person can hear.",False),
"Fungi":("Silent: fungi make no sounds.",False),
}
KING={"Trees":"Plant","Flowers & other plants":"Plant","Fungi":"Fungus"}
out=[];seen=set();slugs=set()
for f in sorted(glob.glob('sp/*.txt')):
    g=e=None
    for ln in open(f,encoding='utf-8'):
        ln=ln.strip()
        if not ln: continue
        if ln.startswith('#'): g,e=[x.strip() for x in ln[1:].split('|')]; continue
        p=[x.strip() for x in ln.split('|')]
        n,sci,where,hab,diet,iu,summ=p[:7]
        if sci in seen: continue
        seen.add(sci)
        s=re.sub(r'[^a-z0-9]+','-',n.lower().replace("'","")).strip('-')
        if s in slugs: s+='-'+re.sub(r'[^a-z]+','-',sci.split()[-1].lower())
        slugs.add(s)
        d0,voc=SND.get(g,("",False))
        d=dict(slug=s,name=n,scientific=sci,group=g,emoji=e,kingdom=KING.get(g,"Animal"),where=where,habitat=hab,diet=diet,iucn=IU.get(iu,iu),summary=summ,wiki=n.replace(' ','_') if (sci.endswith('spp.') or ' ' not in sci) else sci.replace(' ','_'))
        if len(p)>7 and p[7]:
            d['sound_desc']=p[7]; d['sound']=n+' call'
        else:
            d['sound_desc']=d0
            if voc: d['sound']=n+(' song' if g=='Birds' else ' call')
            else: d['silent']=True
        out.append(d)
out.sort(key=lambda d:(d['group'],d['name']))
json.dump(out,open('../species.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print(len(out),Counter(d['group'] for d in out))
