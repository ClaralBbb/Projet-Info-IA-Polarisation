import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from classify_opinions import main,make_request,validate_annotation
from classification_v1.pipeline import prepare,scope_context,candidate_positions,instructions,validate_v1

B=Path('methodologie/pilote_v1')
class PipelineV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=[json.loads(l) for l in (B/'commentaires_50.jsonl').read_text().splitlines()]
        cls.annotations=json.loads((B/'annotations_50_proposees.json').read_text())
        cls.schema=json.loads((B/'schema_annotation_v1.json').read_text())
        cls.tri=json.loads((B/'tri_evenement_france/tri_50.json').read_text())['commentaires']

    def run_cli(self,args):
        with patch.object(sys,'argv',['classify_opinions.py',*args]),redirect_stdout(io.StringIO()):main()

    def test_dry_run_offline_exact_sources_no_predictions(self):
        with tempfile.TemporaryDirectory() as folder,patch('classification_v1.pipeline.urlopen') as network:
            self.run_cli(['--output',folder,'--limit','50'])
            network.assert_not_called()
            requests=[json.loads(l) for l in (Path(folder)/'requetes_pretes.jsonl').read_text().splitlines()]
            self.assertEqual(len(requests),50)
            for row,record in zip(self.rows,requests):
                body=record['request'];data=json.loads(body['input'][0]['content'])
                self.assertEqual(data['commentaire']['texte'],row['texte'])
                self.assertEqual(data['commentaire']['texte_parent'],row['texte_parent'])
                self.assertNotIn('positions',data['commentaire'])
                self.assertNotIn('annotation',data)
                self.assertEqual(body['text']['format']['name'],'positions_v1')
                self.assertTrue(body['text']['format']['strict'])
                self.assertEqual(body['text']['format']['schema'],self.schema)
            self.assertFalse((Path(folder)/'annotations.jsonl').exists())
            self.assertEqual(json.loads((Path(folder)/'bilan.json').read_text())['annotations_produites'],0)
            self.run_cli(['--output',folder,'--limit','50'])
            with self.assertRaises(ValueError):self.run_cli(['--output',folder,'--limit','1'])

    def test_unknown_event_suites_and_disputed_claims_not_main_candidates(self):
        for number in [1,6,11,15,23,25,26,28,32,35,37]:
            self.assertFalse(scope_context(self.rows[number-1],self.tri[number-1])['documentaire_candidat'])
        self.assertTrue(scope_context(self.rows[1],self.tri[1])['documentaire_candidat'])
        self.assertEqual(scope_context(self.rows[22],self.tri[22])['traitement'],'suites_separees')
        self.assertFalse(scope_context(self.rows[1],None)['documentaire_candidat'])
        bad=copy.deepcopy(self.tri[1]);bad['video_id']='wrong'
        with self.assertRaises(ValueError):prepare(self.rows[1],bad)

    def test_v1_semantics_quotes_and_uncertainty(self):
        row=self.rows[3];good=copy.deepcopy(self.annotations[3])
        validate_annotation(good,row,self.schema)
        for change in ['id','proof','argument','uncertainty','event']:
            bad=copy.deepcopy(good)
            if change=='id':bad['comment_id']='other'
            if change=='proof':bad['positions'][0]['preuves_position']=['Citation fabriquée']
            if change=='argument':bad['positions'][0]['argumentation']['statut']='absente'
            if change=='uncertainty':
                bad['positions'][0]['incertitude']['position']='forte'
                bad['positions'][0]['exploitabilite_positions']='exploitable'
            if change=='event':bad['lien_evenement']['statut']='confirme'
            with self.assertRaises(ValueError):validate_v1(bad,row,self.schema)
        self.assertEqual(candidate_positions(good,{'documentaire_candidat':False}),[])

    def test_live_path_mocked_resume_and_raw_before_validation(self):
        # Le seul modèle employé ici est une réponse de test en mémoire.
        raw={'status':'completed','id':'mock_response','model':'mock_model','usage':{'input_tokens':1},
            'output':[{'content':[{'type':'output_text','text':json.dumps(self.annotations[0])}]}]}
        with tempfile.TemporaryDirectory() as folder,patch.dict('os.environ',{'CLASSIFICATION_API_KEY':'TEST_ONLY'}),patch('classification_v1.pipeline.urlopen') as network:
            network.return_value.__enter__.return_value=io.StringIO(json.dumps(raw))
            args=['--output',folder,'--limit','1','--model','mock_model','--execute']
            self.run_cli(args);self.assertEqual(network.call_count,1)
            self.run_cli(args);self.assertEqual(network.call_count,1)
            result=json.loads((Path(folder)/'annotations.jsonl').read_text())
            self.assertFalse(result['validation_humaine_independante'])
            self.assertEqual(result['model_retourne'],'mock_model')
            self.assertEqual(result['positions_candidates_statistiques'],[])
            self.assertNotIn('TEST_ONLY',''.join(p.read_text() for p in Path(folder).iterdir()))
        for raw in [{'status':'incomplete'},{'status':'completed','output':[{'content':[{'type':'refusal'}]}]},
                    {'status':'completed','output':[{'content':[{'type':'output_text','text':'{}'}]}]}]:
            with tempfile.TemporaryDirectory() as folder,patch.dict('os.environ',{'CLASSIFICATION_API_KEY':'TEST_ONLY'}),patch('classification_v1.pipeline.urlopen') as network:
                network.return_value.__enter__.return_value=io.StringIO(json.dumps(raw))
                args=['--output',folder,'--limit','1','--model','mock_model','--execute']
                with self.assertRaises((ValueError,KeyError)):self.run_cli(args)
                self.assertTrue((Path(folder)/'reponses_brutes.jsonl').exists())
                self.assertFalse((Path(folder)/'annotations.jsonl').exists())
                with self.assertRaises(ValueError):self.run_cli(args)
                self.assertEqual(network.call_count,1)

    def test_new_input_has_no_automatic_old_tri_join(self):
        with tempfile.TemporaryDirectory() as folder,patch('classification_v1.pipeline.urlopen') as network:
            source=Path(folder)/'new.jsonl';source.write_text(json.dumps(self.rows[1])+'\n')
            output=Path(folder)/'output'
            self.run_cli(['--input',str(source),'--output',str(output)])
            data=json.loads(json.loads((output/'requetes_pretes.jsonl').read_text())['request']['input'][0]['content'])
            self.assertFalse(data['contexte_documentaire']['documentaire_candidat'])
            network.assert_not_called()

if __name__=='__main__':unittest.main()
