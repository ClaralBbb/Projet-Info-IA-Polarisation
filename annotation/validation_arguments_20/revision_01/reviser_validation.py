"""Exporte une révision proposée après relecture; aucun appel modèle, aucun apprentissage."""
import copy,hashlib,json,textwrap,math
from pathlib import Path
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.worksheet.datavalidation import DataValidation
BASE=Path(__file__).resolve().parent
ORIGINAL=BASE.parent/'propositions_et_dictionnaire.json'
HUMAN=BASE/'relecture_humaine_recue.xlsx'

def table(w,name,headers,rows,widths=None):
    s=w.create_sheet(name);s.append(headers)
    for row in rows:s.append(row)
    for row in s:
        for c in row:
            if isinstance(c.value,str):c.data_type='s'
            c.alignment=Alignment(vertical='top',wrap_text=True)
    for c in s[1]:c.fill=PatternFill('solid',fgColor='244766');c.font=Font(color='FFFFFF',bold=True)
    for i,h in enumerate(headers,1):s.column_dimensions[s.cell(1,i).column_letter].width=(widths or {}).get(h,26)
    s.freeze_panes='B2';s.auto_filter.ref=s.dimensions
    return s

def main():
    baseline=json.loads(ORIGINAL.read_text());proposals=copy.deepcopy(baseline['annotations'])
    w=load_workbook(HUMAN,read_only=True);it=w['Vérification'].iter_rows(values_only=True);headers=next(it)
    received=[dict(zip(headers,r)) for r in it];w.close()
    feedback={r['repere']:r for r in received};byid={r['repere']:r for r in proposals}
    assert set(feedback)==set(byid)
    changes=[]
    def revise(ref,decision,**fields):
        p=byid[ref];before={k:p.get(k) for k in fields};p.update(fields);p['decision_revision']=fields.get('decision_revision',decision)
        changes.append({'repere':ref,'decision':decision,'avant':before,'apres':fields,'retour_humain':feedback[ref].get('avis_humain')})
    for p in proposals:
        p.update(necessite_parent='à préciser' if p['parent'] else 'sans parent',role_dans_reponse='non hiérarchisé',propos_parent_vise=None,preuve_parent=None,statut_relecture='non relu',decision_revision='Proposition inchangée; aucun accord déduit d’une cellule vide.')
        h=feedback[p['repere']]
        assert h['commentaire_original']==p['texte']
        assert h['parent']==(p['parent'] or 'Aucun parent : commentaire principal.')
        if any(h.get(k) not in [None,''] for k in ['avis_humain','commentaire_humain']):
            p['statut_relecture']='retour reçu à interpréter'
        if str(h.get('avis_humain') or '').strip().lower()=='ok':
            p['statut_relecture']='accord exprimé sur cette ligne'
            p['decision_revision']='Conserver la proposition; accord de relecture enregistré sans en déduire une vérité factuelle.'
    revise('L033-P1','Conserver la critique de police, explicite dans la réponse, et la replacer dans la défense du mouvement.',necessite_parent='utile, mais non indispensable pour la critique de police',role_dans_reponse='argument secondaire dans une défense des manifestants',propos_parent_vise='Généralisation de jeunes qui cassent tout et ne veulent pas travailler.',preuve_parent="I do not understand why young people smash everything.",ambiguite='La réponse défend le caractère pacifique du mouvement et critique aussi des actes policiers. Elle ne démontre pas directement que tous les manifestants travaillent.',statut_relecture='révision proposée après réserve humaine')
    revise('L033-P2','Rendre visible la contestation du parent comme axe interactionnel principal, sans attribuer au parent les positions de la réponse.',cible='Généralisation du parent sur les jeunes et les destructions',proposition='Assimilation du mouvement à des jeunes destructeurs',necessite_parent='indispensable pour identifier la généralisation contestée',role_dans_reponse='axe principal proposé : défense des manifestants',propos_parent_vise='Les jeunes cassent tout; généralisation sur les Français et le travail.',preuve_parent="I do not understand why young people smash everything.",ambiguite='La majorité pacifique est explicitement défendue. Le reproche de non-travail est un contexte, pas une assertion factuellement réfutée par cette seule réponse.',statut_relecture='révision proposée après réserve humaine')
    revise('L033-P3','Conserver une critique médiatique distincte, comme appui au même échange et hors pourcentages police/participants.',necessite_parent='utile pour la fonction de réponse; critique des médias lisible seule',role_dans_reponse='appui contextuel : critique du cadrage médiatique',propos_parent_vise='Représentation du mouvement comme destructeur.',preuve_parent="I do not understand why young people smash everything.",ambiguite='Un commentaire et trois positions ou fonctions distinctes, pas trois commentaires. La hiérarchie principal/secondaire est proposée, non validée.',statut_relecture='révision proposée après réserve humaine')
    revise('L059-P1','Conserver l’argument précis et ARG_AUTRE : identifiable ne signifie pas déjà couvert par une famille validée.',decision_revision='Argument interprétable, hors dictionnaire actuel. Candidat à examiner : utilité préventive de l’intervention. Pas de fusion automatique avec A01.',necessite_parent='utile, non indispensable',role_dans_reponse='défense de l’utilité de la police',statut_relecture='accord accompagné d’une question de dictionnaire')
    revise('L005-P1','Retirer A05 : le passage sur le payeur ne permet pas de stabiliser le mécanisme économique.',proposition='Jugement dépréciatif sur les casseurs, associés au non-travail',code='ARG_AMBIGU',intitule='Argument ambigu',argument_precis=None,preuve_position='Pour tout les casseur il on rien a foutre',preuve_argument='il travail pas',statut_argument='ambigu',incertitude='modérée',ambiguite='Le non-travail est affirmé par l’auteur, sans être vérifié. Son rôle justificatif et le lien exact avec la question du payeur restent à discuter; ne pas en faire un coût établi pour les classes moyennes.',exploitation='critique des casseurs identifiable; argument exclu des familles économiques tant que non validé',statut_relecture='correction proposée après remarque humaine')
    revise('L005-P2','Retirer cette allusion isolée de l’analyse principale, à la demande de l’humaine, sans effacer le texte.',pertinence='contextuelle',exploitation='exclu de l’analyse principale',decision_revision='Allusion conservée pour traçabilité; aucune nouvelle position par acteur comptée.',statut_relecture='exclusion du périmètre demandée par l’humaine')
    revise('L063-P1','Conserver le résumé jugé juste et suspendre A07 : aucune revendication précise n’est explicitement confrontée ici aux actes.',code='ARG_AUTRE',intitule='Autre argument',ambiguite='Le motif personnel et le déni de cause sont explicites. Le regroupement A07 est trop large si aucune revendication précise n’est opposée aux actes. Candidat non activé : motivations opportunistes attribuées aux auteurs de dégâts.',statut_relecture='accord sur le résumé; famille à valider')
    revise('L037-P1','Respecter l’exclusion du périmètre principal sans nier l’hostilité générale explicite.',pertinence='hors sujet précis violences et dégâts',exploitation='exclu de l’analyse principale',decision_revision='La critique générale de police ne décrit pas un acte violent ou un dégât identifié.',statut_relecture='exclusion du périmètre demandée par l’humaine')
    revise('L037-P2','Maintenir la non-exploitabilité déjà indiquée, sans inventer un accord humain sur cette ligne vide.',pertinence='incertaine',exploitation='non exploitable dans l’analyse principale',ambiguite='Objet de it non identifié; ligne non renseignée par l’humaine. Exclusion proposée par l’assistant, non validation humaine.',statut_relecture='non relu; exclusion analytique proposée')
    # Contexte nécessaire : décision explicite de lecture, pas une propagation des jugements du parent.
    for ref,status,role in [
        ('L042-P1','indispensable pour comprendre le gazage contesté','contestation du sans raison du parent'),
        ('L065-P1','utile, critique policière lisible seule','réponse au reproche de viser la police'),
        ('L065-P2','utile, jugement sur les casseurs lisible seul','concession ou accord partiel'),
        ('L070-P1','indispensable pour savoir ce qui est confondu','contestation de la généralisation à la jeunesse'),
        ('L077-P1','utile, critique de répression lisible seule','argument distinct au sein d’une réponse'),
        ('L077-P2','indispensable pour identifier la thèse contestée','contestation du payeur allégué'),
        ('L045-P1','utile, accusation lisible seule','réattribution des désordres'),
        ('L045-P2','utile, accusation lisible seule','réattribution de responsabilité')]:
        byid[ref]['necessite_parent']=status;byid[ref]['role_dans_reponse']=role
    for p in proposals:
        for field in ['preuve_position','preuve_argument']:
            for q in p[field].split(' | ') if p[field] else []:assert q in p['texte'],(p['repere'],q)
        if p['preuve_parent']:assert p['preuve_parent'] in p['parent']
        assert p['texte']==next(r['texte'] for r in baseline['annotations'] if r['repere']==p['repere'])
    root=BASE.parents[2]
    sources=[json.loads(l) for l in (root/'classification_v02/commentaires_500.jsonl').read_text().splitlines()]
    candidates=[['CANDIDAT — utilité préventive de l’intervention','L’intervention est défendue parce que son absence permettrait des dégâts.','ARG_AUTRE maintenu; ne pas assimiler à une critique d’inefficacité A01.','L059','Un exemple clair dans ce lot20; ne pas créer une famille active automatiquement.'],
        ['CANDIDAT — motivations opportunistes attribuées aux auteurs de dégâts','Le comportement est expliqué par le plaisir de casser ou un intérêt propre, plutôt que par une cause.','ARG_AUTRE maintenu pour L063-P1; définition et frontière avec A07 à valider.','L063 ; L046 ; L085','Extraits des textes déjà collectés, pas des faits établis.']]
    examples=[['L063',sources[62]['texte']],['L046',sources[45]['texte']],['L085',sources[84]['texte']]]
    report={'statut':'revision_proposee_non_validee','source_humaine_sha256':hashlib.sha256(HUMAN.read_bytes()).hexdigest(),'commentaires':20,'positions_conservees':len(proposals),'lignes_humaines_renseignees':sum(any(r.get(k) not in [None,''] for k in ['avis_humain','commentaire_humain']) for r in received),'source_humaine':received,'journal':changes,'propositions':proposals,'candidats_dictionnaire':candidates,'exemples_candidat_opportunisme':examples,'limite':'Aucune mesure de performance. Les champs vides ne valent pas accord. Hiérarchies et catégories proposées restent à valider.'}
    (BASE/'revision_proposee.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    out=Workbook();out.remove(out.active)
    guide=[['Statut','Révision proposée après relecture humaine, sans API ni apprentissage; les autres fichiers du projet et le dashboard ne sont pas modifiés.'],['Lire','Révision côte à côte : texte complet, parent, proposition ajustée, ton retour exact et explication de la révision. Avis/remarque v2 sont vides pour une éventuelle réponse.'],['Parent','Un lien de réponse ne suffit pas à établir la pertinence. Parent indispensable, utile ou sans nécessité doivent être distingués selon chaque position.'],['L033','Un commentaire, trois lignes. La défense du mouvement contre la généralisation du parent est proposée comme axe principal; critiques policière et médiatique sont conservées sans devenir trois commentaires.'],['Dictionnaire','Les A01–A12 et M01 sont des familles proposées manuellement après lecture exploratoire des90 textes. Ce ne sont pas des catégories apprises ni une vérité de référence.'],['Autre argument','Identifiable mais non couvert. Conserver résumé et preuve, puis examiner les récurrences avant de proposer une nouvelle catégorie. Ni absence ni erreur automatique.'],['Ambigu','Plusieurs lectures possibles : ne pas sélectionner un mécanisme économique ou une intention sans appui.'],['Validation','Une remarque humaine peut valider le résumé mais pas la famille. Les lignes sans remarque restent non relues. Ce pilote sert au développement, pas à l’évaluation indépendante.'],['Textes longs','Textes entiers dans les cellules. Lecture verticale proposée pour contourner la hauteur maximale Excel.']]
    table(out,'Guide',['rubrique','consigne'],guide,{'rubrique':25,'consigne':115})
    view=[];details=[]
    for p in proposals:
        h=feedback[p['repere']];summary='\n'.join(['Cible : '+p['cible'],'Proposition : '+p['proposition'],'Position : '+p['position'],'Argument : '+p['code']+' — '+p['intitule'],'Précis : '+(p['argument_precis'] or 'Aucun résumé stabilisé'),'Preuve position : '+p['preuve_position'],'Preuve argument : '+(p['preuve_argument'] or 'Aucune'),'Statut argument : '+p['statut_argument'],'Incertitude : '+p['incertitude'],'Exploitation : '+p['exploitation'],'Limites : '+p['ambiguite']])
        relation='\n'.join(['Nécessité du parent : '+p['necessite_parent'],'Rôle dans la réponse : '+p['role_dans_reponse'],'Propos parent visé : '+(p['propos_parent_vise'] or 'Non précisé'),'Preuve parent : '+(p['preuve_parent'] or 'Non retenue')])
        view.append([p['repere'],p['texte'],p['parent'] or 'Aucun parent',summary,relation,h.get('avis_humain'),h.get('commentaire_humain'),p['statut_relecture'],p['decision_revision'],'',''])
        details.append([p['repere'],p['cible'],p['proposition'],p['position'],p['code'],p['intitule'],p['argument_precis'],p['preuve_position'],p['preuve_argument'],p['statut_argument'],p['incertitude'],p['necessite_parent'],p['role_dans_reponse'],p['exploitation'],p['ambiguite'],p['statut_relecture']])
    heads=['repere','texte_original','parent','proposition_ajustee','relation_au_parent','avis_humain_original','remarque_humaine_originale','statut_relecture','decision_expliquee','avis_humain_v2','remarque_humaine_v2']
    s=table(out,'Révision côte à côte',heads,view,{'repere':15,'texte_original':80,'parent':65,'proposition_ajustee':90,'relation_au_parent':65,'avis_humain_original':65,'remarque_humaine_originale':50,'decision_expliquee':65,'avis_humain_v2':24,'remarque_humaine_v2':65})
    for row in s.iter_rows(min_row=2):
        s.row_dimensions[row[0].row].height=390
        for c in row:
            if c.column in [10,11]:c.fill=PatternFill('solid',fgColor='FFF3CA')
    d=DataValidation(type='list',formula1='"accord,désaccord,à discuter"',allow_blank=True);s.add_data_validation(d);d.add(f'J2:J{s.max_row}')
    table(out,'Détails révisés',['repere','cible','proposition','position','code_argument','intitule','argument_precis','preuve_position','preuve_argument','statut_argument','incertitude','necessite_parent','role_dans_reponse','exploitation','limites','statut_relecture'],details,{'argument_precis':75,'limites':80,'preuve_position':65,'preuve_argument':65})
    table(out,'Retours humains originaux',headers,[[r.get(k) for k in headers] for r in received],{'commentaire_original':80,'parent':65,'proposition_IA':90,'avis_humain':80,'commentaire_humain':60})
    table(out,'Journal des ajustements',['repere','decision','avant','apres','retour_humain'],[[r['repere'],r['decision'],json.dumps(r['avant'],ensure_ascii=False),json.dumps(r['apres'],ensure_ascii=False),r['retour_humain']] for r in changes],{'decision':80,'avant':90,'apres':90,'retour_humain':70})
    dh=['code','intitule','definition','inclusion','exclusion','exemple1','exemple2']
    table(out,'Dictionnaire conservé',dh,[[r.get(k) for k in dh] for r in baseline['dictionnaire']],{'intitule':65,'definition':70,'inclusion':65,'exclusion':65})
    table(out,'Catégories à discuter',['candidat_non_active','definition_proposee','decision','references','limites'],candidates,{'candidat_non_active':60,'definition_proposee':80,'decision':80,'limites':75})
    table(out,'Exemples de récurrence',['repere','texte_deja_collecte'],examples,{'texte_deja_collecte':125})
    vertical=[]
    for n in baseline['ordre_commentaires']:
        c=next(p for p in proposals if p['ordre']==n)
        for label,text in [(f'L{n:03} — texte',c['texte']),('Parent',c['parent'] or 'Aucun parent')]:
            for line in text.split('\n'):
                for part in textwrap.wrap(line,width=110,replace_whitespace=False,drop_whitespace=False) or ['']:vertical.append([label,part])
        vertical.append(['',''])
    v=table(out,'Lecture verticale',['repere_ou_type','texte_par_bloc'],vertical,{'repere_ou_type':25,'texte_par_bloc':125})
    for i in range(2,v.max_row+1):v.row_dimensions[i].height=32
    out.active=out.sheetnames.index('Révision côte à côte')
    file=BASE/'REVISION_01_retours_parent_arguments.xlsx';out.save(file)
    check=load_workbook(file,read_only=True)
    assert check.active.title=='Révision côte à côte'
    for row,p in zip(check['Révision côte à côte'].iter_rows(min_row=2,values_only=True),proposals):
        assert row[1]==p['texte'] and row[2]==(p['parent'] or 'Aucun parent')
        assert row[5]==feedback[p['repere']].get('avis_humain')
        assert row[6]==feedback[p['repere']].get('commentaire_humain')
        assert row[9] is None and row[10] is None
    check.close()
    print(f"{report['lignes_humaines_renseignees']} lignes avec retours reçus; {len(changes)} décisions proposées; 20 commentaires / {len(proposals)} lignes conservés.")

if __name__=='__main__':main()
