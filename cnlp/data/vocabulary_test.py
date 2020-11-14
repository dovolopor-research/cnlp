import unittest

from cnlp.data import Vocabulary
from cnlp.data import Tokenizer


class VocabularyTest(unittest.TestCase):
    def setUp(self):
        self.input_text_list = [
            "为中华之崛起而读书",
            "好好学习，天天向上"
        ]

        self.char_index_list = [
            [257, 209, 523, 159, 3606, 1539, 454, 1771, 277],
            [617, 617, 1146, 170, 3, 179, 179, 530, 138]
        ]
        self.char_token_list = [
            ['为', '中', '华', '之', '@UNK@', '起', '而', '读', '书'],
            ['好', '好', '学', '习', '，', '天', '天', '向', '上']
        ]

        self.word_index_list = [
            [22870, 19206, 24227, 185441, 423156, 476670],
            [157424, 584430, 151622, 584429, 584429, 584429]
        ]
        self.word_token_list = [
            ['为', '中华', '之', '崛起', '而', '读书'],
            ['好好学习', '@UNK@', '天天向上', '@PAD@', '@PAD@', '@PAD@']
        ]

        self.vocab_char = Vocabulary("char")
        self.vocab_word = Vocabulary("word")
        self.token = Tokenizer()

    def test_token_to_index(self):
        self.assertEqual(self.vocab_char.token_to_index(self.input_text_list), self.char_index_list)
        word_token_list = [self.token.cut(text) for text in self.input_text_list]
        self.assertEqual(self.vocab_word.token_to_index(word_token_list), self.word_index_list)

    def test_index_to_token(self):
        self.assertEqual(self.vocab_char.index_to_token(self.char_index_list), self.char_token_list)
        self.assertEqual(self.vocab_word.index_to_token(self.word_index_list), self.word_token_list)


if __name__ == '__main__':
    unittest.main()
