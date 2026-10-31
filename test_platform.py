import hashlib,json,re,unittest
from pathlib import Path
from classify_opinions import validate_annotation

class PlatformTests(unittest.TestCase):
    def test_all_recorded_annotations_have_valid_sources_and_evidence(self):
        root=Path('classification_v02')
        rows=[json.loads(line) for line in (root/'commentaires_500.jsonl').read_text().splitlines()]
        records=json.loads(Path('plateforme/annotations_60.json').read_text())
        protocol=json.loads(Path('plateforme/protocole.json').read_text())
        schema=json.loads((root/'schema.json').read_text())
        self.assertEqual([r['comment_id'] for r in records],[r['comment_id'] for r in rows[:60]])
        self.assertEqual(protocol['n_classes'],len(records))
        self.assertEqual(protocol['positions'],sum(len(r['annotation']['positions']) for r in records))
        self.assertEqual(protocol['source_sha256'],hashlib.sha256((root/'commentaires_500.jsonl').read_bytes()).hexdigest())
        for record,row in zip(records,rows):
            validate_annotation(record['annotation'],row,schema)
            self.assertEqual(record['validation_humaine'],'non_effectuee')
            self.assertIsNone(record['modele_api'])
    def test_pending_comments_have_no_invented_annotations(self):
        text=Path('docs/index.html').read_text()
        payload=re.search(r'<script id="data" type="application/json">(.*?)</script>',text,re.S).group(1)
        self.assertNotIn('<',payload)
        data=json.loads(payload)
        self.assertEqual(len(data['rows']),500)
        self.assertEqual(sum(row['result'] is not None for row in data['rows']),60)
        self.assertTrue(all(row['result'] is None for row in data['rows'][60:]))
        self.assertEqual(text,Path('plateforme/tableau_de_bord.html').read_text())

if __name__=='__main__':unittest.main()
