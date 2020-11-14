def cut_with_forward_match(input_char, char_dict):
    result = []
    max_word_len = len(char_dict[0])
    while len(input_char):
        cut_word = ""
        range_len = max_word_len if len(input_char) > max_word_len else len(input_char)
        for cut_len in range(range_len, 0, -1):
            tmp_cut_word = input_char[:cut_len]
            if tmp_cut_word in char_dict:
                cut_word = tmp_cut_word
                input_char = input_char[cut_len:]
                break

        if len(cut_word) == 0:
            cut_word = input_char[:1]
            input_char = input_char[1:]

        result.append(cut_word)
    return result
