import csv
import tempfile
import unittest
from pathlib import Path
from analyze import analyze, tokens, phrases, redact, csv_write, HTML

class AnalysisTests(unittest.TestCase):
    def test_presence_deduplication_and_reply_views(self):
        videos=[{'video_id':'v','title':'test'}]
        rows=[{'comment_id':'1','video_id':'v','text':'Police police violence !','parent_id':''},
              {'comment_id':'2','video_id':'v','text':'POLICE police violence !','parent_id':'1'},
              {'comment_id':'3','video_id':'v','text':'😀','parent_id':''}]
        result=analyze(videos,rows)
        self.assertEqual(result['profiles']['tous']['n'],2)
        self.assertEqual(dict(result['profiles']['tous']['words'])['police'],2)
        self.assertEqual(result['profiles']['uniques']['n'],1)
        self.assertEqual(result['profiles']['principaux']['n'],1)
        self.assertEqual(result['profiles']['reponses']['n'],1)
        self.assertEqual(result['quality']['sans_mot_analyse'],1)
        self.assertEqual(result['quality']['doublons_textuels'],1)

    def test_phrases_do_not_bridge_stopwords_or_sentences(self):
        self.assertNotIn('police violence',phrases('Police et violence'))
        self.assertNotIn('police violence',phrases('Police. Violence'))
        self.assertNotIn('police violence',phrases('Police 123 violence'))
        self.assertNotIn('police violence',phrases('Police https://example.org violence'))
        self.assertIn('violence policiere',phrases('violence policière'))
        self.assertNotIn('https',tokens('https://example.com police'))

    def test_reproducible_sample_and_redaction(self):
        videos=[{'video_id':str(i),'title':'test'} for i in range(450)]
        rows=[{'comment_id':str(i),'video_id':str(i),'text':'police mobilisation','parent_id':''} for i in range(450)]
        a=analyze(videos,rows)['sample']; b=analyze(videos,rows)['sample']
        self.assertEqual(a,b)
        self.assertEqual(len(a),400)
        self.assertEqual(len({x['video_id'] for x in a}),400)
        text=redact('Contact abc@example.org ou @personne : https://example.com')
        self.assertNotIn('abc@example.org',text)
        self.assertNotIn('@personne',text)

    def test_line_endings_have_identical_results(self):
        videos=[{'video_id':'v','title':'test'}]
        a=[{'comment_id':'1','video_id':'v','text':'police\r\nviolence','parent_id':''}]
        b=[dict(a[0], text='police\nviolence')]
        left=analyze(videos,a); right=analyze(videos,b)
        for field in ['profiles','sample','quality']:
            self.assertEqual(left[field],right[field])

    def test_csv_formula_escaping(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'data.csv'
            csv_write(path,['text'],[['=1+1'],['normal']])
            with path.open(encoding='utf-8-sig',newline='') as handle:
                rows=list(csv.reader(handle))
            self.assertEqual(rows[1][0],"'=1+1")
            self.assertEqual(rows[2][0],'normal')
        self.assertIn('esc(r.text)',HTML)

if __name__=='__main__': unittest.main()
