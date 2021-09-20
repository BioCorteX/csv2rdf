from unittest import TestCase
from csv2rdf.normalize_naming import normalize_name


class Test(TestCase):
    def test_normalize_name(self):
        self.normalize_name('Hi There', 'Hi_there', 'Hi_there')
        self.normalize_name('Hi-There', 'Hi_there', 'Hi_there')
        self.normalize_name('Hi_There', 'Hi_there', 'Hi_there')

    def normalize_name(self, original, output, output2):
        output_ = normalize_name(original)
        self.assertEqual(output, output_)

        output_ = normalize_name(original, first_character=True)
        self.assertEqual(output2, output_)
