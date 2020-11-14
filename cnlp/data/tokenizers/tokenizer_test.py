import unittest

from cnlp.data.tokenizers.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.t = Tokenizer()
        self.text_list = [
            "为中华之崛起而读书",
            "武汉市长江大桥"
        ]
        self.cut_text_list = [
            "为/中华/之/崛起/而/读书",
            "武汉市/长江大桥"
        ]

    def test_cut(self):
        for index in range(len(self.text_list)):
            tokens = self.t.cut(self.text_list[index], "dag")
            self.assertEqual("/".join(tokens), self.cut_text_list[index])

            tokens = self.t.cut(self.text_list[index], "mechanical")
            self.assertEqual("/".join(tokens), self.cut_text_list[index])


if __name__ == '__main__':
    unittest.main()
