from pkg_resources import resource_stream


class WordDict(object):
    def __init__(self):
        self.word_dict_args = ["cnlp", "src/word_dict.txt"]
        self.radical_dict_args = ["cnlp", "src/radical_dict.txt"]
        self.stroke_dict_args = ["cnlp", "src/stroke_dict.txt"]

    def get_common_word_dict_list(self):
        word_dict_list = []
        _stream = resource_stream(*self.word_dict_args)
        for line in _stream.readlines():
            line_list = line.decode().strip().split(" ")
            word_dict_list.append(line_list)
        _stream.close()
        word_dict_list = sorted(word_dict_list, key=lambda x: (len(x[0]), x[1]), reverse=True)
        word_dict_list = [word[0] for word in word_dict_list]
        return word_dict_list

    def get_common_word_freq_dict(self):
        word_freq_dict = {}
        word_freq_total = 0
        _stream = resource_stream(*self.word_dict_args)
        for line in _stream.readlines():
            word, freq = line.decode("utf-8").split(" ")[:2]
            freq = int(freq)
            word_freq_dict[word] = freq
            word_freq_total += freq
            for word_index in range(len(word)):
                word_frag = word[:word_index + 1]
                if word_frag not in word_freq_dict:
                    word_freq_dict[word_frag] = 0
        _stream.close()
        return word_freq_dict, word_freq_total

    def get_radical_dict(self):
        radical_dict = {}
        with resource_stream(*self.radical_dict_args) as _stream:
            for line in _stream.readlines():
                char, radical = line.decode().strip().split(":")
                radical_dict[char] = radical
        return radical_dict

    def get_stroke_dict(self):
        stroke_dict = {}
        with resource_stream(*self.stroke_dict_args) as _stream:
            for line in _stream.readlines():
                char, strokes = line.decode().strip().split(":")
                stroke_dict[char] = strokes.split(",")
        return stroke_dict
