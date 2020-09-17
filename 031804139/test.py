import numpy as np
import jieba
import matplotlib.pyplot as plt
import difflib
#增加删除标点符号的方法
def delete_char(f):
    chars = ['\n', '\t', '，', '。', '；', '：', "？", '、', '！', '《', '》',
             '‘', '’', '“', '”', ' ', '1', '2', '3', '4', '5', '6', '7', '8',
             '9', '0', '.', '*', '-', '—', ',', '——', '……', '（', '）', '…',
             '%', '#', '@', '$', '￥', '~', '`', '~', '·']
    for item in chars:
        f = f.replace(item, '')
        return f

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 加载停用词
stopwords = stopwordslist("hit_stopwords.txt")

#一、余弦算法
def cosine_similarity(f1, f2) -> float:

    #file_origin = open(f1, 'r', encoding='utf-8').read()

    #file_copy = open(f2, 'r', encoding='utf-8').read()
    f1 = delete_char(f1)
    f2 = delete_char(f2)
    seg1 = [word for word in jieba.cut(f1) if word not in stopwords]
    seg2 = [word for word in jieba.cut(f2) if word not in stopwords]
    word_list = list(set([word for word in seg1 + seg2]))#建立词库
    word_count_vec_1 = []
    word_count_vec_2 = []
    for word in word_list:
        word_count_vec_1.append(seg1.count(word))#文本1统计在词典里出现词的次数
        word_count_vec_2.append(seg2.count(word))#文本2统计在词典里出现词的次数

    vec_1 = np.array(word_count_vec_1)
    vec_2 = np.array(word_count_vec_2)
    #余弦公式

    num = vec_1.dot(vec_2.T)
    denom = np.linalg.norm(vec_1) * np.linalg.norm(vec_2)
    cos = num / denom
    sim = 0.5 + 0.5 * cos

    return sim

#二、levenshtein距离算法
def compute_levenshtein_distance(f1, f2) -> int:
    f1 = delete_char(f1)
    f2 = delete_char(f2)
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


#三、jaccard算法
def compute_jaccard_similarity(f1, f2) -> float:
    word_set1 = set(f1.strip(" ").split(" "))
    word_set2 = set(f2.strip(" ").split(" "))

    return len(word_set1 & word_set2) / len(word_set1 | word_set2)

#将结果可视化
def visual_tabel(l1,l2,l3):
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']= False

    titles=('test1','test2','test3','test4','test5','test6','test7','test8','test9')

    bar_width = 0.2
    index1 = np.arange(len(titles))
    index2 = index1 + bar_width
    index3 = index2 + bar_width

    plt.bar(index1,height=l1,width=bar_width,color='b',label='cosine_sim')
    plt.bar(index2,height=l2,width=bar_width,color='g',label='levenshtein_sim')
    plt.bar(index3, height=l3, width=bar_width, color='r', label='jaccard_sim')

    plt.legend()
    plt.xticks(index1+bar_width/2,titles)
    plt.ylabel('重复率')
    plt.title('三种算法重复率检测结果比较')

    plt.show()
if __name__ == "__main__":
    #读取原文件
    file = open('orig.txt', 'r', encoding='utf-8').read()
    #读取待测试的txt文件
    c1 = open('orig_0.8_add.txt', 'r', encoding='utf-8').read()
    c2 = open('orig_0.8_del.txt', 'r', encoding='utf-8').read()
    c3 = open('orig_0.8_dis_1.txt', 'r', encoding='utf-8').read()
    c4 = open('orig_0.8_dis_3.txt', 'r', encoding='utf-8').read()
    c5 = open('orig_0.8_dis_7.txt', 'r', encoding='utf-8').read()
    c6 = open('orig_0.8_dis_10.txt', 'r', encoding='utf-8').read()
    c7 = open('orig_0.8_dis_15.txt', 'r', encoding='utf-8').read()
    c8 = open('orig_0.8_mix.txt', 'r', encoding='utf-8').read()
    c9 = open('orig_0.8_rep.txt', 'r', encoding='utf-8').read()
    #c10 = open('test.txt', 'r', encoding='utf-8').read()
    list_file = [c1,c2,c3,c4,c5,c6,c7,c8,c9]
    list_sim_cos=[]
    list_sim_leven=[]
    list_sim_jaccard = []
    #计算两种算法的重复率并打印结果
    for i in list_file:
        sim_cos=cosine_similarity(file,i)
        sim_leven=compute_levenshtein_similarity(file, i)
        sim_jaccard = compute_jaccard_similarity(file, i)
        list_sim_cos.append(sim_cos)
        list_sim_leven.append(sim_leven)
        list_sim_jaccard.append(sim_jaccard)
        print("cosine_sim：", sim_cos," levenshtein_sim：", sim_leven," jaccard_sim：",sim_jaccard )
    #可视化结果

    visual_tabel(list_sim_cos,list_sim_leven,list_sim_jaccard)