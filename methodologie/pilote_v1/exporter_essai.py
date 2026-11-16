"""Présentation des propositions enregistrées, pas classification automatique."""
import json
from pathlib import Path
from collections import Counter
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
B=Path(__file__).resolve().parent

def sheet(w,name,headers,rows,widths=None):
 s=w.create_sheet(name);s.append(headers)
 for row in rows:s.append(row)
 for row in s:
  for c in row:
   if isinstance(c.value,str):c.data_type='s'
   c.alignment=Alignment(vertical='top',wrap_text=True)
 for c in s[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='244766')
 for i,h in enumerate(headers,1):s.column_dimensions[s.cell(1,i).column_letter].width=(widths or {}).get(h,26)
 s.freeze_panes='B2';s.auto_filter.ref=s.dimensions
 return s

def main():
 rows=[json.loads(l) for l in (B/'commentaires_50.jsonl').read_text().splitlines()];annotations=json.loads((B/'annotations_50_proposees.json').read_text())
 byid={a['comment_id']:a for a in annotations};positions=[p for a in annotations for p in a['positions']]
 codes=Counter(arg['code'] for p in positions for arg in p['argumentation']['arguments'])
 summary={'commentaires_examinesi':len(annotations),'positions_proposees':len(positions),'commentaires_sans_position_extraite':sum(not a['positions'] for a in annotations),'pertinence':dict(Counter(a['pertinence_thematique'] for a in annotations)),'exploitabilite_positions':dict(Counter(p['exploitabilite_positions'] for p in positions)),'arguments_codes':dict(codes),'evenement_verifie':0,'appels_api':0,'validation_humaine_sur_ce_lot':False}
 summary['commentaires_examines']=summary.pop('commentaires_examinesi')
 (B/'bilan_essai.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
 w=Workbook();w.remove(w.active)
 sheet(w,'Guide',['point','description'],[
 ['Statut','ESSAI PROVISOIRE de50 nouveaux commentaires, interprétés dans la conversation. Pas de modèle entraîné ni d’appel API; aucune validation humaine de ce lot.'],
 ['Objet','Tester le protocoleV1 et signaler ses limites. Le dashboard et les annotations historiques restent inchangés.'],
 ['Lire','Lecture50 réunit texte, parent, pertinence et propositions. Certaines entrées n’ont pas de position extraite; elles ne sont pas supprimées.'],
 ['Travail humain','Aucune nouvelle passe exhaustive demandée. Le bilan et les cas à discuter sont disponibles pour décider de la suite.'],
 ['Événement','Aucune vidéo ni commentaire n’est validé pour Paris le17octobre; références à d’autres dates/pays signalées.'],
 ['Dictionnaire','A01–A12/M01 provisoires conservés. ARG_AUTRE permet de garder les arguments identifiables sans forcer une famille.'],
 ['Preuves','Citations exactes contrôlées dans le texte; leur présence ne valide ni les faits ni la justesse de la classification.'],
 ],{'point':25,'description':115})
 vals=[];detail=[]
 for r in rows:
  a=byid[r['comment_id']];texts=[]
  for p in a['positions']:
   args=p['argumentation'];parts=[p['position_id']+' — '+p['position'],'Cible : '+p['cible']['designation'],'Proposition : '+p['proposition_evaluee'],'Preuve : '+' | '.join(p['preuves_position'])]
   parts+=['Argument '+ar['code']+' ('+ar['mode_expression']+') : '+ar['argument_precis'] for ar in args['arguments']]
   if not args['arguments']:parts.append('Diagnostic argument : '+str(args['diagnostic']))
   parts+=['Exploitation : '+p['exploitabilite_positions'],'Limites : '+p['note']];texts.append('\n'.join(parts))
   detail.append([r['repere'],r['comment_id'],p['position_id'],p['cible']['designation'],p['proposition_evaluee'],p['position'],p['statut_position'],json.dumps(args,ensure_ascii=False),' | '.join(p['preuves_position']),p['incertitude']['cible'],p['incertitude']['position'],p['incertitude']['argument'],p['exploitabilite_positions'],p['note']])
  vals.append([r['repere'],r['texte'],r['texte_parent'] or 'Aucun parent',a['pertinence_thematique'],'\n\n'.join(texts) if texts else 'Aucune position dans le périmètre extraite; voir les limites.','\n'.join(a['limites']),a['necessite_parent'],a['fonction_reponse'],json.dumps(a['lien_evenement'],ensure_ascii=False),r['titre_video'],r['chaine'],r['comment_id']])
 s=sheet(w,'Lecture50',['repere','texte_complet','parent','pertinence','propositions','limites','necessite_parent','fonction_reponse','lien_evenement','titre_video','chaine','comment_id'],vals,{'repere':14,'texte_complet':85,'parent':75,'propositions':100,'limites':80,'fonction_reponse':65,'lien_evenement':65,'titre_video':60})
 for i in range(2,s.max_row+1):s.row_dimensions[i].height=280
 sheet(w,'Positions détaillées',['repere','comment_id','position_id','cible','proposition','position','statut_position','argumentation_json','preuves','incertitude_cible','incertitude_position','incertitude_argument','exploitation','note'],detail,{'argumentation_json':100,'preuves':80,'note':90,'proposition':65})
 dictionary=json.loads((B/'dictionnaire_v1.json').read_text())
 dh=['code','intitule','definition','inclusion','exclusion','exemple1','exemple2']
 sheet(w,'Dictionnaire provisoire',dh,[[r.get(h) for h in dh] for r in dictionary['categories']],{'intitule':65,'definition':75,'inclusion':65,'exclusion':65})
 w.active=w.sheetnames.index('Lecture50');out=B/'ESSAI_50_PROPOSITIONS_PROTOCOLE_V1.xlsx';w.save(out)
 check=load_workbook(out,read_only=True)
 assert check['Lecture50'].max_row==51 and check['Positions détaillées'].max_row==len(positions)+1
 for real,expected in zip(check['Lecture50'].iter_rows(min_row=2,values_only=True),rows):assert real[1]==expected['texte'] and real[2]==(expected['texte_parent'] or 'Aucun parent')
 check.close();print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
