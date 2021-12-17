import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_jan_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_01_2018.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-01-2018.ods',
                 'src/output_test/sheets/membros-verbas-indenizatorias-01-2018.ods']

        dados = load(files, '2018', '01', 'src/output_test/sheets')
        result_data = parse(dados, 'mpto/1/2018', '01', '2018')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)

    def test_aug_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_08_2018.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-08-2018.ods',
                 'src/output_test/sheets/membros-verbas-indenizatorias-08-2018.ods']

        dados = load(files, '2018', '08', 'src/output_test/sheets')
        result_data = parse(dados, 'mpto/8/2018', '08', '2018')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)

    def test_apr_2019(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_04_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-04-2019.ods',
                 'src/output_test/sheets/membros-verbas-indenizatorias-04-2019.ods']

        dados = load(files, '2019', '04', 'src/output_test/sheets')
        result_data = parse(dados, 'mpto/4/2019', '04', '2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)

    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_01_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-01-2020.ods',
                 'src/output_test/sheets/membros-verbas-indenizatorias-01-2020.ods']

        dados = load(files, '2020', '01', 'src/output_test/sheets')
        result_data = parse(dados, 'mpto/1/2020', '01', '2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)

    def test_jan_2021(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_01_2021.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-01-2021.ods',
                 'src/output_test/sheets/membros-verbas-indenizatorias-01-2021.ods']

        dados = load(files, '2021', '01', 'src/output_test/sheets')
        result_data = parse(dados, 'mpto/1/2021', '01', '2021')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)


if __name__ == '__main__':
    unittest.main()