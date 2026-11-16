import copy,hashlib,json,unittest
from pathlib import Path
from methodologie.pilote_v1.valider_annotations import check_annotation
B=Path('methodologie/pilote_v1')
class ProtocoleV1Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rows=[json.loads(l) for l in (B/'commentaires_50.jsonl').read_text().splitlines()]
  cls.annotations=json.loads((B/'annotations_50_proposees.json').read_text())
  cls.schema=json.loads((B/'schema_annotation_v1.json').read_text())
 def test_all_50_complete_and_source_distinct_by_video(self):
  self.assertEqual(len(self.rows),50);self.assertEqual(len(self.annotations),50)
  self.assertEqual(len({r['video_id'] for r in self.rows}),50)
  manifest=json.loads((B/'selection.json').read_text())
  self.assertFalse({r['video_id'] for r in self.rows}&set(manifest['excluded_videos']))
  self.assertFalse({r['comment_id'] for r in self.rows}&set(manifest['excluded_ids']))
  self.assertEqual(sum(bool(r['parent_id']) for r in self.rows),25)
  for a,row in zip(self.annotations,self.rows):check_annotation(a,row,self.schema)
 def test_reject_unknown_fields_bad_quote_and_invalid_argument(self):
  original=self.annotations[3];row=self.rows[3]
  bad=copy.deepcopy(original);bad['score_polarisation']=8
  with self.assertRaises(ValueError):check_annotation(bad,row,self.schema)
  bad=copy.deepcopy(original);bad['positions'][0]['preuves_position']=['Citation inventée']
  with self.assertRaises(ValueError):check_annotation(bad,row,self.schema)
  bad=copy.deepcopy(original);bad['positions'][0]['argumentation']['statut']='absente'
  with self.assertRaises(ValueError):check_annotation(bad,row,self.schema)
 def test_no_forced_signed_position_and_protocol_fingerprints(self):
  bad=copy.deepcopy(self.annotations[2]);bad['positions'][0]['exploitabilite_positions']='exploitable'
  with self.assertRaises(ValueError):check_annotation(bad,self.rows[2],self.schema)
  meta=json.loads((B/'execution_conversationnelle.json').read_text())
  for key,path in [('source_sha256','commentaires_50.jsonl'),('protocole_sha256','PROTOCOLE_V1.md'),('dictionnaire_sha256','dictionnaire_v1.json'),('schema_sha256','schema_annotation_v1.json'),('annotations_sha256','annotations_50_proposees.json')]:
   self.assertEqual(meta[key],hashlib.sha256((B/path).read_bytes()).hexdigest())

if __name__=='__main__':unittest.main()
