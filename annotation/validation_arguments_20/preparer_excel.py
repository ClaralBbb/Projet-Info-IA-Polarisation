"""Exporte les propositions conversationnelles séparément, sans modifier les annotations sources."""
import hashlib,json,math,textwrap
from pathlib import Path
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.worksheet.datavalidation import DataValidation

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
ORDER=[3,2,15,33,42,65,68,90,59,5,27,69,63,70,74,77,45,37,29,13]
# Dictionnaire PROVISOIRE issu de la proposition conversationnelle, non validé.
DICTIONARY=[
('A01','Défaillance du maintien de l’ordre','Absence, incapacité ou inefficacité supposée face aux dégâts.','Absence ou défaut de prévention lié aux dégradations.','Complicité volontaire à distinguer; force excessive.','L003 : police impuissante','L068 : dégâts et absence policière'),
('A02','Laisser-faire ou complicité attribués aux autorités','Absence de réaction présentée comme voulue ou complice.','Intention ou complicité exprimée.','Ne pas déduire une intention de la seule absence.','L007 : État complice faute de sanctions','L090 : laisser-faire voulu'),
('A03','Force non ciblée contre des personnes présentées comme pacifiques','Critique du traitement de personnes pacifiques ou non impliquées.','Absence de distinction entre fauteurs de troubles et autres personnes.','Insulte générale; blessure sans raisonnement de non-ciblage.','L015 : why attack everyone?','L033 : marches pacifiques gazées'),
('A04','Violences antérieures invoquées pour justifier une riposte','Une réaction est défendue comme réponse à une violence antérieure.','Lien entre agression préalable alléguée et réponse justifiée.','Prédiction seule; mérite punitif sans raison précise.','L042 : violences contre policiers invoquées','L087 : violences contre enfants invoquées'),
('A05','Coût collectif et dépenses détournées des besoins sociaux','Critique des dégâts par leur financement ou les arbitrages de dépenses.','Repayer les biens; réparation en concurrence avec besoins collectifs.','Perte d’emploi individuelle sans raisonnement collectif.','L027 : biens à repayer','L083 : réparations contre budget scolaire'),
('A06','Préjudice économique aux travailleurs et commerçants','Critique par les pertes subies par des tiers.','Commerces, emplois, investissement personnel.','Coût fiscal général; mécanisme économique non explicité.','L043 : commerces financés par leurs propriétaires','L069 : perte d’emploi rapportée'),
('A07','Décalage entre les actes et les revendications affichées','Les actes sont présentés comme étrangers ou contraires à la cause.','Contradiction actes / cause revendiquée.','Simple insulte; majorité / minorité sans ce raisonnement.','L028 : aucun rapport avec revendications lycéennes','L064 : biens pillés opposés à la vie chère'),
('A08','Refus de généraliser les violences à l’ensemble du mouvement','Distinction entre majorité pacifique et partie violente.','Contestation d’une condamnation collective.','Négation de toute violence; justification du pillage.','L031 : majorité pacifique','L055 : marches pacifiques et violences reconnues'),
('A09','Absence d’écoute ou de dialogue alimentant l’escalade','Manque d’écoute relié aux dégâts ou dialogue opposé à la confrontation.','Lien causal ou alternative exprimés.','Critique générale du gouvernement; soutien à la casse inféré.','L074 : jeunes ignorés puis casse','L077 : dialogue plutôt que répression'),
('A10','Provocations ou dégradations attribuées à des infiltrés liés aux autorités','Désordres expliqués par des provocations ou une instrumentalisation alléguées.','Lien explicite entre groupes, autorités et provocation / dégâts.','Force excessive ordinaire; infiltrés sans lien identifiable.','L036 : groupes dans des rangs policiers accusés','L045 : casseurs policiers infiltrés allégués'),
('A11','Incitation politique alléguée aux violences','Acteurs politiques ou relais accusés d’encourager ou organiser la violence.','Appels, organisation, incitation attribués.','Affiliation seule; critique politique sans lien avec la violence.','L007 : influenceurs accusés de relayer des appels','L062 : incitation attribuée à Mélenchon et LFI'),
('A12','Attribution de responsabilité jugée insuffisamment fondée','Accusation contestée par demande de preuve ou contre-exemple.','Contestation du fondement causal ou de la preuve.','Désaccord sans raison; demande de preuve prise pour preuve d’innocence.','L072 : demande de preuves','L036 : casse antérieure à LFI invoquée'),
('M01','Surexposition médiatique des violences au détriment du mouvement','Sélection médiatique supposée occulter revendications ou marches pacifiques.','Violences privilégiées au détriment du reste du mouvement.','Minimisation des violences; critique générale sans raison.','L001 : revendications absentes','L019 : pillages montrés, marches ignorées'),
('ARG_ABSENT','Argument absent','Position présente sans raison identifiable.','Absence de justification après lecture.','Non annoté ne signifie pas absent.','L037 : I don’t like Paris police','L013 : description sans justification évaluative'),
('ARG_AUTRE','Autre argument','Raisonnement interprétable non couvert par une famille provisoire.','Résumé précis et preuve obligatoires.','Ne pas employer pour une lecture indécidable.','L059 : utilité préventive','L029 : objet dit volé opposé au déni'),
('ARG_AMBIGU','Argument ambigu','Plusieurs raisonnements restent possibles.','Impossible de choisir sans hypothèse externe.','Ne pas choisir un mécanisme arbitraire.','L002 : Amazon / Zalando','Pas de second exemple imposé'),
]
D={r[0]:r[1] for r in DICTIONARY}
PROPOSALS=[]
def add(n,cible,proposition,position,code,precis,preuve,statut,incertitude,ambiguite='',pertinence='directe',exploitation='exploitable',preuve_argument=None,parent_utilise=False):
    PROPOSALS.append(dict(ordre=n,cible=cible,proposition=proposition,position=position,code=code,intitule=D[code],argument_precis=precis,preuve_position=preuve,preuve_argument=preuve_argument or '',statut_argument=statut,incertitude=incertitude,ambiguite=ambiguite,pertinence=pertinence,exploitation=exploitation,parent_utilise=parent_utilise))
