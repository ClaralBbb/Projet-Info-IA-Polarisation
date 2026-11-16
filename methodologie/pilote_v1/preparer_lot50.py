"""Sélection uniquement; aucune classification ni collecte API."""
import hashlib,json,random
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
def main():
 source=ROOT/'classification_v02/commentaires_500.jsonl'
 rows=[json.loads(l) for l in source.read_text().splitlines()]
 old=[]
 for f in ['annotations_60.json','annotations_lot02.json']:old+=json.loads((ROOT/'plateforme'/f).read_text())
 excluded_ids={r['comment_id'] for r in old};excluded_videos={r['video_id'] for r in old}
 rng=random.Random(20261116);candidates=[(i+1,r) for i,r in enumerate(rows) if r['comment_id'] not in excluded_ids and r['video_id'] not in excluded_videos];rng.shuffle(candidates)
 chosen=[];used=set()
 for replies in [False,True]:
  picked=0
  for order,r in candidates:
   if bool(r['parent_id'])==replies and r['video_id'] not in used:
    chosen.append(dict(r,ordre_source=order,repere=f'N{len(chosen)+1:03}'));used.add(r['video_id']);picked+=1
    if picked==25:break
  if picked!=25:raise ValueError('Quotas indisponibles')
 rng.shuffle(chosen)
 for i,r in enumerate(chosen,1):r['repere']=f'N{i:03}'
 (BASE/'commentaires_50.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in chosen))
 manifest={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'seed':20261116,'n':50,'principaux':25,'reponses':25,'videos':50,'exclusion':'Identifiants ET vidéos des90 annotations conversationnelles précédentes; lot500 déjà distinct des pilotes initiaux.','excluded_ids':sorted(excluded_ids),'excluded_videos':sorted(excluded_videos),'verification_evenement':'non_effectuee','representativite':'Non représentatif; sous-échantillon exploratoire du lot présélectionné par lexique.'}
 (BASE/'selection.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print('50 nouveaux commentaires,50 vidéos,25 principaux/25 réponses; aucune classification effectuée par ce script.')
if __name__=='__main__':main()
