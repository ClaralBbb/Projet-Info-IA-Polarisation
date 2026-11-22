"""Export hors ligne des décisions documentaires explicites; aucune classification LLM."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

ROOT = Path(__file__).resolve().parent
PILOTE = ROOT.parent

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def build():
    rows = [json.loads(line) for line in (PILOTE/'commentaires_50.jsonl').read_text().splitlines()]
    snapshot = read(ROOT/'metadata_api_snapshot.json')
    videos = {v['id']:v['snippet'] for v in snapshot['items']}
    decisions = {v['comment_id']:v for v in read(ROOT/'decisions_documentaires_50.json')['decisions']}
    assert len(rows) == len(decisions) == len(videos) == 50
    output = []
    for row in rows:
        d = decisions[row['comment_id']]
        assert d['video_id'] == row['video_id']
        evidence = d['preuve_commentaire_ou_parent']
        assert evidence['extrait'] in row['texte' if evidence['source']=='commentaire' else 'texte_parent']
        v = videos[row['video_id']]
        n = int(row['repere'][1:])
        status, reason = 'lien_plausible_non_confirme', 'Titre ou description rattachant la vidéo au 17 octobre; images et faits non vérifiés.'
        if n == 11:
            status, reason = 'autre_evenement_explicite', 'Le titre porte explicitement sur le 17 octobre 1961.'
        elif n in [23,32,35,37]:
            status, reason = 'suite_ou_autre_date_liee', 'Nouveau rassemblement ou appel les 18, 22 ou 24 octobre; contexte distinct du 17.'
        elif n == 26:
            status, reason = 'date_contradictoire_a_verifier', 'Le titre indique le 7 octobre et la description le 17 octobre; contradiction non résolue.'
        elif n == 28:
            status, reason = 'informations_insuffisantes', 'Paris est cité, mais ni titre ni description ne datent les faits; publication le 17 insuffisante.'
        warnings = []
        if n == 6:
            warnings.append('La description présente les images du couple comme probablement générées par IA et rapporte une absence de trace de l’agression. Décryptage à distinguer d’une preuve d’agression; vérification indépendante non effectuée.')
        if n in [15,25]:
            warnings.append('Allégation grave de décès attribué à la police dans le commentaire, non corroborée par cette revue documentaire.')
        if n == 13:
            warnings.append('La description ne précise pas le lieu ni l’auteur des images citées.')
        disposition = 'contexte_separe'
        if d['statut_commentaire']=='autre_evenement_explicite' or status=='autre_evenement_explicite':
            disposition = 'hors_corpus_principal'
        elif d['statut_commentaire']=='informations_insuffisantes' or status in ['informations_insuffisantes','date_contradictoire_a_verifier']:
            disposition = 'rattachement_a_verifier'
        elif d['statut_commentaire']=='lien_plausible_non_confirme' and status=='lien_plausible_non_confirme':
            disposition = 'candidat_non_verifie' if not warnings else 'candidat_avec_signalement'
        pub = datetime.fromisoformat(v['publishedAt'].replace('Z','+00:00'))
        output.append({**row, **d, 'titre_video_api':v['title'], 'chaine_api':v['channelTitle'],
            'publication_utc':v['publishedAt'], 'publication_paris':pub.astimezone(ZoneInfo('Europe/Paris')).isoformat(),
            'description_api':v['description'], 'url_video':'https://www.youtube.com/watch?v='+row['video_id'],
            'statut_video':status,'motif_video':reason,'date_des_faits_confirmee':False,
            'images_verifiees':False,'disposition_proposee':disposition,'signalements':warnings})
    write('tri_50.json', {'perimetre':'France entière; mobilisation du 17 octobre 2026, suites et contexte séparés',
        'nature':'Décisions documentaires proposées par assistant; sans visionnage ni validation factuelle indépendante.',
        'metadata_recuperees_le':snapshot['requested_at_utc'],'commentaires':output})
    counts = {'nombre_commentaires':len(output),'metadonnees_videos_accessibles':len(videos),
        'statuts_commentaires':dict(Counter(r['statut_commentaire'] for r in output)),
        'statuts_videos':dict(Counter(r['statut_video'] for r in output)),
        'dispositions_proposees':dict(Counter(r['disposition_proposee'] for r in output)),
        'faits_confirmes_independamment':0}
    write('bilan.json',counts)
    headers = ['Repère','Commentaire original','Parent du fil','Titre vidéo','Chaîne déclarée','Publication (Paris)','Lien vidéo','Description vidéo','Statut vidéo','Motif vidéo','Statut commentaire','Motif commentaire','Lieu du propos','Source de la preuve','Preuve textuelle','Disposition proposée','Signalements','Comment ID','Video ID']
    values=[]
    for r in output:
        values.append([r['repere'],r['texte'],r['texte_parent'],r['titre_video_api'],r['chaine_api'],r['publication_paris'],r['url_video'],r['description_api'],r['statut_video'],r['motif_video'],r['statut_commentaire'],r['motif'],r['lieu_du_propos'],r['preuve_commentaire_ou_parent']['source'],r['preuve_commentaire_ou_parent']['extrait'],r['disposition_proposee'],' | '.join(r['signalements']),r['comment_id'],r['video_id']])
    with (ROOT/'TRI_50_FRANCE.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f); writer.writerow(headers); writer.writerows(values)
    wb=Workbook(); ws=wb.active; ws.title='Tri documentaire 50'
    for vals in [headers]+values:
        ws.append(vals)
        # Les textes de commentaires ne doivent jamais être interprétés comme formules Excel.
        for cell in ws[ws.max_row]:
            if isinstance(cell.value,str): cell.data_type='s'
            cell.alignment=Alignment(vertical='top',wrap_text=True)
    for cell in ws[1]:cell.font=Font(bold=True)
    ws.freeze_panes='B2';ws.auto_filter.ref=ws.dimensions
    for col in ws.columns:ws.column_dimensions[col[0].column_letter].width=45
    ws.column_dimensions['B'].width=85;ws.column_dimensions['C'].width=75
    notice=wb.create_sheet('Lire avant')
    for text in ['Tri documentaire provisoire, France entière, 50 commentaires du pilote V1.', 'Aucun fait ni aucune image confirmé indépendamment. La publication ne date pas les scènes.', 'Les textes sont complets dans les cellules; la hauteur affichée peut nécessiter d’ouvrir la cellule.', 'Le parent est le parent disponible du fil; il ne prouve pas toujours le destinataire exact.', 'Les noms de chaînes sont ceux déclarés par l’API, sans authentification éditoriale.', 'Aucune correction humaine supplémentaire demandée à ce stade; les cas à vérifier sont identifiés.', 'Le dashboard et les annotations historiques restent inchangés.']:
        notice.append([text])
    notice.column_dimensions['A'].width=120
    wb.save(ROOT/'TRI_50_FRANCE.xlsx')
    write('provenance.json',{'generation':'Export déterministe hors ligne des décisions manuelles explicites; aucun appel LLM.', 'sources_sha256':{str(p.relative_to(PILOTE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [PILOTE/'commentaires_50.jsonl',ROOT/'metadata_api_snapshot.json',ROOT/'decisions_documentaires_50.json']}})
    print(json.dumps(counts,ensure_ascii=False,indent=2))
    return output

if __name__=='__main__':build()