add(3,'Police','Capacité à empêcher les dégradations','critique','A01','L’auteur considère la police responsable des dégradations en raison de son incapacité supposée à les empêcher.','La police est incapable de quoi que ce soit.','explicite','faible','Faits et responsabilité allégués, non vérifiés.',preuve_argument='La police était impuissante face à ces vandales. | Elle est responsable de tous les graffitis sur les murs')
add(2,'Casseurs','Sens du remerciement ironique Amazon / Zalando','indéterminable','ARG_AMBIGU',None,'AMAZON VOUS REMERCIE','ambigu','forte','Ironie probable. Ne pas choisir entre revente, commerce en ligne ou autre mécanisme économique.',exploitation='à revoir; exclu des statistiques automatiques de position')
add(15,'Police','Force contre tous les participants','critique','A03','La présence possible de fauteurs de troubles ne justifierait pas d’attaquer tout le monde.','but why attack everyone?','explicite','faible',preuve_argument='some protesters are there just to cause chaos. Ok..but why attack everyone?')
add(33,'Police','Gazage de marches présentées comme pacifiques','critique','A03','L’auteur critique l’usage de gaz et la dispersion de personnes décrites comme pacifiques.','absolutely peaceful marches getting gassed and scattered by the police','explicite','faible','Accusations non vérifiées.',preuve_argument='absolutely peaceful marches getting gassed and scattered by the police',parent_utilise=True)
add(33,'Généralisation des destructions à tous les manifestants','Assimilation du mouvement entier aux destructions','critique','A08','Une majorité de marches décrites comme pacifiques est distinguée d’une poignée de personnes destructrices.','many marches were peaceful, it only takes a handful of people to destroy stuffs.','explicite','faible','Critique d’une généralisation; pas un soutien à toutes les actions des manifestants.',preuve_argument='many marches were peaceful, it only takes a handful of people to destroy stuffs.',parent_utilise=True)
add(33,'Médias','Sélection des violences et images choquantes','critique','M01','L’auteur reproche aux médias d’insister sur les images violentes et d’omettre des manifestations pacifiques.','medias that will obviously emphasize on violence and shocking images','explicite','faible','Position contextuelle, distincte de la position sur la police.',pertinence='contextuelle',exploitation='exploitable pour les médias; hors pourcentages police / participants',preuve_argument="nor will they show you chill family-friendly demonstrations",parent_utilise=True)
add(42,'Forces ayant gazé les participants, identifiées avec le parent','Justification du gazage évoqué par le parent','favorable','A04','Le gazage est défendu comme une réponse à des violences antérieures alléguées contre des policiers.','Pas sans raison','explicite','faible','Soutien à la justification de cette intervention, pas à tout acte policier.',preuve_argument='qui a commencer par du lynchage et tabassage de homme et de femme policier',parent_utilise=True)
add(65,'Certains policiers','Dangerosité des actes décrits contre des civils et enfants','critique','ARG_AUTRE','Des actes présentés comme gravement dangereux pour des civils et enfants sont invoqués pour critiquer certains policiers.','les policiers te tirent au flashbang en plein visage','explicite','faible','Restriction à certains policiers; qualification juridique et faits non vérifiés.',preuve_argument='tazent des enfants isolés, foncent sur des civils en voiture',parent_utilise=True)
add(65,'Casseurs','Destructions matérielles et demande de sanction','critique','ARG_AUTRE','La responsabilité alléguée dans des destructions matérielles fonde la demande de sanction.','les casseurs sont responsables de destruction matérielle et doivent être punis','explicite','faible','Deux cibles distinctes : ne pas fusionner avec la critique de policiers.',preuve_argument='les casseurs sont responsables de destruction matérielle',parent_utilise=True)
add(68,'Police','Absence d’intervention face à des dégâts','critique','A01','L’absence policière est rapprochée de dégradations d’une porte de mairie.','pas un flic a  proximité','implicite étayé','modérée','Reproche probable sous forme interrogative; frontière observation / critique à valider.',exploitation='à revoir avant comptage automatique',preuve_argument='Certains fracassent là porte de la mairie ...et pas un flic a  proximité')
add(90,'Police et responsables de l’intervention','Laisser-faire volontaire allégué','critique','A02','L’auteur interprète l’absence prolongée puis un bref passage policier comme un laisser-faire voulu.','ces voulu je vous le dit','explicite','faible','L’intention attribuée n’est pas un fait établi.',preuve_argument='il y avait aucun policier aucun civil aucun crs jusqu’à 23h')
# Corriger uniquement la citation ci-dessus pour conserver l’apostrophe exacte de la source.
PROPOSALS[-1]['preuve_argument']="il y avait aucun policier aucun civil aucun crs jusqu'à 23h"
add(59,'Police','Utilité préventive de l’intervention','favorable','ARG_AUTRE','Les conséquences invoquées de la non-intervention servent à défendre l’utilité de la police.','voilà ce que ça donne quand la police n’intervient pas','implicite étayé','modérée','Le détail des conséquences n’est pas explicité dans la réponse. Ne pas compter comme soutien aux coups.',preuve_argument='voilà ce que ça donne quand la police n’intervient pas',parent_utilise=True)
add(5,'Casseurs','Coût des conséquences pour les travailleurs','critique','A05','Les travailleurs des classes moyennes supporteraient les coûts des dégâts.','Pour tout les casseur il on rien a foutre','implicite étayé','modérée','Formulation peu structurée; ne pas inférer un mécanisme de paiement précis.',preuve_argument='qui va payer les travailleurs de classes moyen')
add(5,'Acteur non précisément identifié','Allusion à une réponse ferme par le karsher','indéterminable','ARG_ABSENT',None,'comme à dit Sarkozy coup de karsher','absent','forte','Allusion punitive séparée; mesure et agent non précisément identifiés. Pas de justification supplémentaire extraite.',exploitation='à revoir; hors statistiques par acteur')
add(27,'Auteurs des dégradations parmi les mobilisés','Refus de la casse et de son coût','critique','A05','Les biens collectifs déjà financés devront être payés de nouveau.','Pas besoin de tou cassé pour autant...','explicite','faible','Ne pas convertir la solidarité du même texte en soutien aux dégâts.',preuve_argument='On vas continuer à payer c’est fameuse choses')
PROPOSALS[-1]['preuve_argument']='On vas continuer à payer c\'est fameuse choses'
add(27,'Collectif auquel l’auteur s’associe','Solidarité avec le collectif mobilisé','favorable','ARG_ABSENT',None,'Force à nous tous en vrai...','absent','modérée','Soutien collectif distinct de la critique des dégâts. L’hypothèse sur les années80–90 ne devient pas une justification actuelle.',pertinence='contextuelle',exploitation='hors statistiques sur la légitimité des dégâts')
add(69,'Auteurs des pillages et dégradations, sans identité précise','Conséquences des dégâts sur les emplois','critique','A06','Les dégâts menaceraient les emplois; l’auteur rapporte une perte de son propre emploi.','Le pillage et les magasins cassés','explicite','faible','Témoignage non vérifié; pas d’identité de groupe établie.',preuve_argument="J'ai perdu mon emploi pour ces raisons.")
add(63,'Pillards / casseurs qualifiés par l’auteur','Actes présentés comme étrangers à une cause','critique','A07','Les actes sont décrits comme servant une recherche personnelle de destruction et de vol plutôt qu’une cause.','ils ne servent aucune cause si ce n\'est la leur','explicite','faible','Motivations attribuées par l’auteur, non vérifiées.',preuve_argument='se défouler, détruire et voler...')
add(63,'Attribution politique des casseurs à l’ultragauche','Fondement de la qualification politique','critique','ARG_AUTRE','L’auteur conteste la qualification politique en présentant les actes comme poursuivant des intérêts propres.','Comment peuvent-ils affirmer que ces casseurs sont de l\'ultra-gauche ?!','implicite étayé','modérée','Ne prouve pas l’absence d’affiliation; frontière avec A12 à valider, sans forcer une famille.',exploitation='exploitable comme contestation; pas comme soutien à un groupe politique',preuve_argument='ils ne servent aucune cause si ce n\'est la leur')
add(70,'Généralisation à toute la jeunesse dans le parent','Assimilation jeunesse / casseurs','critique','A08','La réponse distingue les casseurs de la jeunesse prise collectivement.','Non juste des casseurs. Il ne faut pas confondre.','implicite étayé','modérée','Distinction suffisante comme argument implicite ? À valider. Pas de soutien à toutes les actions des jeunes.',preuve_argument='Non juste des casseurs.',parent_utilise=True)
add(74,'Lien entre absence d’écoute et casse','Explication de l’escalade','descriptive','A09','La casse est reliée à une mobilisation décrite comme non entendue.','non et apres ont s\'etonne de la casse','implicite étayé','modérée','Lien causal suggéré; ne pas transformer en justification morale. Critique implicite des autorités à discuter séparément.',exploitation='analyse des arguments; hors soutien / critique de la casse',preuve_argument="est ce qu'ils ont été entendus non et apres ont s'etonne de la casse")
add(77,'Pouvoir répressif non nommé','Répression sans discussion','critique','A09','Dialogue et mesures concrètes sont présentés comme une alternative à la répression.','être dans la répression sans discussion','explicite','faible','Ne pas fusionner avec le désaccord sur les assurances.',preuve_argument='Il suffirait pourtant juste des mesures concrètes et un dialogue',parent_utilise=True)
add(77,'Affirmation du parent : le contribuable paiera','Prise en charge du coût des dégâts','critique','ARG_AUTRE','La couverture assurantielle alléguée est invoquée contre l’affirmation selon laquelle le contribuable paiera.','Non les assurances','explicite','faible','Contrats et conséquences financières non vérifiés; ne signifie pas soutien aux dégâts.',exploitation='analyse du débat sur le coût; pas soutien / critique d’un acteur violent',preuve_argument='tout le patrimoine et infrastructures français sont assuré.',parent_utilise=True)
add(45,'Policiers infiltrés allégués','Provocations servant à détourner les revendications','critique','A10','Des policiers infiltrés sont accusés de produire des désordres pour détourner les revendications.','casseurs policiers infiltrés afin de détourner la véritable cause','explicite','faible','Accusation non vérifiée; pas une accusation contre tous les policiers.',preuve_argument='afin de détourner la véritable cause de la manifestation',parent_utilise=True)
add(45,'Nuñez et responsables décrits comme protecteurs des agents','Protection alléguée d’agitateurs et violences contre lycéens','critique','A10','L’auteur attribue aux responsables une protection de la stratégie de provocation décrite.','soutenus, protégés par NUNEZ TORTIONNAIRE de lyceens','implicite étayé','modérée','Attribution accusatoire; portée de la cible et séparation des deux positions à valider.',preuve_argument='qui utilisent leurs agitateurs, casseurs policiers infiltrés',parent_utilise=True)
add(37,'Police parisienne','Appréciation générale de la police','critique','ARG_ABSENT',None,'I don’t like Paris police','absent','faible','Hostilité claire, mais aucun acte précis ni raison donné.',pertinence='contextuelle',exploitation='critique générale uniquement; hors usage précis de la force')
add(37,'Objet du pronom it non identifié','Soutien à la poursuite d’un objet non résolu','favorable','ARG_ABSENT',None,'I love it so much don’t stop it','absent','forte','Soutien explicite, cible inconnue. Ne pas supposer un soutien aux violences ou au mouvement.',pertinence='incertaine',exploitation='non exploitable par cible; à revoir')
add(29,'Déni d’implication du personnage décrit','Compatibilité du déni avec l’objet présenté comme volé','critique','ARG_AUTRE','La présence alléguée d’une bouteille volée est opposée au déni d’implication.','une bouteille de whisky volée dans la poche qui n\'a rien fait','explicite','faible','Ironie interprétable; vol non vérifié. Pas un soutien automatique à une sanction policière.',exploitation='contestation du déni uniquement',preuve_argument='une bouteille de whisky volée dans la poche')
add(13,'Unités policières','Identification des unités par les casques','descriptive','ARG_ABSENT',None,'ce avec les casques noirs et bande jaune ce sont les CRS','absent','faible','Description sans jugement évaluatif; exactitude technique non vérifiée.',pertinence='contextuelle',exploitation='non exploitable dans les pourcentages favorable / critique')

