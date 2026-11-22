"""Précontrôle documentaire hors réseau; aucune certification des images."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'methodologie/pilote_v1/tri_evenement_france/metadata_api_snapshot.json'

def precontrole(video):
    s=video['snippet'];evidence=[]
    for field in ['title','description']:
        text=s.get(field,'')
        for match in re.finditer(r'(?i)\b(?:17\s*(?:octobre|october|/\s*10)|(?:18|22|24)\s*(?:octobre|october|/\s*10)|1961|2026|Paris|France|Limoges|Marseille|Toulouse|Grenoble|Clermont)\b',text):
            evidence.append({'champ':field,'extrait':text[max(0,match.start()-50):min(len(text),match.end()+90)]})
    full=s.get('title','')+'\n'+s.get('description','')
    flags=[]
    if '1961' in full:flags.append('reference_1961_a_distinguer')
    if re.search(r'(?i)\b7\s+octobre',s.get('title','')) and re.search(r'(?i)\b17\s+octobre',s.get('description','')):
        flags.append('contradiction_7_17_octobre')
    if not s.get('description','').strip():flags.append('description_absente')
    if re.search(r'(?i)\b(?:18|22|24)\s*(?:octobre|/\s*10)',full):flags.append('autre_date_ou_suite_a_examiner')
    if re.search(r'(?i)intelligence artificielle|prétendue agression',full):flags.append('contenu_conteste_a_examiner')
    return {'video_id':video['id'],'url':'https://www.youtube.com/watch?v='+video['id'],
        'titre':s['title'],'publication_utc':s.get('publishedAt'),'indices_documentaires':evidence,
        'signalements_automatiques':flags,'statut':'a_verifier','preuves_examinees':[],
        'date_controle':None,'responsable_controle':None,'motif':'Indices extraits automatiquement; décision documentaire encore nécessaire.',
        'images_authentifiees':False}

def validate_review(review):
    if review['statut'] not in ['a_verifier','lien_plausible','rattachement_etaye','autre_evenement','suites']:
        raise ValueError('Statut de vérification inconnu')
    if review.get('images_authentifiees') is not False:
        raise ValueError('Ce registre ne certifie pas les images')
    if review['statut']=='rattachement_etaye':
        if not review.get('responsable_controle') or not review.get('date_controle') or not review.get('motif','').strip():
            raise ValueError('Contrôle étayé sans responsable, date ou motif')
        datetime.fromisoformat(review['date_controle'].replace('Z','+00:00'))
        proofs=review.get('preuves_examinees',[])
        if not proofs or not all(p.get('url','').startswith('https://') and p.get('passage','').strip()
            and p.get('type') in ['reportage_examine','transcription_examinee','source_concordante'] for p in proofs):
            raise ValueError('Preuve examinée manquante : un titre seul ne suffit pas')
        if not any(p.get('etaye_date_evenement') is True and p.get('etaye_lieu_france') is True for p in proofs):
            raise ValueError('Date de l’événement et lieu français non étayés')

def attach(scope,review,video_id):
    result=dict(scope)
    if review is None:
        review={'video_id':video_id,'statut':'a_verifier','motif':'Aucun contrôle documentaire fourni.',
                'images_authentifiees':False,'preuves_examinees':[]}
    if review['video_id']!=video_id:raise ValueError('Vérification associée à une autre vidéo')
    validate_review(review)
    result['verification_video']=review
    # Deux conditions indépendantes : rattachement vidéo étayé ET commentaire admissible.
    result['documentaire_candidat']=bool(scope['documentaire_candidat'] and review['statut']=='rattachement_etaye')
    result['controle_video_requis_pour_statistiques']=True
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata',type=Path,default=SOURCE)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Choisir un nouveau fichier pour préserver les contrôles existants')
    source=json.loads(args.metadata.read_text());videos=[precontrole(v) for v in source['items']]
    if len({v['video_id'] for v in videos})!=len(videos):raise ValueError('Vidéo dupliquée')
    output={'version':'verification-evenement-1.0','objet':'Vidéo traitant de la mobilisation du 17 octobre 2026 en France; pas authentification de chaque scène.',
        'methode':'Extraction de repères dans titre/description; publication conservée séparément. Aucun visionnage, transcription ou recoupement exécuté.',
        'source_sha256':hashlib.sha256(args.metadata.read_bytes()).hexdigest(),
        'metadata_recuperees_le':source.get('requested_at_utc'),'generation_utc':datetime.now(timezone.utc).isoformat(),
        'videos':videos}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(videos)} vidéos précontrôlées; 0 rattachement étayé automatiquement.')

if __name__=='__main__':main()
