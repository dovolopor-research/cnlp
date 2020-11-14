import re
from math import log

re_cn = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&._%-]+)", re.U)
re_en = re.compile("[a-zA-Z0-9]", re.U)


def cut(sentence, freq_dict, freq_total):
    block_list = re_cn.split(sentence)
    cut_result_list = []
    for block in block_list:
        # 跳过空的 block
        if not block:
            continue
        if re_cn.match(block):
            cut_result_list.extend(cut_util(block, freq_dict, freq_total))
        else:
            cut_result_list.append(block)
    return cut_result_list


def cut_util(sentence, freq_dict, freq_total):
    word_index = 0
    word_buf = ""
    result = []
    route = _calc_dag_with_dp(sentence, freq_dict, freq_total)
    while word_index < len(sentence):
        word_index_end = route[word_index][1] + 1
        word = sentence[word_index:word_index_end]
        # 匹配出英文
        if re_en.match(word) and len(word) == 1:
            word_buf += word
            word_index = word_index_end
        else:
            if word_buf:
                result.append(word_buf)
                word_buf = ""
            else:
                result.append(word)
                word_index = word_index_end
    # 纯英文
    if word_buf:
        result.append(word_buf)
    return result


def _get_dag(sentence, freq_dict):
    dag = {}
    sen_len = len(sentence)
    for i in range(sen_len):
        temp_list = []
        j = i
        frag = sentence[i]
        while j < sen_len and frag in freq_dict:
            if freq_dict[frag]:
                temp_list.append(j)
            j += 1
            frag = sentence[i:j + 1]
        if not temp_list:
            temp_list.append(i)
        dag[i] = temp_list
    return dag


def _calc_dag_with_dp(sentence, freq_dict, freq_total):
    dag = _get_dag(sentence, freq_dict)
    sen_len = len(sentence)
    route = {sen_len: (0, 0)}
    # 取 log 防止数值下溢
    log_total = log(freq_total)
    for sen_index in reversed(range(sen_len)):
        freq_list = []
        for word_index in dag[sen_index]:
            word_freq = freq_dict.get(sentence[sen_index:word_index + 1])
            # 解决 log(0) 无定义问题, 则取 log(1)=0
            freq_index = (log(word_freq or 1) - log_total + route[word_index + 1][0], word_index)
            freq_list.append(freq_index)
        route[sen_index] = max(freq_list)
    return route
