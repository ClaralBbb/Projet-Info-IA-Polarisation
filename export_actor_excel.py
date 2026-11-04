"""Nouvelle présentation du corpus annoté; ne remplace pas les corrections humaines."""
import json
from pathlib import Path
from shutil import copyfile
from openpyxl.styles import PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
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
    verification=[]
    for r in records:
        c=rows[r['comment_id']]
        for i,p in enumerate(r['annotation']['positions']):
            q=project(r['ordre_lot'],i)
            values.append([r['comment_id'],i,q['sujet'],'oui' if q['retenue'] else 'non',q['acteur'],p['acteur_precis'],q['attribution'],q['action'],p['position'],' | '.join(p['preuves']),' | '.join(p['arguments_utilises']),p['incertitude'],c['texte'],c['texte_parent'],c['chaine'],c['titre_video'],q['limite']])
            description='\n'.join([
                'Sujet : '+q['sujet'],
                'Retenue dans le sujet : '+('oui' if q['retenue'] else 'non — hors périmètre de cette comparaison'),
                'Acteur évalué : '+(q['acteur'] or 'non retenu dans la comparaison'),
                'Acteur précis dans le texte : '+p['acteur_precis'],
                'Action : '+(q['action'] or p['objet']+' (annotation initiale hors comparaison)'),
                'Position : '+p['position'],
                'Preuve : '+' | '.join(p['preuves']),
                'Argument : '+(' | '.join(p['arguments_utilises']) or 'aucun explicite enregistré'),
                'Incertitude : '+p['incertitude'],
                'Attribution de l’acteur : '+q['attribution'],
                'Note IA : '+p['note'],
            ])
            verification.append([f"C{r['ordre_lot']:03}-P{i+1}",c['texte'],c['texte_parent'] or ('Parent non disponible' if c['parent_id'] else 'Aucun parent : commentaire principal'),description,'','',c['chaine'],c['titre_video']])

    sheet(w,'Positions et acteurs',heads,values,{5:30,6:45,8:45,10:65,11:65,13:80,14:80,16:55,17:60})
    ws=sheet(w,'Vérification simple',['repere','commentaire_complet','commentaire_parent','classification_IA_et_justification','avis_facultatif','remarque_facultative','chaine','titre_video'],verification,{1:15,2:58,3:48,4:68,5:20,6:45,7:25,8:55})
    ws.freeze_panes='B2'
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.fill=PatternFill('solid',fgColor='FFF3CA' if cell.column in [5,6] else 'F2F6FB')
        ws.row_dimensions[row[0].row].height=280
    validation=DataValidation(type='list',formula1='"accord,désaccord,à discuter"',allow_blank=True)
    ws.add_data_validation(validation);validation.add(f'E2:E{ws.max_row}')
    w.active=w.sheetnames.index('Vérification simple')
    w['Guide'].append(['Lecture simple','Le classeur s’ouvre sur Vérification simple : commentaire complet, parent et classification côte à côte. Avis et remarque sont facultatifs. Un commentaire peut être répété pour plusieurs positions. Pour un texte très long, agrandir la barre de formule; aucun texte tronqué.'])
    out=root/'ANALYSE_V4_sujet_acteurs_positions.xlsx';w.save(out)
    copyfile(out,root/'VERIFICATION_V5_commentaires_et_positions.xlsx')
    check=load_workbook(out,read_only=True)
    assert check['Positions et acteurs'].max_row==len(values)+1
    assert check.active.title=='Vérification simple'
    assert check['Vérification simple'].max_row==len(values)+1
    for expected,actual in zip(verification,check['Vérification simple'].iter_rows(min_row=2,values_only=True)):
        assert actual[0:4]==tuple(expected[0:4])
        assert actual[4] is None and actual[5] is None
    check.close()
    print(len(values),'positions exportées, dont',sum(v[3]=='oui' for v in values),'retenues dans le sujet; historique humain préservé.')

if __name__=='__main__':main()
