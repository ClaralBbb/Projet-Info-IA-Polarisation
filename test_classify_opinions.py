import copy,json,unittest
from pathlib import Path
from classify_opinions import validate_annotation,make_request,response_annotation

class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.schema=json.loads(Path('classification_v02/schema.json').read_text())
        self.row={'texte':'La police frappe trop fort.','texte_parent':None,'parent_id':None}
        fields=self.schema['properties']['positions']['items']['properties']
        p={k: (v['enum'][0] if 'enum' in v else '' if v['type']=='string' else False if v['type']=='boolean' else [] if v['type']=='array' else None) for k,v in fields.items()}
        p.update(preuves=['frappe trop fort'],relation_parent='sans_parent')
        self.good={'pertinence':'intervention_policiere','contexte_parent_utilise':'non','positions':[p],'limites':[]}
    def test_strict_schema_and_evidence(self):
        validate_annotation(self.good,self.row,self.schema)
        for field,value in [('position','pour_la_police'),('preuves',['citation inventée']),('relation_parent','accord')]:
            bad=copy.deepcopy(self.good);bad['positions'][0][field]=value
            with self.assertRaises(ValueError):validate_annotation(bad,self.row,self.schema)
        bad=copy.deepcopy(self.good);bad['champ_invente']=1
        with self.assertRaises(ValueError):validate_annotation(bad,self.row,self.schema)
    def test_structured_request_and_optional_reasoning(self):
        body=make_request(self.row,'modele-a-tester','consigne',self.schema,'medium')
        self.assertTrue(body['text']['format']['strict'])
        self.assertEqual(body['text']['format']['type'],'json_schema')
        self.assertEqual(body['reasoning']['effort'],'medium')
        self.assertFalse(body['store'])
    def test_refusal_and_incomplete_are_not_annotations(self):
        for response in [{'status':'incomplete'},{'status':'completed','output':[{'content':[{'type':'refusal'}]}]}]:
            with self.assertRaises(ValueError):response_annotation(response)
        response={'status':'completed','output':[{'content':[{'type':'output_text','text':json.dumps(self.good)}]}]}
        self.assertEqual(response_annotation(response),self.good)

if __name__=='__main__':unittest.main()
