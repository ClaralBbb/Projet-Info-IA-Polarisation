"""Pipeline API V1. Simulation hors réseau par défaut; aucune annotation simulée."""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(__file__).resolve().parent
PILOTE = ROOT / 'methodologie/pilote_v1'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def scope_context(row,tri):
    """Jointure par identifiant + vidéo; jamais d'opinions historiques jointes."""
    if tri is None:
        return {'statut_video':'non_verifie','statut_commentaire':'non_verifie',
                'signalements':[], 'documentaire_candidat':False,'traitement':'rattachement_a_verifier'}
    if tri['video_id'] != row['video_id']:
        raise ValueError('Tri associé à une autre vidéo')
    v,c=tri['statut_video'],tri['statut_commentaire']
    flags=tri.get('signalements',[])
    plausible='lien_plausible_non_confirme'
    if 'autre_evenement_explicite' in [v,c]: treatment='hors_corpus_principal'
    elif v=='suite_ou_autre_date_liee': treatment='suites_separees'
    elif v!=plausible or c in ['informations_insuffisantes','non_verifie']: treatment='rattachement_a_verifier'
    elif c=='contexte_general_ou_comparaison': treatment='contexte_separe'
    elif c==plausible: treatment='candidat_avec_signalement' if flags else 'candidat_non_verifie'
    else: treatment='rattachement_a_verifier'
    return {k:tri.get(k) for k in ['statut_video','motif_video','statut_commentaire','motif',
        'preuve_commentaire_ou_parent','signalements','publication_utc','titre_video_api','description_api']} | {
        'documentaire_candidat':treatment=='candidat_non_verifie','traitement':treatment,
        'verification_factuelle':False}

def prepare(row,tri):
    required=['comment_id','video_id','texte','parent_id','texte_parent']
    if not set(required)<=set(row):raise ValueError('Champs source manquants')
    if not isinstance(row['texte'],str) or not row['texte'].strip():raise ValueError('Texte source vide ou invalide')
    for key in ['comment_id','video_id']:
        if not isinstance(row[key],str) or not row[key].strip():raise ValueError('Identifiant source invalide')
    for key in ['parent_id','texte_parent']:
        if row[key] is not None and not isinstance(row[key],str):raise ValueError('Parent source invalide')
    return {'commentaire':{k:row.get(k) for k in required+['titre_video','chaine','statut_parent']},
            'contexte_documentaire':scope_context(row,tri)}

def instructions():
    files=[BASE/'prompt_v1.md',BASE/'REGLES_PERIMETRE_V1.md',PILOTE/'PROTOCOLE_V1.md',
           PILOTE/'dictionnaire_v1.json',PILOTE/'decisions_et_exemples.md']
    return '\n\n'.join('## '+p.name+'\n'+p.read_text(encoding='utf-8') for p in files)

def candidate_positions(annotation,scope):
    return [p['position_id'] for p in annotation['positions'] if scope['documentaire_candidat']
        and annotation['pertinence_thematique']=='directe'
        and p['position'] in ['favorable','critique','mitigee']
        and p['exploitabilite_positions']=='exploitable'
        and p['incertitude']['cible']!='forte' and p['incertitude']['position']!='forte']

def validate_v1(annotation,row,schema):
    from methodologie.pilote_v1.valider_annotations import check_annotation
    check_annotation(annotation,row,schema)
    for p in annotation['positions']:
        if not p['position_id'].strip() or not p['proposition_evaluee'].strip():
            raise ValueError('Identifiant ou proposition de position vide')
        if p['exploitabilite_positions']=='exploitable' and (
            p['incertitude']['cible']=='forte' or p['incertitude']['position']=='forte'):
            raise ValueError('Forte incertitude incompatible avec une position exploitable')

def append(path,value):
    with path.open('a',encoding='utf-8') as f:
        f.write(json.dumps(value,ensure_ascii=False)+'\n')
        f.flush();os.fsync(f.fileno())

