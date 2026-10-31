import hashlib,json,random
from pathlib import Path
from openpyxl import load_workbook
from prepare_annotation import select,sheet,LEXICON
from analyze import load
from openpyxl import Workbook
root=Path('classification_v02')
source=Path('data/paris_2026-10-17.json')
if not source.exists():source=source.with_suffix('.xlsx')
videos,comments=load(source);lookup={c['comment_id']:c for c in comments};vm={v['video_id']:v for v in videos}
pilot=json.loads(Path('annotation/exemples_ia_20.json').read_text())
evaluation=json.loads(Path('annotation/evaluation/selection.json').read_text())
excluded=set(pilot['excluded_comment_ids'])|set(evaluation['selected_comment_ids'])
excluded_vids=set(pilot['excluded_video_ids'])|{lookup[c]['video_id'] for c in evaluation['selected_comment_ids']}
selected=select([c for c in comments if c['comment_id'] not in excluded and c['video_id'] not in excluded_vids],size=500,max_per_video=2)
rows=[]
for c in selected:
 v=vm[c['video_id']];p=lookup.get(c.get('parent_id'))
 rows.append({'comment_id':c['comment_id'],'video_id':c['video_id'],'titre_video':v['title'],'chaine':v.get('channel',''),
  'texte':c.get('text','').replace('\r\n','\n').replace('\r','\n'), 'parent_id':c.get('parent_id') or None,
  'texte_parent':p.get('text') if p else None,'statut_parent':'disponible' if p else ('absent_du_corpus' if c.get('parent_id') else 'sans_parent')})
(root/'commentaires_500.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
rng=random.Random(20261031);control=set(rng.sample([r['comment_id'] for r in rows],50))
w=Workbook();w.remove(w.active)
sheet(w,'Guide',['Point','Description'],[
 ['Statut','500 candidats sélectionnés; aucune classification IA réalisée. Aucun appel API.'],
 ['Périmètre','Police et violences au sens large. Pertinence pour Paris le 17 octobre non validée.'],
 ['Sélection','250 principaux, 250 réponses; au maximum deux par vidéo; aucun commentaire ni vidéo du pilote20 ou du lot100 précédent. Lexique public, graine fixe.'],
 ['Contrôle humain','50 commentaires marqués oui dans controle_humain : un petit contrôle proposé, pas une obligation d’annoter les 500. Ne pas montrer les prédictions avant une annotation indépendante.'],
 ['Biais','Présélection lexicale et équilibrage des vidéos : ne représente pas les proportions d’opinion dans le corpus. Les commentaires pertinents sans mots-clés peuvent être manqués.'],
 ['Contexte','Parent référencé seulement; pas tout le fil, pas de vidéo visionnée.'],
],{1:24,2:110})
headers=['comment_id','titre_video','chaine','texte_complet','texte_parent','controle_humain','pertinence_humaine','acteur_precis','objet','position','preuve','note']
ws=sheet(w,'Commentaires 500',headers,[[r['comment_id'],r['titre_video'],r['chaine'],r['texte'],r['texte_parent'],'oui' if r['comment_id'] in control else 'non','','','','','',''] for r in rows],{2:50,4:75,5:70,12:45})
ws.freeze_panes='D2'
w.save(root/'lot_police_violences_500.xlsx')
manifest={'statut':'selection_non_classee','source_file':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'n':len(rows),'videos':len({r['video_id'] for r in rows}),'principaux':sum(not r['parent_id'] for r in rows),'reponses':sum(bool(r['parent_id']) for r in rows),
 'parent_manquant':sum(r['statut_parent']=='absent_du_corpus' for r in rows),'seed_selection':20261024,'seed_control':20261031,
 'excluded_comment_ids':sorted(excluded),'excluded_video_ids':sorted(excluded_vids),'control_comment_ids':sorted(control),'lexicon':sorted(LEXICON)}
(root/'selection.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in manifest.items() if k in ['statut','n','videos','principaux','reponses','parent_manquant']},ensure_ascii=False))
