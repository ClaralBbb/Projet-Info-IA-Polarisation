"""Construit une interface autonome à partir des annotations réellement enregistrées."""
import hashlib
import csv
import html
import json
from collections import Counter
from actor_scope import project,aggregate,argument_families
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TEMPLATE=ROOT/'plateforme/template.html'

def build():
    rows=[json.loads(l) for l in (ROOT/'classification_v02/commentaires_500.jsonl').read_text().splitlines()]
    record_files=[ROOT/'plateforme/annotations_60.json',ROOT/'plateforme/annotations_lot02.json']
    records=[r for file in record_files for r in json.loads(file.read_text())]
    protocol=json.loads((ROOT/'plateforme/protocole.json').read_text())
    protocol.update(n_classes=len(records),n_total=len(rows),positions=sum(len(r['annotation']['positions']) for r in records),selection_lot='90 premières lignes du lot mélangé; exploratoire et non représentatif.')
    protocol['annotations_sha256']=hashlib.sha256(b''.join(file.read_bytes() for file in record_files)).hexdigest()
    (ROOT/'plateforme/protocole.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2))
    by_id={r['comment_id']:r for r in records}
    for record in records:
        n=record['ordre_lot'];derived=[]
        for position_index,p in enumerate(record['annotation']['positions']):
            tags=argument_families(n,position_index,p['arguments_utilises'])
            projection=project(n,position_index)
            derived.append({'groupe':projection['action'] if projection['retenue'] else 'Hors sujet principal','familles_arguments':tags,'scope':projection})
        record['regroupements_exploratoires']=derived
    pilot=json.loads((ROOT/'plateforme/pilote_revise.json').read_text())
    pilot['positions_revisees']=[r for r in pilot['positions'] if r['repere'] in pilot['commentaires_revises']]
    data={'subject':'Violences et dégâts','source_channel_count':len({r['chaine'] for r in rows}),'protocol':protocol,'pilot':{k:v for k,v in pilot.items() if k!='positions'},'rows':[dict(r,result=by_id.get(r['comment_id'])) for r in rows]}
    payload=json.dumps(data,ensure_ascii=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e')
    text=TEMPLATE.read_text().replace('__PAYLOAD__',payload)
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/'docs/index.html').write_text(text)
    (ROOT/'docs/.nojekyll').touch()
    (ROOT/'plateforme/tableau_de_bord.html').write_text(text)
    (ROOT/'plateforme/RESULTATS_V3_90_commentaires.html').write_text(text)
    (ROOT/'plateforme/RESULTATS_V4_acteurs_violences.html').write_text(text)
    with (ROOT/'plateforme/positions_analysees.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['comment_id','acteur','objet','position','theme','dans_perimetre','incertitude','preuve','validation_humaine'])
        for r in records:
            for p in r['annotation']['positions']:
                cells=[r['comment_id'],p['acteur_precis'],p['objet'],p['position'],p['theme'],p['dans_perimetre'],p['incertitude'],' | '.join(p['preuves']),'non_effectuee']
                writer.writerow(["'"+x if isinstance(x,str) and x.startswith(('=','+','-','@','\t','\r')) else x for x in cells])
    summary={'commentaires_classes':len(records),'positions':sum(len(r['annotation']['positions']) for r in records),
             'pertinence':dict(Counter(r['annotation']['pertinence'] for r in records)),'restants':len(rows)-len(records)}
    scoped=[{'comment_id':r['comment_id'],'acteur':d['scope']['acteur'],'position':p['position']} for r in records for p,d in zip(r['annotation']['positions'],r['regroupements_exploratoires']) if d['scope']['retenue'] and p['statut_enonciation']=='auteur' and p['incertitude']=='lecture_explicite' and d['scope']['attribution']=='explicite']
    (ROOT/'plateforme/statistiques_acteurs.json').write_text(json.dumps(aggregate(scoped),ensure_ascii=False,indent=2))
    (ROOT/'plateforme/bilan.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':build()
