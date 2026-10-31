"""Pipeline Structured Outputs. Simulation par défaut; --execute déclenche des appels payants."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE=Path(__file__).resolve().parent/'classification_v02'

def validate(value,schema,path='$'):
    kinds=schema.get('type');kinds=[kinds] if isinstance(kinds,str) else kinds
    def is_kind(kind):
        return {'object':isinstance(value,dict),'array':isinstance(value,list),
                'string':isinstance(value,str),'boolean':isinstance(value,bool),
                'null':value is None}.get(kind,False)
    if not any(is_kind(t) for t in kinds):raise ValueError(f'{path}: type invalide')
    if 'enum' in schema and value not in schema['enum']:raise ValueError(f'{path}: catégorie invalide')
    if isinstance(value,dict):
        if set(value)!=set(schema['required']):raise ValueError(f'{path}: champs manquants ou supplémentaires')
        for key,item in value.items():validate(item,schema['properties'][key],path+'.'+key)
    if isinstance(value,list):
        if len(value)<schema.get('minItems',0):raise ValueError(f'{path}: tableau trop court')
        for i,item in enumerate(value):validate(item,schema['items'],f'{path}[{i}]')

def validate_annotation(annotation,row,schema):
    validate(annotation,schema)
    for pos in annotation['positions']:
        for proof in pos['preuves']:
            if not proof.strip() or proof not in row['texte']:raise ValueError('Citation absente du commentaire')
        passage=pos['passage_parent_vise']
        if passage is not None and (not passage.strip() or passage not in (row['texte_parent'] or '')):
            raise ValueError('Citation absente du parent')
        if not row['parent_id'] and pos['relation_parent']!='sans_parent':
            raise ValueError('Relation attribuée à un parent absent')

def response_annotation(response):
    if response.get('status')!='completed':raise ValueError('Réponse incomplète')
    chunks=[]
    for item in response.get('output',[]):
        for content in item.get('content',[]):
            if content.get('type')=='refusal':raise ValueError('Refus du modèle; aucune annotation validée')
            if content.get('type')=='output_text':chunks.append(content['text'])
    if not chunks:raise ValueError('Aucune sortie structurée')
    return json.loads(''.join(chunks))

def make_request(row,model,prompt,schema,effort=None):
    body={'model':model,'store':False,'instructions':prompt,
          'input':[{'role':'user','content':json.dumps(row,ensure_ascii=False)}],
          'text':{'format':{'type':'json_schema','name':'positions_v02','strict':True,'schema':schema}},
          'max_output_tokens':6000}
    if effort:body['reasoning']={'effort':effort}
    return body

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=BASE/'commentaires_500.jsonl')
    parser.add_argument('--output',type=Path,default=BASE/'execution')
    parser.add_argument('--model',help='Identifiant exact du modèle compatible, à vérifier avant exécution')
    parser.add_argument('--reasoning-effort',choices=['low','medium','high'])
    parser.add_argument('--limit',type=int,default=10)
    parser.add_argument('--execute',action='store_true',help='Effectue de vrais appels API facturables')
    args=parser.parse_args()
    if args.limit<=0:parser.error('--limit doit être positif')
    if args.execute and not args.model:parser.error('--model est obligatoire pour exécuter')
    rows=[json.loads(line) for line in args.input.read_text().splitlines() if line.strip()][:args.limit]
    if len({r['comment_id'] for r in rows})!=len(rows):raise ValueError('Identifiants dupliqués')
    schema=json.loads((BASE/'schema.json').read_text());prompt=(BASE/'grille_et_prompt_v02.md').read_text()
    config={'model':args.model,'reasoning_effort':args.reasoning_effort,'schema':schema,'prompt':prompt,
            'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest()}
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    # Aucune clé ni requête réseau en simulation.
    if not args.execute:
        print(json.dumps({'mode':'SIMULATION_SANS_APPEL_API','commentaires':len(rows),
            'lot_disponible':len(args.input.read_text().splitlines()),'model':args.model,
            'empreinte_protocole':fingerprint,'structured_outputs':True,
            'cout':'Non estimé : modèle, tarification et tokens réels à vérifier avant exécution.'},ensure_ascii=False,indent=2))
        return
    key=os.environ.get('CLASSIFICATION_API_KEY')
    if not key:raise ValueError('Configurer CLASSIFICATION_API_KEY de manière sécurisée; ne pas la mettre dans Git')
    args.output.mkdir(parents=True,exist_ok=True)
    meta=args.output/'protocole.json'
    if meta.exists() and json.loads(meta.read_text())['fingerprint']!=fingerprint:
        raise ValueError('Protocole différent : choisir un autre dossier de sortie')
    meta.write_text(json.dumps({'fingerprint':fingerprint,**config},ensure_ascii=False,indent=2))
    result_path=args.output/'annotations.jsonl';done=set()
    if result_path.exists():
        for line in result_path.read_text().splitlines():
            record=json.loads(line);done.add(record['comment_id'])
    for row in rows:
        if row['comment_id'] in done:continue
        body=make_request(row,args.model,prompt,schema,args.reasoning_effort)
        request=Request('https://api.openai.com/v1/responses',
            data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        try:
            with urlopen(request,timeout=180) as r:response=json.load(r)
        except HTTPError as e:raise RuntimeError(f'API HTTP {e.code}; arrêt sans répétition automatique') from None
        except (URLError,OSError):raise RuntimeError('Connexion API interrompue; vérifier avant de relancer pour éviter un doublon facturable') from None
        # Conserver la réponse reçue avant validation pour pouvoir diagnostiquer une erreur.
        with (args.output/'reponses_brutes.jsonl').open('a') as f:
            f.write(json.dumps({'comment_id':row['comment_id'],'response':response},ensure_ascii=False)+'\n')
        annotation=response_annotation(response);validate_annotation(annotation,row,schema)
        record={'comment_id':row['comment_id'],'video_id':row['video_id'],'protocol':fingerprint,
                'response_id':response.get('id'),'model_retourne':response.get('model'),
                'usage':response.get('usage'),'annotation':annotation}
        with result_path.open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
        print('Annotation validée :',row['comment_id'],flush=True)

if __name__=='__main__':main()
