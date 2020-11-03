import unittest
import pandas as pd
# pandas-dataframen testaus ongelma, self.assertEqual ei suoraan toimi;
# käytän pandasin omaa testiä pdt.assert_frame_equal
import pandas.util.testing as pdt

from ravinteiden_saanti import filter_food_class, transpose_component_value

class NutrientTest(unittest.TestCase):

    def test_filter_food_class(self):
        original_data = {'FOODNAME': ['SOKERI', 'SUKLAA, TUMMA', 'KURKKU',
        'NAUDANLIHA-KASVISSOSE, TEOLLINEN LASTENRUOKA, TUOTEKESKIARVO',
        'ATERIANKORVIKE, SHAKE, VALMISJUOMA, NATURDIET', 'POROKEITTO'], 
        'IGCLASS': ['SUGARSYR', 'CHOCOLAT', 'VEGFRU', 'DISH', 'MEALREP', 'DISH'], 
        'FUCLASS': ['SUGADD', 'CHOCOL', 'VEGFRESH', 'BABMEATD', 'MEALREP', 'MEATSOUP']}
        original_df = pd.DataFrame(original_data, index=[1, 32, 346, 11472, 32619, 33479])

        filtered_data1 = {'FOODNAME': ['SOKERI', 'SUKLAA, TUMMA', 'KURKKU',
        'POROKEITTO'], 
        'IGCLASS': ['SUGARSYR', 'CHOCOLAT', 'VEGFRU', 'DISH'], 
        'FUCLASS': ['SUGADD', 'CHOCOL', 'VEGFRESH', 'MEATSOUP']}
        filtered_df1 = pd.DataFrame(filtered_data1, index=[1, 32, 346, 33479])

        filtered_data2 = {'FOODNAME': ['KURKKU',
        'NAUDANLIHA-KASVISSOSE, TEOLLINEN LASTENRUOKA, TUOTEKESKIARVO',
        'ATERIANKORVIKE, SHAKE, VALMISJUOMA, NATURDIET', 'POROKEITTO'], 
        'IGCLASS': ['VEGFRU', 'DISH', 'MEALREP', 'DISH'], 
        'FUCLASS': ['VEGFRESH', 'BABMEATD', 'MEALREP', 'MEATSOUP']}
        filtered_df2 = pd.DataFrame(filtered_data2, index=[346, 11472, 32619, 33479])

        pdt.assert_frame_equal(filter_food_class(original_df, []), original_df)
        pdt.assert_frame_equal(filter_food_class(original_df, ['BABMEATD', 'MEALREP'], 'FUCLASS'), filtered_df1)
        pdt.assert_frame_equal(filter_food_class(original_df, ['BABMEATD', 'MEALREP']), filtered_df1)
        pdt.assert_frame_equal(filter_food_class(original_df, ['SUGARSYR', 'CHOCOLAT'], 'IGCLASS'), filtered_df2)
        self.assertRaises(ValueError, filter_food_class, original_df, ["BABMEATD"], 'EUFDNAME')

    def test_transpose_component_value(self):
        original_data = {'FOODID': [1,1,1,1, 2, 2, 2, 2], 
        'EUFDNAME': ['ENERC', 'FAT', 'CHOAVL', 'CHOCDF', 'ENERC', 'FAT', 'CHOAVL', 'CHOCDF'], 
        'BESTLOC': [1698.30, None, 99.90, 99.88, 1590.0, 1.6, None, 99.0],
        'ACQTYPE': ['S', 'F', 'S', 'S', 'S', 'F', 'S', 'S'], 
        'METHTYPE': ['S', 'E', 'S', 'S', 'S', 'E', 'S', 'S'],
        'METHIND': ['MI0107', 'MI0107', 'MI0107', 'MI0107', 'MI0107', 'MI0107', 'MI0107', 'MI0107']}
        original_df = pd.DataFrame(original_data)
        #print(f'original df:', original_df, sep='\n')

        transposed_data = {'FOODID': [1, 2],
        'CHOAVL': [99.90, 0], 'CHOCDF': [99.88, 99.0], 'ENERC': [1698.30, 1590.0],
        'FAT': [0.0, 1.6]}
        transposed_df = pd.DataFrame(transposed_data)
        print(f'transposed df:', transposed_df, sep='\n')
        transposed_df.set_index('FOODID', inplace=True)
        #print(f'transposed df:', transposed_df, sep='\n')

        #print('returned: ', transpose_component_value(original_df), sep='\n')

        pdt.assert_frame_equal(transpose_component_value(original_df), transposed_df, check_names=False)


if __name__ == '__main__':
    unittest.main()