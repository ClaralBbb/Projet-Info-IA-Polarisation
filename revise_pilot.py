"""Applique des décisions de révision explicites; ne transforme pas les blancs en accords."""
import copy,json
from pathlib import Path

def main():
    original=json.loads(Path('annotation/exemples_ia_20.json').read_text())
    rows=copy.deepcopy(original['positions']);index={r['position_id']:r for r in rows}
    index['C003-P1']['acteur']='jeunes manifestants / génération Z visée par l’auteur'
    index['C005-P1'].update(objet='conditions salariales présentées comme cause de violence',position='décrit sans position',note='Explication générale pertinente pour les causes de violence, pas une approbation ni une intervention policière précise.')
    index['C006-P1'].update(acteur='parti / équipe de Mélenchon',objet='caractère violent attribué à un parti politique',argument='',note='Ne pas confondre un parti qualifié de violent avec des dégâts précis. Parent et réponse peuvent avoir des positions différentes.')
    index['C007-P1'].update(acteur='manifestants, y compris les casseurs',objet='comportements non précisés',argument='',incertitude='ambigu',note='Désapprobation explicite mais comportements imprécis; ne pas inventer de violences matérielles.')
    new=copy.deepcopy(index['C007-P1']);new.update(position_id='C007-P2',acteur='Nicolas Sarkozy',objet='disparition alléguée de la République',position='condamne',responsabilite_attribuee='Sarkozy mis en cause dans une rupture institutionnelle alléguée.',preuve_textuelle="grâce à Sarkozy, la République n'existe plus !",incertitude='lecture explicite',note='Position supplémentaire, hors périmètre policier direct; ne remplace pas la ligne sur les manifestants.');rows.append(new)
    index['C008-P1']['note']='Conteste l’accusation visant les retraités; justifie les coups contre des personnes non identifiées. Ne réfute pas nécessairement toutes les accusations du parent.'
    for r in rows:r['version_grille']='0.2 — révision du pilote';r['origine_annotation']='assistant après relecture humaine; pas vérité de référence'
    feedback=json.loads(Path('classification_v02/retours_humains_pilote.json').read_text())
    reviewed=sum(any(r.get(k) not in [None,''] for k in ['accord','correction_acteur','correction_objet','correction_position','correction_preuve','note']) for r in feedback)
    result={'statut':'revision_explicite_apres_retours_humains','positions':rows,'lignes_relecture_renseignees':reviewed,'lignes_non_renseignees':len(feedback)-reviewed,
        'commentaires_revises':['C003','C005','C006','C007','C008'],
        'desaccords_non_resolus':[{'position_id':'C002-P2','sujet':'Humour et pertinence','decision':'Conserver le désaccord : humour du parent ne prouve pas que la réponse est hors sujet.'}],
        'limite':'Ces données ont servi à améliorer la grille et ne mesurent pas une performance indépendante.'}
    Path('plateforme/pilote_revise.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(reviewed,'lignes de relecture renseignées;',len(feedback)-reviewed,'non renseignées; 5 commentaires révisés et une position ajoutée.')

if __name__=='__main__':main()
