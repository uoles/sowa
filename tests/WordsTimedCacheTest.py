import time
import unittest

from classes.WordsTimedCache import WordsTimedCache


class WordsTimedCacheTest(unittest.TestCase):
    def test_empty_dict(self):
        cache = WordsTimedCache(1)
        self.assertFalse(cache.check('word'))

    def test_contains_word(self):
        cache = WordsTimedCache(100)
        cache.put('word')
        self.assertTrue(cache.check('word'))

    def test_expired_time(self):
        cache = WordsTimedCache(1)
        cache.put('word')
        time.sleep(2)
        self.assertTrue(cache.check('word'))

    def test_string_view(self):
        cache = WordsTimedCache(100)
        cache.put('word-1')
        cache.put('word-2')
        cache.put('word-3')
        string_view = cache.to_string()
        self.assertTrue("word-1" in string_view)
        self.assertTrue("word-2" in string_view)
        self.assertTrue("word-3" in string_view)
        self.assertFalse("word-4" in string_view)

    def test_keys_view(self):
        cache = WordsTimedCache(100)
        cache.put('word-1')
        cache.put('word-2')
        cache.put('word-3')
        string_view = cache.keys_as_string()
        self.assertTrue("word-1" in string_view)
        self.assertTrue("word-2" in string_view)
        self.assertTrue("word-3" in string_view)
        self.assertFalse("word-4" in string_view)


if __name__ == '__main__':
    unittest.main()