def main():
    from classify_opinions import make_request,response_annotation
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=PILOTE/'commentaires_50.jsonl')
    parser.add_argument('--tri',type=Path,help='tri_50.json ou même format ; sinon seul le lot50 utilise son tri par défaut')
    parser.add_argument('--output',type=Path,help='Dossier neuf dédié, ou reprise de la même configuration')
    parser.add_argument('--model',help='Identifiant exact du modèle à vérifier avant un appel réel')
    parser.add_argument('--reasoning-effort',choices=['low','medium','high'])
    parser.add_argument('--limit',type=int,default=10)
    parser.add_argument('--execute',action='store_true',help='Effectue des appels API facturables')
    args=parser.parse_args()
    if args.limit<=0:parser.error('--limit doit être positif')
    if args.execute and not args.model:parser.error('--model obligatoire avec --execute')
    rows=[json.loads(l) for l in args.input.read_text().splitlines() if l.strip()]
    ids=[r['comment_id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('Identifiants source dupliqués')
    tri_path=args.tri
    if tri_path is None and args.input.resolve()==(PILOTE/'commentaires_50.jsonl').resolve():
        tri_path=PILOTE/'tri_evenement_france/tri_50.json'
    entries=load(tri_path)['commentaires'] if tri_path else []
    tri={r['comment_id']:r for r in entries}
    if len(tri)!=len(entries):raise ValueError('Identifiants dupliqués dans le tri')
    selected=rows[:args.limit]
    prepared=[prepare(r,tri.get(r['comment_id'])) for r in selected]
    schema=load(PILOTE/'schema_annotation_v1.json');prompt=instructions()
    config={'version':'api-v1.0','model':args.model,'reasoning_effort':args.reasoning_effort,
        'schema':schema,'prompt':prompt,'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),
        'tri_sha256':hashlib.sha256(tri_path.read_bytes()).hexdigest() if tri_path else None,
        'selection_comment_ids':[r['comment_id'] for r in selected],
        'donnees_envoyees_sha256':digest(prepared),'max_output_tokens':6000,
        'code_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [BASE/'pipeline.py',ROOT/'classify_opinions.py',PILOTE/'valider_annotations.py']}}
    fingerprint=digest(config)
    output=args.output or BASE/('execution' if args.execute else 'simulation')
    # Un dossier dédié ne doit jamais écraser un fichier existant sans protocole connu.
    output.mkdir(parents=True,exist_ok=True)
    meta=output/'protocole.json'
    if meta.exists():
        old=load(meta)
        if old['fingerprint']!=fingerprint or old['mode']!=('api' if args.execute else 'simulation'):
            raise ValueError('Configuration différente : choisir un autre dossier de sortie')
    elif any(output.iterdir()):raise ValueError('Dossier non vide sans protocole : choisir un nouveau dossier')
    else:
        meta.write_text(json.dumps({'fingerprint':fingerprint,'mode':'api' if args.execute else 'simulation',
            'created_at':datetime.now(timezone.utc).isoformat(),**config},ensure_ascii=False,indent=2)+'\n')
    if not args.execute:
        with (output/'requetes_pretes.jsonl').open('w',encoding='utf-8') as f:
            for data in prepared:
                req=make_request(data,args.model or 'MODELE_A_CHOISIR',prompt,schema,args.reasoning_effort)
                f.write(json.dumps({'comment_id':data['commentaire']['comment_id'],'request':req},ensure_ascii=False)+'\n')
        summary={'mode':'SIMULATION_SANS_APPEL_API','commentaires':len(selected),'lot_disponible':len(rows),
            'structured_outputs':True,'empreinte_protocole':fingerprint,'modele':args.model,
            'annotations_produites':0,'cout_api':0,'sortie':str(output),
            'avertissement':'Requêtes préparées, pas de classification ni mesure de qualité.'}
        (output/'bilan.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(summary,ensure_ascii=False,indent=2));return
    key=os.environ.get('CLASSIFICATION_API_KEY')
    if not key:raise ValueError('Configurer CLASSIFICATION_API_KEY sans l’enregistrer dans Git')
    result_path=output/'annotations.jsonl';journal=output/'tentatives.jsonl'
    records=[json.loads(l) for l in result_path.read_text().splitlines()] if result_path.exists() else []
    done={r['comment_id'] for r in records}
    if len(done)!=len(records):raise ValueError('Résultats dupliqués')
    for rec in records:
        if rec['protocol']!=fingerprint:raise ValueError('Protocole de résultat incompatible')
    attempted={json.loads(l)['comment_id'] for l in journal.read_text().splitlines()} if journal.exists() else set()
    if attempted-done:
        raise ValueError('Tentative sans résultat validé : examiner le journal et la réponse brute avant toute nouvelle facturation; aucune répétition automatique.')
    for row,data in zip(selected,prepared):
        if row['comment_id'] in done:continue
        body=make_request(data,args.model,prompt,schema,args.reasoning_effort)
        request=Request('https://api.openai.com/v1/responses',data=json.dumps(body).encode(),
            headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        append(journal,{'comment_id':row['comment_id'],'request_sha256':digest(body),'started_at':datetime.now(timezone.utc).isoformat()})
        try:
            with urlopen(request,timeout=180) as response:raw=json.load(response)
        except HTTPError as err:raise RuntimeError(f'API HTTP {err.code}; arrêt sans répétition automatique') from None
        except (URLError,OSError):raise RuntimeError('Connexion interrompue : examiner la tentative avant de relancer') from None
        append(output/'reponses_brutes.jsonl',{'comment_id':row['comment_id'],'response':raw})
        annotation=response_annotation(raw);validate_v1(annotation,row,schema)
        append(result_path,{'comment_id':row['comment_id'],'video_id':row['video_id'],'protocol':fingerprint,
            'model_retourne':raw.get('model'),'response_id':raw.get('id'),'usage':raw.get('usage'),
            'contexte_documentaire':data['contexte_documentaire'],'annotation':annotation,
            'positions_candidates_statistiques':candidate_positions(annotation,data['contexte_documentaire']),
            'validation_humaine_independante':False})
        print('Sortie conforme enregistrée (interprétation non validée) :',row['comment_id'],flush=True)

if __name__=='__main__':main()
