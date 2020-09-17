import numpy as np
import jieba
from gensim import corpora,models,similarities
import sys
import difflib
def delete_char(f):
    chars = ['\n', '\t', '，', '。', '；', '：', "？", '、', '！', '《', '》',
             '‘', '’', '“', '”', ' ', '1', '2', '3', '4', '5', '6', '7', '8',
             '9', '0', '.', '*', '-', '—', ',', '——', '……', '（', '）', '…',
             '%', '#', '@', '$', '￥', '~', '`', '~', '·']
    for item in chars:
        f = f.replace(item, '')
        return f


def compute_levenshtein_distance(f1, f2) -> int:
    f1=delete_char(f1)
    f2=delete_char(f2)

    leven_cost = 0
    s = difflib.SequenceMatcher(None, f1, f2)
    for tag, i1, i2, j1, j2 in s.get_opcodes():

        if tag == 'replace':
            leven_cost += max(i2 - i1, j2 - j1)
        elif tag == 'insert':
            leven_cost += (j2 - j1)
        elif tag == 'delete':
            leven_cost += (i2 - i1)

#    print(leven_cost)
    return leven_cost
def compute_levenshtein_similarity(f1, f2) -> float:
    """Compute the hamming similarity."""
    leven_cost = compute_levenshtein_distance(f1, f2)
#    print(len(f2))
    return 1 - (leven_cost / len(f2))

#这是一个将结果写入文件的方法
def write_result(output, file, test):
    with open(output, 'a') as file_handle:
        # 清空文件内容
        file_handle.truncate(0)
        sim=compute_levenshtein_similarity(file,test)
        if sim==0:
            print("这两个文件毫不相关哦")
        file_handle.write('%.4f' %sim)
        file_handle.close()
#用自己和自己比较，但相似度不是100%

#空文本的异常类
class BlankError(Exception):
    def __init__(self):
        print("这个文件没有内容哦")

if __name__ == '__main__':

    # 论文原文
    file_origin = open(sys.argv[1], 'r', encoding='utf-8').read()
    # 抄袭论文
    file_copy = open(sys.argv[2], 'r', encoding='utf-8').read()
    #计算相似度

    if file_origin=='' :
        raise BlankError
    if file_origin=='' :
        raise BlankError


    #sim4=str(sim4)
    # 输出文件
    file_output = sys.argv[3]
    write_result(file_output, file_origin, file_copy)


    #print("sim",compute_levenshtein_similarity(file_origin,file_copy))

