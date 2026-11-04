import unittest
from actor_scope import aggregate,project,argument_families
class ActorScopeTests(unittest.TestCase):
    def test_denominator_is_comment_actor_and_mixed_is_not_double_counted(self):
        rows=[{'comment_id':'1','acteur':'Police','position':'condamne'},
              {'comment_id':'1','acteur':'Police','position':'condamne'},
              {'comment_id':'1','acteur':'Police','position':'justifie_soutient'},
              {'comment_id':'2','acteur':'Police','position':'condamne'},
              {'comment_id':'1','acteur':'Manifestants','position':'nuance'}]
        a=aggregate(rows)
        self.assertEqual(a['Police']['denominateur'],2)
        self.assertEqual(a['Police']['effectifs']['mixte'],1)
        self.assertEqual(a['Police']['pourcentages']['condamne'],50)
        for actor in a.values():self.assertAlmostEqual(sum(actor['pourcentages'].values()),100)
        self.assertEqual(a['Manifestants']['denominateur'],1)
    def test_ambiguous_actor_not_forced_into_police(self):
        self.assertEqual(project(76,0)['acteur'],'Acteur non établi')
        self.assertEqual(project(87,0)['acteur'],'Acteur non établi')
        self.assertFalse(project(1,0)['retenue']) # critique de média
        self.assertFalse(project(66,0)['retenue']) # 1961
        self.assertFalse(project(86,0)['retenue']) # Kyiv
        self.assertEqual(project(45,0)['acteur'],'Police') # accusations de policiers casseurs

    def test_argument_family_is_position_specific_and_requires_argument(self):
        self.assertEqual(argument_families(87,0,[]),[])
        self.assertEqual(argument_families(87,0,['antécédent']),['Violences antérieures ou punition invoquées'])
        self.assertEqual(argument_families(87,1,['guerre civile']),['Risque d’escalade'])

if __name__=='__main__':unittest.main()
