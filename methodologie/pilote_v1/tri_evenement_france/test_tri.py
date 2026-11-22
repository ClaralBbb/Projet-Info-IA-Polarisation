import json
import unittest
from pathlib import Path
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parent

class TriTest(unittest.TestCase):
    def test_sources_et_preuves(self):
        source={r['comment_id']:r for r in map(json.loads,(ROOT.parent/'commentaires_50.jsonl').read_text().splitlines())}
        rows=json.loads((ROOT/'tri_50.json').read_text())['commentaires']
        self.assertEqual(len(rows),50)
        self.assertEqual(set(source),{r['comment_id'] for r in rows})
        for r in rows:
            self.assertEqual(r['texte'],source[r['comment_id']]['texte'])
            self.assertEqual(r['texte_parent'],source[r['comment_id']]['texte_parent'])
            ev=r['preuve_commentaire_ou_parent']
            self.assertIn(ev['extrait'],r['texte' if ev['source']=='commentaire' else 'texte_parent'])
            self.assertFalse(r['images_verifiees'])
            self.assertFalse(r['date_des_faits_confirmee'])
    def test_distinction_video_commentaire(self):
        rows={r['repere']:r for r in json.loads((ROOT/'tri_50.json').read_text())['commentaires']}
        self.assertEqual(rows['N001']['statut_video'],'lien_plausible_non_confirme')
        self.assertEqual(rows['N001']['statut_commentaire'],'autre_evenement_explicite')
        self.assertEqual(rows['N011']['statut_video'],'autre_evenement_explicite')
        self.assertEqual(rows['N018']['statut_video'],'lien_plausible_non_confirme')
        self.assertEqual(rows['N023']['statut_video'],'suite_ou_autre_date_liee')
        self.assertEqual(rows['N026']['statut_video'],'date_contradictoire_a_verifier')
        self.assertEqual(rows['N028']['statut_video'],'informations_insuffisantes')
        self.assertTrue(rows['N006']['signalements'])
    def test_excel_textes_complets_sans_formules(self):
        rows=json.loads((ROOT/'tri_50.json').read_text())['commentaires']
        ws=load_workbook(ROOT/'TRI_50_FRANCE.xlsx').worksheets[0]
        self.assertEqual(ws.max_row,51)
        for i,r in enumerate(rows,2):
            self.assertEqual(ws.cell(i,2).value,r['texte'])
            self.assertEqual(ws.cell(i,3).value or '',r['texte_parent'] or '')
        self.assertFalse(any(c.data_type=='f' for row in ws for c in row))

if __name__=='__main__':unittest.main()
