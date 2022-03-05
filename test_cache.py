import unittest
from Memory import Memory
from cache import Cache

class TestCache(unittest.TestCase):
    def setUp(self):
        self.mem = Memory()
        self.mem.read_mem('IPL.txt')
    
    def test_set_words_miss(self):
        #test if writing when not in cache
        c = Cache(self.mem)
        c.set_word(19, 9) 
        self.assertEqual(self.mem.words[19], 9, "word not written into memory")
    
    def test_set_words_hit(self):
        #test if writing when in cache
        c = Cache(self.mem)
        c.lines.append((4, [(3, 9)]))
        c.set_word(19,15)
        self.assertEqual(self.mem.words[19], 15, 'word not updated in memory')
        self.assertEqual(c.lines[0], (4, [(3, 15)]), 'incorrect writing to cache')

    def test_get_word_empty_miss(self):
        c = Cache(self.mem)
        c.get_word(3)
        self.assertEqual(c.lines[0][0], 0, 'incorrect tag')
        for idx, (byte_addr, word) in enumerate(c.lines[0][1]):
            with self.subTest(idx):
                self.assertEqual(byte_addr, idx, "loaded incorrect block")
                self.assertEqual(word, self.mem.words[idx])
    
    def test_get_words_full_miss(self):
        c = Cache(self.mem, max_size=1)
        c.get_word(3)
        res = c.get_word(10)

        self.assertEqual(res, self.mem.words[10], 'incorrect word fetched')
        self.assertEqual(len(c.lines), 1, 'not popping correctly')
        self.assertEqual(c.lines[0][0], 2, 'wrong tag')

        start = (10 // 4) * 4
        for idx, (byte_addr, word) in enumerate(c.lines[0][1]):
            with self.subTest(idx):
                self.assertEqual(byte_addr, (idx), "loaded incorrect block")
                self.assertEqual(word, self.mem.words[start + idx], 'pulled wrong block')

    def test_get_words_hit(self):
        c = Cache(self.mem)
        c.get_word(10)
        res = c.get_word(8)
        self.assertEqual(res, self.mem.words[8], 'incorrect word fetched')
        self.assertEqual(len(c.lines), 1, 'blocking incorrectly')


if __name__ == '__main__':
    unittest.main()









            
        
