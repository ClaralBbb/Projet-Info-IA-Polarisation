import unittest
from collections import Counter
from prepare_annotation import select

class SelectionTests(unittest.TestCase):
    def test_balanced_reproducible_diverse_selection(self):
        rows=[]
        for video in range(70):
            for reply in [False,True]:
                for i in range(3):
                    rows.append({'comment_id':f'{video}-{reply}-{i}','video_id':str(video),
                        'parent_id':'parent' if reply else '',
                        'text':f'police violence {video} {reply} {i}'})
        a=select(rows)
        self.assertEqual(a,select(rows))
        self.assertEqual(len(a),100)
        self.assertEqual(sum(bool(c['parent_id']) for c in a),50)
        self.assertEqual(len({c['comment_id'] for c in a}),100)
        self.assertLessEqual(max(Counter(c['video_id'] for c in a).values()),2)

    def test_insufficient_candidates_explicit_failure(self):
        with self.assertRaises(ValueError):
            select([{'comment_id':'1','video_id':'v','parent_id':'','text':'bonjour'}])

if __name__=='__main__':unittest.main()
