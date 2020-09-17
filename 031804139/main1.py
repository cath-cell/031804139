# 语料库、模型、相似度
from gensim import corpora, models, similarities
# 结巴分词
import jieba
# defaultdict：用于数据过滤的词典
from collections import defaultdict
import numpy as np
import sys

# doc1、doc2代表了流程中的文本数据1
#doc1 = "C:/Users/hp/Desktop/orig.txt"
#doc2 = "C:/Users/hp/Desktop/test.txt"


#计算余弦相似度
'''
def dist_cos(vec1,vec2):
    return dist1
'''

def dist_cos(vec1, vec2) :
    dist1 = float(np.dot(word_vector1,word_vector2) / (np.linalg.norm(word_vector1) * np.linalg.norm(word_vector2)))
    return dist1
'''
def write_result(output,file,test):
    with open(output,'a')as file_handle:
        file_handle.truncate(0)
        if round(dist_cos(vec1,vec2),2) == 1.00:
            if file

        file_handle.write
'''
if __name__ == '__main__':
    #论文原文
    file_origin = open(sys.argv[1],'r',encoding='utf-8').read()
    #抄袭论文
    file_copy = open(sys.argv[2],'r',encoding='utf-8').read()
    #输出文件
#    file_output = sys.argv[3]

    # 对文本数据进行分词
    data1 = jieba.cut(file_origin)
    data2 = jieba.cut(file_copy)
    list_word1 = (','.join(data1)).split(',')
    list_word2 = (','.join(data2)).split(',')
    #列出所有的词并求交集
    key_word = list(set(list_word1 + list_word2))

    #用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2= np.zeros(len(key_word))

    #计算词频
    for i in range(len(key_word)):
        #遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i]+=1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i]+=1

    result=dist_cos(word_vector1, word_vector2)
    result=str(result)
#    file_origin.close()
#    file_copy.close()
    #最终保存一下结果
    with open('C:\\Users\\hp\\Desktop\\result.txt','w')as f:
        f.write(result)

    print(result)
