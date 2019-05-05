#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 11:26:37 2019

"""

import unittest
#from lyricsfunc import *
#from load import *
from main import *


names_test = ["271~E-40~Neva-Broke.txt", "081~V-Ice~I-Know.txt",
              "008~Sarah-Harmer~Almost.txt", "272~E-40~Neva-Broke.txt",
              "011~Sarah-Harmer~Almost.txt"]
buffer_test = {
        "271~E-40~Neva-Broke.txt":
        ["Rockies value, happy-nice value\r\n", "you're, street\r\n"],
        "081~V-Ice~I-Know.txt":
        ['hello honey, bowl baby\r\n', 'honey meet\r\n']
}

lyrics_test = {
        "271~E-40~Neva-Broke.txt":
        ['rockies', 'value', 'happy', 'nice', 'value', "you're", 'street'],
        "081~V-Ice~I-Know.txt":
        ['hello', 'honey', 'bowl', 'baby', 'honey', 'meet'],
        "008~Sarah-Harmer~Almost.txt":
        ['fresh', 'swim', 'vegetables', 'fresh', 'cry', 'cry', 'wallet'],
        "272~E-40~Neva-Broke.txt":
        ['rockies', 'value*', 'happy', 'nice', 'value', 'you', 'street'],
        "011~Sarah-Harmer~Almost.txt":
        ['y', 'así', 'hablamos', 'solas', 'aquella', 'linda', 'mañana']
            }

detail_test = {
                "271~E-40~Neva-Broke.txt":
                ['271', 'E 40', 'Neva Broke', True],
                "081~V-Ice~I-Know.txt":
                ['081', 'V Ice', 'I Know', True],
                "008~Sarah-Harmer~Almost.txt":
                ['008', 'Sarah Harmer', 'Almost', True],
                "272~E-40~Neva-Broke.txt":
                ['272', 'E 40', 'Neva Broke', True],
                "011~Sarah-Harmer~Almost.txt":
                ['011', 'Sarah Harmer', 'Almost', False]
              }
love_test = ['honey', 'love', 'happy']
dirty_test = ['blood', 'fuck']
langset1 = ["i'm", 'watching', 'tv', 'a', 'saturday', 'night', 'what',
            'desire', 'see', 'but', 'a', 'middleweight', 'boxing', 'fight']
langset2 = ['en', 'el', 'balcón', 'de', 'la', 'escuela', 'nos', 'quedamos',
            'por', 'un', 'rato', 'y', 'así', 'hablamos', 'solas', 'aquella',
            'linda', 'mañana', 'le', 'dije', 'que']
langset3 = ['instrumental']

comptest = lyricsfunc.complexity(names_test, lyrics_test)
senttest = lyricsfunc.sentiment(names_test, lyrics_test)
lovetest = lyricsfunc.love(names_test, love_test, lyrics_test)
lengthtest = lyricsfunc.length(names_test, lyrics_test)
kidsafe_test = lyricsfunc.kid_safe(
    names_test, dirty_test, senttest, lyrics_test)
a, b, c, d, e = lyricsfunc.result_rank(
    senttest, lovetest, kidsafe_test, lengthtest, comptest, detail_test, 1)
findic_test = lyricsfunc.get_finaldic(a, b, c, d, e, detail_test, names_test)
details = load.get_details(names_test, lyrics_test)

class TestStringMethods(unittest.TestCase):
    
    def test_path_1(self):
        with self.assertRaises(FileNotFoundError):
            load.read_path('notvalidpath')

    def test_lyrics_1(self):
        songname, songlyrics = load.read_lyrics(buffer_test)
        self.assertEqual(songname[1], names_test[1])
        self.assertEqual(songlyrics[songname[1]], lyrics_test[songname[1]])

    def test_lang(self):
        self.assertTrue(load.detect_lang(langset1))
        self.assertFalse(load.detect_lang(langset2))
        self.assertTrue(load.detect_lang(langset3))   

    def test_details1(self):
        self.assertEqual(details["271~E-40~Neva-Broke.txt"],
                         detail_test["271~E-40~Neva-Broke.txt"])

    def test_details2(self):
        with self.assertRaises(AttributeError):
            load.get_details([1, 2], {1: ['a', 'b'], 2: ['c', 'd', 'd']})

    def test_details3(self):
        self.assertIsInstance(details, dict)
        
#    def test_readtxt(self):
#        self.assertIsInstance(read_txt("love_words.txt"), list)
        
    def test_get_word(self):
        positive_words = lyricsfunc.get_words('http://ptrckprry.com/course/ssd/data/positive-words.txt')
        negative_words = lyricsfunc.get_words('http://ptrckprry.com/course/ssd/data/negative-words.txt')
        self.assertTrue('admire' in positive_words)
        self.assertFalse('admire' in negative_words)

    def test_get_pos_neg_words(self):
        positive_words, negative_words = lyricsfunc.get_pos_neg_words()
        self.assertTrue('admire' in positive_words)
        self.assertFalse('admire' in negative_words)

    def test_mood_valid(self):
        self.assertEqual(senttest[names_test[1]], 0.0)

#    def test_mood_invalid(self):
#        with self.assertRaises(TypeError):
#            sentiment()

    def test_love_valid(self):
        self.assertEqual(lovetest[names_test[2]], 0.0)

#    def test_love_invalid(self):
#        with self.assertRaises(TypeError):
#            love()
    def test_kidsafe_valid(self):
        self.assertEqual(round(kidsafe_test[names_test[3]], 1), 0.7)

#    def test_kidsafe_invalid(self):
#        with self.assertRaises(TypeError):
#            kid_safe()
            
    def test_length_valid(self):
        self.assertEqual(lengthtest[names_test[0]],7)

#    def test_length_invalid(self):
#        with self.assertRaises(TypeError):
#            length()
    
    def test_complexity_valid(self):
        self.assertEqual(round(comptest[names_test[2]], 1), 2.2)

#    def test_complexity_invalid(self):
#        with self.assertRaises(TypeError):
#            complexity()
    
    def test_result_rank_valid(self):
        self.assertTrue((a[max(a, key=a.get)] <=1) & (a[min(a, key=a.get)]>=0))
        self.assertTrue((b[max(b, key=b.get)] <=1) & (b[min(b, key=b.get)]>=0))
        self.assertTrue((c[max(c, key=c.get)] <=1) & (c[min(c, key=c.get)]>=0))
        self.assertTrue((d[max(d, key=d.get)] <=1) & (d[min(d, key=d.get)]>=0))
        self.assertTrue((e[max(e, key=e.get)] <=1) & (e[min(e, key=e.get)]>=0))

#    def test_result_rank_invalid(self):
#        with self.assertRaises(TypeError):
#            result_rank()
            
    def test_get_findic(self):
        self.assertEqual(len(findic_test[0]),8)
        self.assertEqual(list(findic_test[0].keys())[1],'artist')
    
#    def test_get_hash(self):
#        self.assertTrue(type(get_hash(names_test)),set)
        
    def test_main(self):
        with self.assertRaises(TypeError):
            main(None)
        
        
        
# Get tests as a test suite
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
# Run each test in suite
unittest.TextTestRunner().run(suite)