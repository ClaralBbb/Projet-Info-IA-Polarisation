"""Projection analytique explicite des positions : sujet, acteur évalué, action.
Les identifiants n:index renvoient aux lectures enregistrées, pas à des mots-clés.
Aucune observation des faits ou identification des personnes réelles n'est déduite.
"""
from collections import defaultdict,Counter
SUBJECT='Violences et dégâts'
ACTORS=['Police','Manifestants','Casseurs / pillards / émeutiers','Autres autorités','Autres acteurs','Acteur non établi']
ACTIONS={'force':'Coups, gaz et usage de la force','participants':'Violences attribuées aux participants','degats':'Dégradations, incendies et pillages','reponse':'Intervention, prévention et sanctions','general':'Jugements généraux sur les acteurs'}
# Listes de décisions explicites; les autres positions restent conservées mais exclues.
RULES={}
def group(actor,action,pairs,implicit=()):
    for pair in pairs:
        key=f'{pair[0]}:{pair[1]}'
        if key in RULES:raise ValueError('Position affectée deux fois')
        RULES[key]={'acteur':actor,'action':ACTIONS[action], 'attribution':'non_etablie' if actor=='Acteur non établi' else 'implicite' if pair in implicit else 'explicite'}
group('Police','force',[(15,0),(17,0),(33,0),(41,1),(42,0),(47,0),(57,0),(65,0),(67,0)],implicit=[(47,0)])
group('Police','reponse',[(3,0),(59,0),(68,0),(78,0),(90,0)])
group('Police','degats',[(36,0),(45,0)])
group('Police','general',[(23,0),(37,0),(81,1)])
group('Manifestants','participants',[(58,0)])
group('Manifestants','degats',[(27,0),(31,0),(33,2),(55,0),(70,0),(83,0)],implicit=[(27,0),(83,0)])
group('Casseurs / pillards / émeutiers','degats',[(2,0),(5,0),(24,0),(29,0),(43,0),(63,0),(64,0),(65,1),(85,0)])
group('Casseurs / pillards / émeutiers','participants',[(46,1),(84,0)])
group('Casseurs / pillards / émeutiers','general',[(56,0)])
group('Autres autorités','reponse',[(7,1),(21,0),(34,1),(73,0)],implicit=[(34,1)])
group('Autres autorités','force',[(31,1),(45,1),(54,0),(77,0),(81,0),(87,1)])
group('Autres acteurs','participants',[(7,0),(18,0),(51,0),(62,0)])
group('Autres acteurs','degats',[(34,0),(71,0)])
group('Acteur non établi','participants',[(7,2),(28,0),(49,0),(50,0),(61,0),(75,0),(87,0)])
group('Acteur non établi','degats',[(19,0),(22,0),(69,0)])
group('Acteur non établi','force',[(76,0)])
group('Acteur non établi','reponse',[(5,1)])

def project(order,index):
    rule=RULES.get(f'{order}:{index}')
    return {'sujet':SUBJECT,'retenue':bool(rule),'acteur':rule['acteur'] if rule else None,
            'action':rule['action'] if rule else None,'attribution':rule['attribution'] if rule else 'non_applicable',
            'regle':f'{order}:{index}',
            'limite':'Acteur tel qu’évalué ou désigné dans le discours, pas auteur des faits établi.' if rule else 'Hors sujet principal ou action/acteur trop imprécis pour cette comparaison.'}

BUCKETS=['condamne','justifie_soutient','nuance','decrit_sans_position','indeterminee','mixte']
def aggregate(items):
    """Une unité = commentaire × acteur. Plusieurs attitudes => mixte, pas doublons."""
    grouped=defaultdict(lambda:defaultdict(set))
    for row in items:
        grouped[row['acteur']][row['comment_id']].add(row['position'])
    result={}
    for actor,comments in grouped.items():
        c=Counter(next(iter(v)) if len(v)==1 else 'mixte' for v in comments.values());n=len(comments)
        result[actor]={'denominateur':n,'effectifs':{k:c[k] for k in BUCKETS},'pourcentages':{k:100*c[k]/n for k in BUCKETS}}
    return result

# Regroupements d'arguments lus, indexés par POSITION, pas par commentaire entier.
ARGUMENT_FAMILIES={
    'Coût des dégâts et conséquences matérielles':{(5,0),(27,0),(58,0),(69,0),(83,0)},
    'Protection des personnes ou commerces':{(15,0),(28,0),(43,0),(57,0),(59,0)},
    'Violences antérieures ou punition invoquées':{(42,0),(76,0),(87,0)},
    'Absence d’écoute ou de dialogue':{(74,0),(77,0)},
    'Risque d’escalade':{(87,1)},
}
def argument_families(order,index,arguments):
    if not arguments:return []
    return [name for name,pairs in ARGUMENT_FAMILIES.items() if (order,index) in pairs] or ['Autres justifications explicites']