HUMAN=['avis_humain','correction_cible','correction_proposition','correction_position','correction_code_argument','correction_argument_precis','correction_preuve','correction_statut_argument','correction_ambiguite','commentaire_humain']
def write_sheet(w,name,headers,rows,widths):
    s=w.create_sheet(name);s.append(headers)
    for values in rows:s.append(values)
    for row in s:
        for c in row:
            if isinstance(c.value,str):c.data_type='s'
            c.alignment=Alignment(wrap_text=True,vertical='top')
    for c in s[1]:c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='244766')
    for i,h in enumerate(headers,1):
        s.column_dimensions[s.cell(1,i).column_letter].width=widths.get(h,24)
        if h in HUMAN:
            for row in s.iter_rows(min_row=2,min_col=i,max_col=i):row[0].fill=PatternFill('solid',fgColor='FFF3CA')
    s.freeze_panes='B2';s.auto_filter.ref=s.dimensions
    return s

def main():
    source=ROOT/'classification_v02/commentaires_500.jsonl'
    sources=[json.loads(l) for l in source.read_text().splitlines()]
    rows=[];seq={}
    for p in PROPOSALS:
        n=p['ordre'];c=sources[n-1];seq[n]=seq.get(n,0)+1
        for field in ['preuve_position','preuve_argument']:
            for quote in p[field].split(' | ') if p[field] else []:
                if quote not in c['texte']:raise ValueError(f'L{n:03} : citation non exacte {field}: {quote}')
        if p['statut_argument'] in ['absent','ambigu'] and p['argument_precis'] is not None:raise ValueError('Ne pas inventer un résumé pour absent ou ambigu')
        rows.append(dict(p,repere=f'L{n:03}-P{seq[n]}',comment_id=c['comment_id'],texte=c['texte'],parent=c['texte_parent'],chaine=c['chaine'],titre_video=c['titre_video']))
    assert list(dict.fromkeys(p['ordre'] for p in rows))==ORDER
    w=Workbook();w.remove(w.active)
    guide=[['Statut','Propositions exploratoires pour validation humaine, issues de la dernière réponse. Pas de vérité de référence ni de classement API.'],
        ['Sélection','Exactement les20 commentaires discutés. L003 signifie ordre_lot=3 du lot500, pas C003 du premier Excel.'],
        ['Lire','Vérification : texte complet, parent et proposition réunis. Plusieurs positions = plusieurs lignes avec le même commentaire.'],
        ['Corriger','Colonnes jaunes vides : accord/désaccord ou correction libre. Détails et corrections structurées dans Annotations détaillées. Ne pas confondre blanc et accord.'],
        ['Preuves','Citations exactes vérifiées dans le commentaire original; contexte parent conservé distinctement. Les textes ne sont pas tronqués.'],
        ['Argument','Explicite ou implicite étayé si interprétable; Argument absent et Argument ambigu sont des diagnostics, pas des arguments à compter. Autre argument exige un résumé fidèle.'],
        ['Incertitude','Concerne la lecture, pas la vérité des accusations. L’ironie n’entraîne pas automatiquement une position indéterminable.'],
        ['Exploitation','Un texte pertinent peut être exclu des statistiques de positions. Une explication causale ne prouve pas un soutien à la violence.'],
        ['Dictionnaire','A01–A12 et M01 sont provisoires. Seules les familles adaptées aux20 textes sont utilisées. ARG_ABSENT, ARG_AUTRE et ARG_AMBIGU sont réservés.'],
        ['Contexte','Le parent référencé n’est pas nécessairement le message exact visé dans le fil. Tous les parents disponibles sont joints, même si non nécessaires.'],
        ['Textes longs','Utiliser la barre de formule ou la lecture verticale si la hauteur maximale Excel masque la fin. Aucun texte n’est coupé dans les cellules.'],
        ['Périmètre','Aucune modification des annotations sources, du dashboard ou des fichiers de relecture existants. Aucun appel API.'],
    ]
    write_sheet(w,'Guide',['rubrique','explication'],guide,{'rubrique':25,'explication':115})
    heads=['repere','commentaire_original','parent','cible','proposition_evaluee','position','code_argument','argument_standardise','argument_precis','preuve_position','preuve_argument','statut_argument','incertitude','ambiguite','pertinence_thematique','exploitation_positions','parent_utilise','comment_id','chaine','titre_video',*HUMAN]
    detailed=[];simple=[]
    for p in rows:
        detailed.append([p['repere'],p['texte'],p['parent'],p['cible'],p['proposition'],p['position'],p['code'],p['intitule'],p['argument_precis'],p['preuve_position'],p['preuve_argument'],p['statut_argument'],p['incertitude'],p['ambiguite'],p['pertinence'],p['exploitation'],'oui' if p['parent_utilise'] else 'non nécessaire',p['comment_id'],p['chaine'],p['titre_video'],*['']*len(HUMAN)])
        summary='\n'.join(['Cible : '+p['cible'],'Proposition : '+p['proposition'],'Position : '+p['position'],'Argument : '+p['code']+' — '+p['intitule'],'Argument précis : '+(p['argument_precis'] or 'Non formulé : '+p['statut_argument']),'Preuve position : '+p['preuve_position'],'Preuve argument : '+(p['preuve_argument'] or 'Aucune citation argumentative retenue'),'Statut argument : '+p['statut_argument'],'Incertitude : '+p['incertitude'],'Ambiguïtés / limites : '+p['ambiguite'],'Analyse des positions : '+p['exploitation']])
        simple.append([p['repere'],p['texte'],p['parent'] or 'Aucun parent : commentaire principal.',summary,'',''])
    widths={'commentaire_original':85,'parent':75,'argument_precis':70,'preuve_position':65,'preuve_argument':65,'ambiguite':75,'proposition_evaluee':55,'cible':45,'argument_standardise':55,'exploitation_positions':65,'commentaire_humain':65}
    write_sheet(w,'Annotations détaillées',heads,detailed,widths)
    s=write_sheet(w,'Vérification',['repere','commentaire_original','parent','proposition_IA','avis_humain','commentaire_humain'],simple,{'repere':15,'commentaire_original':78,'parent':60,'proposition_IA':85,'avis_humain':22,'commentaire_humain':65})
    for row in s.iter_rows(min_row=2):
        lines=max(sum(max(1,math.ceil(len(line)/width)) for line in str(row[col].value or '').split('\n')) for col,width in [(1,75),(2,57),(3,82)])
        s.row_dimensions[row[0].row].height=min(409,max(110,(lines+2)*15))
    # Lecture verticale : petits blocs de texte complets pour contourner la limite de hauteur des cellules Excel.
    vertical=[]
    for n in ORDER:
        c=sources[n-1];vertical.append([f'L{n:03}','COMMENTAIRE ORIGINAL'])
        for label,text in [('Texte',c['texte']),('Parent',c['texte_parent'] or 'Aucun parent')]:
            for line in text.split('\n'):
                for part in textwrap.wrap(line,width=110,replace_whitespace=False,drop_whitespace=False) or ['']:
                    vertical.append([label,part])
        vertical.append(['',''])
    v=write_sheet(w,'Lecture sans masquage',['repere_ou_type','texte_original_par_bloc'],vertical,{'repere_ou_type':20,'texte_original_par_bloc':125})
    for r in range(2,v.max_row+1):v.row_dimensions[r].height=32
    write_sheet(w,'Dictionnaire provisoire',['code','intitule','definition','inclusion','exclusion','exemple1','exemple2'],DICTIONARY,{'intitule':60,'definition':65,'inclusion':65,'exclusion':65,'exemple1':55,'exemple2':55})
    for ws,column in [(s,'E'),(w['Annotations détaillées'],'U')]:
        d=DataValidation(type='list',formula1='"accord,désaccord,à discuter,problème de format"',allow_blank=True);ws.add_data_validation(d);d.add(f'{column}2:{column}{ws.max_row}')
    w.active=w.sheetnames.index('Vérification')
    output=OUT/'VALIDATION_20_ARGUMENTS_PROVISOIRES.xlsx';w.save(output)
    check=load_workbook(output,read_only=True)
    assert check.active.title=='Vérification'
    assert check['Vérification'].max_row==len(rows)+1
    for actual,p in zip(check['Vérification'].iter_rows(min_row=2,values_only=True),rows):
        assert actual[1]==p['texte'] and actual[2]==(p['parent'] or 'Aucun parent : commentaire principal.')
        assert actual[4] is None and actual[5] is None
    for actual in check['Annotations détaillées'].iter_rows(min_row=2,values_only=True):assert all(v is None for v in actual[-len(HUMAN):])
    check.close()
    manifest={'statut':'propositions_non_validees','source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'ordre_commentaires':ORDER,'commentaires':len(ORDER),'positions':len(rows),'methode':'Réannotation conversationnelle proposée; export uniquement, sans appel API.','annotations':rows,'dictionnaire':[dict(zip(['code','intitule','definition','inclusion','exclusion','exemple1','exemple2'],d)) for d in DICTIONARY]}
    (OUT/'propositions_et_dictionnaire.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(f'{len(ORDER)} commentaires, {len(rows)} positions. Textes/citations vérifiés, corrections humaines vides. Fichier : {output.name}, {output.stat().st_size} octets.')

if __name__=='__main__':main()
