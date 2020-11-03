import unittest
import numpy as np
from text_functions import word_freq, summary, file_statistics

class TextTest(unittest.TestCase):

    def test_word_freq(self):
        self.assertEqual(word_freq('holmes.txt')['the'], 10)
        self.assertEqual(word_freq('holmes.txt', True)['the'], 9)
        self.assertEqual(word_freq('holmes.txt')['abhorrent'], 1)

    def test_summary(self):
        s,a,d = summary("lukuja.txt")
        self.assertAlmostEqual(s, 61.3)
        self.assertAlmostEqual(a, 10.216666666666667)
        self.assertAlmostEqual(d, 8.91480042775309)
        self.assertRaises(Exception, summary, 'holmes.txt')

    def test_file_statistics(self):
        lines, words, chars = file_statistics('holmes.txt')
        self.assertEqual(lines, 25)
        self.assertEqual(words, 221)
        self.assertEqual(chars, 1234)
        

if __name__ == '__main__':
    unittest.main()