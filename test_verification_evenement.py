import copy
import unittest
from verification_evenement.controle import precontrole,attach,validate_review

class VerificationTests(unittest.TestCase):
    def video(self,title,description='',published='2026-10-17T10:00:00Z'):
        return {'id':'video','snippet':{'title':title,'description':description,'publishedAt':published}}
    def test_publication_ne_confirme_pas_evenement(self):
        result=precontrole(self.video('Voitures brûlées à Paris'))
        self.assertEqual(result['statut'],'a_verifier')
        self.assertFalse(result['images_authentifiees'])
        self.assertEqual(result['preuves_examinees'],[])
    def test_histoire_contradiction_et_suites(self):
        for title,description,flag in [
            ('Paris 17 octobre 1961','','reference_1961_a_distinguer'),
            ('Mobilisation du 7 octobre','Le 17 octobre à Limoges','contradiction_7_17_octobre'),
            ('Rassemblement du 24 octobre','','autre_date_ou_suite_a_examiner')]:
            result=precontrole(self.video(title,description))
            self.assertIn(flag,result['signalements_automatiques'])
            self.assertEqual(result['statut'],'a_verifier')
    def test_etaye_exige_preuve_responsable_date_lieu(self):
        review=precontrole(self.video('Paris le 17 octobre 2026'))
        review.update(statut='rattachement_etaye',responsable_controle='Test fictif',date_controle='2026-11-22T12:00:00Z',
            motif='Exemple de test, ne constitue pas une vérification réelle.',
            preuves_examinees=[{'type':'source_concordante','url':'https://example.org/test','passage':'Extrait fictif',
                'etaye_date_evenement':True,'etaye_lieu_france':True}])
        validate_review(review)
        scope={'documentaire_candidat':True}
        self.assertTrue(attach(scope,review,'video')['documentaire_candidat'])
        self.assertFalse(attach({'documentaire_candidat':False},review,'video')['documentaire_candidat'])
        for field,value in [('preuves_examinees',[]),('responsable_controle',None),('images_authentifiees',True)]:
            bad=copy.deepcopy(review);bad[field]=value
            with self.assertRaises(ValueError):validate_review(bad)
        self.assertFalse(attach(scope,None,'video')['documentaire_candidat'])
        review['statut']='lien_plausible'
        self.assertFalse(attach(scope,review,'video')['documentaire_candidat'])
        with self.assertRaises(ValueError):attach(scope,review,'other')

if __name__=='__main__':unittest.main()
