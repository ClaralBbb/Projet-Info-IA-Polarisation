"""Pipeline Structured Outputs. Simulation par défaut; --execute déclenche des appels payants."""
import json

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
    if 'version_protocole' in schema.get('properties',{}):
        from classification_v1.pipeline import validate_v1
        return validate_v1(annotation,row,schema)
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
          'text':{'format':{'type':'json_schema','name':('positions_v1' if 'version_protocole' in schema.get('properties',{}) else 'positions_v02'),'strict':True,'schema':schema}},
          'max_output_tokens':6000}
    if effort:body['reasoning']={'effort':effort}
    return body

def main():
    from classification_v1.pipeline import main as run_v1
    run_v1()

if __name__=='__main__':main()
