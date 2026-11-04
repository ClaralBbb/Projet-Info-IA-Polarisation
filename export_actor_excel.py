"""Nouvelle présentation du corpus annoté; ne remplace pas les corrections humaines."""
import json
from pathlib import Path
from openpyxl import Workbook,load_workbook
from prepare_annotation import sheet
from actor_scope import project

def main():
    root=Path('plateforme')
    rows={r['comment_id']:r for r in [json.loads(l) for l in Path('classification_v02/commentaires_500.jsonl').read_text().splitlines()]}
    records=json.loads((root/'annotations_60.json').read_text())+json.loads((root/'annotations_lot02.json').read_text())
    w=Workbook();w.remove(w.active)
    sheet(w,'Guide',['Champ','Explication'],[
        ['Sujet','Violences et dégâts : sujet principal unique.'],
        ['Acteur évalué','Police, manifestants, casseurs/pillards/émeutiers, autres autorités, autres acteurs, acteur non établi. Ce sont les acteurs désignés ou évalués dans le discours, pas des identités vérifiées.'],
        ['Action','Distinguer force, violences des participants, dégradations/pillages, réponse policière, jugement général.'],
        ['Position','Attitude envers cette action ou ce jugement : critique, justification, nuance, description, indéterminée. Ne pas la convertir en soutien global à un groupe.'],
        ['Pourcentages','Une unité = commentaire × acteur. Si plusieurs attitudes coexistent pour le même acteur, catégorie mixte. Dénominateur séparé par acteur et par filtre; les chiffres des différents acteurs ne s’additionnent pas.'],
        ['Incertitude','Distinguer ambiguïté de position et attribution implicite de l’acteur. Par défaut le tableau de bord retient lectures et acteurs explicites.'],
        ['Hors périmètre','Les lignes sur d’autres sujets restent conservées, sans être comptées dans les pourcentages du sujet principal.'],
        ['Provenance','Annotations conversationnelles grille0.2, puis revue de périmètre0.3 explicite; pas une nouvelle classification API. Aucune relecture supplémentaire demandée.'],
        ['Sources','188 chaînes déclarées dans le lot de500, pas uniquement des journaux; authenticité et couverture non validées.'],
    ],{1:25,2:110})
    heads=['comment_id','position_index','sujet','retenue_sujet','acteur_evalue','acteur_precis_annotation','attribution_acteur','action','position','preuve','arguments','incertitude_position','texte_complet','parent','chaine','titre_video','motif_perimetre']
    values=[]
    for r in records:
        c=rows[r['comment_id']]
        for i,p in enumerate(r['annotation']['positions']):
            q=project(r['ordre_lot'],i)
            values.append([r['comment_id'],i,q['sujet'],'oui' if q['retenue'] else 'non',q['acteur'],p['acteur_precis'],q['attribution'],q['action'],p['position'],' | '.join(p['preuves']),' | '.join(p['arguments_utilises']),p['incertitude'],c['texte'],c['texte_parent'],c['chaine'],c['titre_video'],q['limite']])
    sheet(w,'Positions et acteurs',heads,values,{5:30,6:45,8:45,10:65,11:65,13:80,14:80,16:55,17:60})
    out=root/'ANALYSE_V4_sujet_acteurs_positions.xlsx';w.save(out)
    check=load_workbook(out,read_only=True)
    assert check['Positions et acteurs'].max_row==len(values)+1
    check.close()
    print(len(values),'positions exportées, dont',sum(v[3]=='oui' for v in values),'retenues dans le sujet; historique humain préservé.')

if __name__=='__main__':main()
