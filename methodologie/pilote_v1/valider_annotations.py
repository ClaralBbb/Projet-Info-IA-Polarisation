"""Contrôles de contrat et cohérence; ne valide pas la justesse des interprétations."""
import json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parents[1]))
from classify_opinions import validate

def check_annotation(a,row,schema):
 validate(a,schema)
 if a['comment_id']!=row['comment_id']:raise ValueError('Identifiant source incorrect')
 if not row['parent_id'] and a['necessite_parent']!='sans_parent':raise ValueError('Parent inexistant')
 if row['parent_id'] and a['necessite_parent']=='sans_parent':raise ValueError('Parent ignoré comme inexistant')
 for q in a['preuves_parent']:
  if not q.strip() or q not in (row['texte_parent'] or ''):raise ValueError('Citation parent non retrouvée: '+q)
 ids=set()
 for p in a['positions']:
  if p['position_id'] in ids:raise ValueError('Position dupliquée')
  ids.add(p['position_id'])
  for q in p['preuves_position']:
   if not q.strip() or q not in row['texte']:raise ValueError('Citation position non retrouvée: '+q)
  state=p['argumentation']['statut'];diag=p['argumentation']['diagnostic'];args=p['argumentation']['arguments']
  if state=='interpretable' and (not args or diag is not None):raise ValueError('Argument interprétable incohérent')
  if state in ['absente','ambigue']:
   if args or diag!=('ARG_ABSENT' if state=='absente' else 'ARG_AMBIGU'):raise ValueError('Diagnostic argument incohérent')
  for arg in args:
   if not arg['argument_precis'].strip():raise ValueError('Résumé vide')
   for q in arg['preuves']:
    if not q.strip() or q not in row['texte']:raise ValueError('Citation argument non retrouvée: '+q)
  if p['position'] in ['indeterminable','descriptive'] and p['exploitabilite_positions']=='exploitable':raise ValueError('Position non signée exploitable sans réserve')
  if p['position']=='indeterminable' and p['statut_position']!='indeterminable':raise ValueError('Statut position incohérent')
  if a['pertinence_thematique']!='directe' and p['exploitabilite_positions']=='exploitable':raise ValueError('Hors noyau mais position exploitable sans réserve')
 for rel in a['relations_sujets']:
  for q in rel['preuves']:
   if not q.strip() or q not in row['texte']:raise ValueError('Preuve de relation absente: '+q)

def main():
 schema=json.loads((BASE/'schema_annotation_v1.json').read_text())
 rows=[json.loads(l) for l in (BASE/'commentaires_50.jsonl').read_text().splitlines()]
 annotations=json.loads((BASE/'annotations_50_proposees.json').read_text())
 byid={r['comment_id']:r for r in rows}
 if len(annotations)!=50 or len({a['comment_id'] for a in annotations})!=50 or set(byid)!={a['comment_id'] for a in annotations}:raise ValueError('Lot incomplet ou doublonné')
 failures=[]
 for i,a in enumerate(annotations,1):
  try:check_annotation(a,byid[a['comment_id']],schema)
  except ValueError as err:failures.append(f'N{i:03}: {err}')
 if failures:raise ValueError('\n'.join(failures))
 print('50 sorties conformes au contrat; citations et cohérences contrôlées. Cela ne valide pas leur interprétation.')

if __name__=='__main__':main()
