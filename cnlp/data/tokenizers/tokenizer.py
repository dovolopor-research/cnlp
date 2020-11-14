from cnlp.data import Vocabulary
from cnlp.data.tokenizers import dag
from cnlp.data.word_dict import WordDict
from cnlp.data.tokenizers import mechanical


class Tokenizer(object):
    def __init__(self) -> None:
        self.wd = WordDict()
        self.common_word_dict_list = self.wd.get_common_word_dict_list()
        self.word_freq_dict, self.word_freq_total = self.wd.get_common_word_freq_dict()
        self.char_radical_dict = self.wd.get_radical_dict()
        self.char_stroke_dict = self.wd.get_stroke_dict()

        self.vocab = Vocabulary()

    # 分词
    def cut(self, text: str = None, methods: str = "dag") -> list:
        if text:
            if methods == "mechanical":
                tokenizer_list = mechanical.cut_with_forward_match(text, self.common_word_dict_list)
            elif methods == "dag":
                tokenizer_list = dag.cut(text, self.word_freq_dict, self.word_freq_total)
            else:
                raise ValueError(f"Error cut methods: {methods}")
        else:
            raise ValueError("text is empty!")
        return tokenizer_list

    # 偏旁
    def radical(self, text: str = None) -> list:
        radical_list = []
        for char in text:
            if char in self.char_radical_dict.keys():
                radical_list.append(self.char_radical_dict[char])
            else:
                radical_list.append([self.vocab.unknown_token])
        return radical_list

    # 笔画
    def stroke(self, text: str = None) -> list:
        stroke_list = []
        for char in text:
            if char in self.char_stroke_dict.keys():
                stroke_list.append(self.char_stroke_dict[char])
            else:
                stroke_list.append([self.vocab.unknown_token])
        return stroke_list
