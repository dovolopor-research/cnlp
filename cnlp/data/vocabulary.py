import logging
from pkg_resources import resource_stream

logger = logging.getLogger(__name__)


class Vocabulary(object):
    """
    vocab_type: char, word, radical, stroke
    """

    def __init__(self, vocab_type: str = "char", vocab_file: str = None) -> None:
        self.vocab_type = vocab_type
        self.vocab_file = vocab_file
        self._stream_args = ["cnlp", f"src/{vocab_type}_vocab.txt"]

        self.padding_token = "@PAD@"
        self.unknown_token = "@UNK@"

    @staticmethod
    def _read_vocab_from_file(vocab_path: str) -> list:
        with open(vocab_path, "r") as vocab_file:
            vocab_list = [_v.strip() for _v in vocab_file]
        return vocab_list

    @staticmethod
    def _read_vocab_from_stream(stream_args: list) -> list:
        with resource_stream(*stream_args) as stream:
            vocab_list = [_v.decode().strip("\n") for _v in stream.readlines()]
        return vocab_list

    def _extend_vocab(self, vocab_data: list) -> list:
        vocab_data.append(self.padding_token)
        vocab_data.append(self.unknown_token)
        return vocab_data

    def get_default_vocab(self, extend_pad_and_unk: bool = True) -> list:
        if self.vocab_file:
            _vocab = self._read_vocab_from_file(self.vocab_file)
        else:
            _vocab = self._read_vocab_from_stream(self._stream_args)

        if extend_pad_and_unk:
            _vocab = self._extend_vocab(_vocab)
        return _vocab

    def token_sequence_util(self, token_list: list = None, max_len: int = None) -> list:
        new_token_list = []
        for token_item in token_list:
            if len(token_item) >= max_len:
                token_array = [token for token in token_item[:max_len]]
            else:
                # padding sequence
                token_array = [token for token in token_item] + [self.padding_token] * (max_len - len(token_item))
            new_token_list.append(token_array)
        return new_token_list

    def token_to_index(self, token_list: list = None, max_len: int = None) -> list:
        vocab_data = self.get_default_vocab()

        if isinstance(token_list, list):
            if self.vocab_type == "char" and not isinstance(token_list[0], str):
                raise TypeError(f"char array must 1 dim!")
            elif self.vocab_type == "word" and not isinstance(token_list[0], list):
                raise TypeError(f"word array must 2 dim!")
        else:
            raise TypeError(f"not support this type: {type(token_list)}")

        if not max_len:
            token_len_list = [len(_token) for _token in token_list]
            max_len = max(token_len_list)
            if max_len > 100:
                # 如果 max_len 没有默认值，且最大长度超过了 100，自动取覆盖 80% 数据的长度
                logger.warning(
                    ">> info: max length is 0 or empty, automatically take over 80% of the length of the data.")
                max_len = sorted(token_len_list)[int(len(token_list) * 0.8)]
                logger.warning(f">> info: 80% max length is {max_len}")

        index_list = []
        for token_item in self.token_sequence_util(token_list, max_len):
            index_line = []
            for token in token_item:
                if token in vocab_data:
                    index_line.append(vocab_data.index(token))
                else:
                    index_line.append(vocab_data.index(self.unknown_token))
            index_list.append(index_line)
        return index_list

    def index_to_token(self, index_list: list = None) -> list:
        vocab_data = self.get_default_vocab()
        max_vocab_length = len(vocab_data)

        token_list = []
        if index_list:
            for index_item in index_list:
                if isinstance(index_item, int):
                    if index_item < max_vocab_length:
                        token_list.append(vocab_data[index_item])
                    else:
                        token_list.append(self.padding_token)
                elif isinstance(index_item, list):
                    token = []
                    for _index in index_item:
                        if isinstance(_index, int):
                            if _index < max_vocab_length:
                                token.append(vocab_data[_index])
                            else:
                                token.append(self.padding_token)
                        else:
                            raise TypeError(f"error type data: {index_item}")

                    token_list.append(token)
                else:
                    raise TypeError(f"error type data: {index_item}")

            return token_list
        else:
            raise ValueError("index_list is None or empty !")
