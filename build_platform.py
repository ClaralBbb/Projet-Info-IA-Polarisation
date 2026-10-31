"""Construit une interface autonome à partir des annotations réellement enregistrées."""
import hashlib
import csv
import html
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TEMPLATE=ROOT/'plateforme/template.html'

def build():
    rows=[json.loads(l) for l in (ROOT/'classification_v02/commentaires_500.jsonl').read_text().splitlines()]
    records=json.loads((ROOT/'plateforme/annotations_60.json').read_text())
    protocol=json.loads((ROOT/'plateforme/protocole.json').read_text())
    protocol['annotations_sha256']=hashlib.sha256((ROOT/'plateforme/annotations_60.json').read_bytes()).hexdigest()
    by_id={r['comment_id']:r for r in records}
    data={'protocol':protocol,'rows':[dict(r,result=by_id.get(r['comment_id'])) for r in rows]}
    payload=json.dumps(data,ensure_ascii=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e')
    text=TEMPLATE.read_text().replace('__PAYLOAD__',payload)
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/'docs/index.html').write_text(text)
    (ROOT/'docs/.nojekyll').touch()
    (ROOT/'plateforme/tableau_de_bord.html').write_text(text)
    with (ROOT/'plateforme/positions_60.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['comment_id','acteur','objet','position','theme','dans_perimetre','incertitude','preuve','validation_humaine'])
        for r in records:
            for p in r['annotation']['positions']:
                cells=[r['comment_id'],p['acteur_precis'],p['objet'],p['position'],p['theme'],p['dans_perimetre'],p['incertitude'],' | '.join(p['preuves']),'non_effectuee']
                writer.writerow(["'"+x if isinstance(x,str) and x.startswith(('=','+','-','@','\t','\r')) else x for x in cells])
    summary={'commentaires_classes':len(records),'positions':sum(len(r['annotation']['positions']) for r in records),
             'pertinence':dict(Counter(r['annotation']['pertinence'] for r in records)),'restants':len(rows)-len(records)}
    (ROOT/'plateforme/bilan.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':build()
