import unittest
import filecmp
import subprocess
from huffman import *

usediff = False  # When comparing files: True to use Linux diff, False to use Python filecmp

class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

        freqlist	= cnt_freq("file1.txt")
        anslist = [4,3,2,1]
        self.assertListEqual(freqlist[97:101], anslist)

    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_header(self):
        #All these tests check headers of files of varying complexity
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

        freqlist=cnt_freq("file1.txt")
        self.assertEqual(create_header(freqlist), "32 3 97 4 98 3 99 2 100 1")

        freqlist=cnt_freq("multiline.txt")
        self.assertEqual(create_header(freqlist), "10 2 32 8 46 1 84 1 97 3 101 5 102 2 104 2 105 7 108 5 109 2 110 4 111 1 112 3 115 3 116 3 117 2 119 1 120 1")

        freqlist=cnt_freq("declaration.txt")
        self.assertEqual(create_header(freqlist), "10 166 32 1225 38 1 39 1 44 109 45 3 46 36 49 1 52 1 54 1 55 2 58 10 59 10 65 22 66 7 67 19 68 5 69 3 70 17 71 15 72 24 73 8 74 5 75 1 76 15 77 3 78 8 79 6 80 23 82 9 83 23 84 15 85 3 87 13 97 466 98 88 99 171 100 253 101 875 102 169 103 116 104 331 105 451 106 12 107 13 108 216 109 144 110 487 111 518 112 116 113 6 114 420 115 460 116 640 117 211 118 74 119 84 120 9 121 82 122 4")

        freqlist=cnt_freq("oneLetter.txt")
        self.assertEqual(create_header(freqlist), "97 5")
    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        if usediff:
            err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
            self.assertEqual(err, 0)
        else:
            self.assertTrue(filecmp.cmp("file1_out.txt", "file1_soln.txt"))
    def test_02_textfile(self):
        huffman_encode("file2.txt", "file2_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        if usediff:
            err = subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell = True)
            self.assertEqual(err, 0)
        else:
            self.assertTrue(filecmp.cmp("file2_out.txt", "file2_soln.txt"))
    def test_multiline_textfile(self):
        huffman_encode("multiline.txt", "multiline_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        if usediff:
            err = subprocess.call("diff -wb multiline_out.txt multiline_soln.txt", shell = True)
            self.assertEqual(err, 0)
        else:
            self.assertTrue(filecmp.cmp("multiline_out.txt", "multiline_soln.txt"))
    def test_declaration_textfile(self):
        huffman_encode("declaration.txt", "declaration_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        if usediff:
            err = subprocess.call("diff -wb declaration_out.txt declaration_soln.txt", shell = True)
            self.assertEqual(err, 0)
        else:
            self.assertTrue(filecmp.cmp("declaration_out.txt", "declaration_soln.txt"))
    def test_empty_textfile(self):
        huffman_encode("empty_file.txt", "empty_file_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        if usediff:
            err = subprocess.call("diff -wb empty_file.txt empty_soln.txt", shell = True)
            self.assertEqual(err, 0)
        else:
            self.assertTrue(filecmp.cmp("empty_out.txt", "empty_soln.txt"))
    def test_oneLetter_textfile(self):
        huffman_encode("oneLetter.txt", "oneLetter_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        if usediff:
            err = subprocess.call("diff -wb oneLetter.txt oneLetter_soln.txt", shell = True)
            self.assertEqual(err, 0)
        else:
            self.assertTrue(filecmp.cmp("oneLetter_out.txt", "oneLetter_soln.txt"))

    #Tests a file that doesn't exist
    def test_incorrect_textfile(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode("sike.txt", "sike_out.txt")




if __name__ == '__main__': 
   unittest.main()
