# encoding = utf-8

# import jieba
import csv
import thulac

# seg_list = jieba.cut("德汉街8座114铺派送拨打17099730680陈耀忠签收", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("德汉街8座114铺派送拨打17099730680陈耀忠签收", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

# seg_list = jieba.cut("德汉街8座114铺派送拨打17099730680陈耀忠签收")  # 默认是精确模式
# print(list(seg_list))
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("德汉街8座114铺派送拨打17099730680陈耀忠签收")  # 搜索引擎模式
# print(", ".join(seg_list))

'''
加载停用词
'''


def stopwords(path):

    words_list = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]
    return words_list


'''
对地址进行切词
'''
csv_reader = csv.reader(open("addr_result.csv", "r"))
result_list = [row for row in csv_reader]
final_list = list()
output_for_hive = list()
# 初始化thulac 切词器,使用地址词典
thu1 = thulac.thulac(user_dict="THUOCL_diming.txt", seg_only=True)
for row in result_list[1:]:
    seg_list = list()
    # t_seg_list_jieba = jieba.cut(row[0][3:].replace(" ", "").replace(";", "").replace(".", "").replace("，", "")
    #                              .replace(",", "").replace("。", ""))
    t_seg_list_thu = thu1.cut(row[0][3:].replace(" ", "").replace(";", "").replace(".", "").replace("，", "")
                              .replace(",", "").replace("。", ""), text=False)
    stopwordslist = stopwords('stopwordslist.txt')
    for word in t_seg_list_thu:
        if word[0] != '\t':
            seg_list.append(word[0])
        # if word[0] not in stopwordslist and word[0] != '\t':
        #     seg_list.append(word[0])
    temp_list = list()
    temp_list.append(row[0])
    temp_list.append(row[1])
    temp_list.append({"local_addr": row[5] + row[6] + row[7],
                      "province": row[5],
                      "city": row[6],
                      "district": row[7]})
    temp_list.append(row[5] + row[6] + row[7])
    temp_list.append(seg_list)
    temp_list.extend(seg_list)
    final_list.append(temp_list)
    output_for_hive.append(temp_list[0:5])

'''
包含切词结果
'''
with open("addr_cut_words_result.csv", "w+", newline="") as wr:
    writer = csv.writer(wr)
    for row in final_list:
        writer.writerow(row)

'''
不包含切词结果
'''
with open("addr_cut_words_result_for_hive.csv", "w+", newline="") as wr_h:
    writer = csv.writer(wr_h)
    for row in output_for_hive:
        writer.writerow(row)

with open("addr_result.csv", "r") as ar:
    ar_list = list(csv.reader(ar))[1:]
    main_addr_set = list()
    addr_words_frequency_source = list()
    for ar_row in ar_list:
        for fa_row in final_list:
            if ar_row[0] == fa_row[0]:
                addr_words_frequency_source.append([ar_row[0], ar_row[1], fa_row[2], fa_row[5:]])

addr_words_frequency_set_a = list()
location_index = list(set([s_row[2]["local_addr"] for s_row in addr_words_frequency_source]))
for li in location_index:
    temp_words_list = list()
    temp_words_list2 = list()
    temp_words_list3 = list()
    for addr_row in addr_words_frequency_source:
        if li == addr_row[2]["local_addr"]:
            if len(temp_words_list3) == 0:
                temp_words_list3 = addr_row[2]
            temp_words_list.extend(addr_row[3])
            temp_words_list2.append(addr_row[3])
        else:
            continue
    addr_words_frequency_set_a.append([temp_words_list3["local_addr"], temp_words_list3,
                                       list(set(temp_words_list)), temp_words_list, temp_words_list2])

with open("addr_cut_words_result_set_a.csv", "w+", newline="") as wr_seta:
    writer = csv.writer(wr_seta)
    for row in addr_words_frequency_set_a:
        writer.writerow(row)

'''
词频计算部分及切词结果合并
'''
temp_words_frequency_dict_list = list()
for set_a_row in addr_words_frequency_set_a:
    temp_buffer = dict()
    temp_buffer["addr_area"] = set_a_row[0]
    temp_buffer["main_addr"] = set_a_row[1]
    temp_buffer["value"] = list()
    for addr_words_list in set_a_row[2]:
        words_frequency_dict = dict()
        words_frequency_dict["word_nm"] = addr_words_list
        words_frequency_dict["word_cnt"] = set_a_row[3].count(addr_words_list)
        temp_buffer["value"].append(words_frequency_dict)
        # for keyword in addr_words_list:
        #     if keyword not in [k[1] for k in set_a_row[2].items()]:
        #         words_frequency_dict = dict()
        #         words_frequency_dict["word_nm"] = keyword
        #         words_frequency_dict["word_cnt"] = set_a_row[4].count(keyword)
        #         if set_a_row[3].count(keyword) == 0:
        #             words_frequency_dict["word_index"] = ""
        #         else:
        #             temp_s_list = addr_words_list
        #             word_i = addr_words_list.index(keyword)
        #             temp_s_list[word_i] = keyword
        #             words_frequency_dict["word_index"] = addr_words_list.index(keyword)
        #         words_frequency_dict_list.append(words_frequency_dict)
        #     else:
        #         continue
        # temp_buffer["value"].append(words_frequency_dict_list)
    temp_words_frequency_dict_list.append(temp_buffer)

# full_words_list = list()
# for element_c in temp_words_frequency_dict_list:
#     words_dict = dict()
#     _words_list = list()
#     words_dict["main_addr"] = element_c["main_addr"]
#     words_dict["addr_area"] = element_c["addr_area"]
#     for words_frequency_source in element_c["value"]:
#         for word_index in range(0, len(words_frequency_source)):
#             _words_dict = dict()
#             try:
#                 if words_frequency_source[word_index]["word_cnt"] == words_frequency_source[word_index+1]["word_cnt"]
#                         and words_frequency_source[word_index]["word_index"] < words_frequency_source[word_index+1]["word_index"]:
#                     print(words_frequency_source[word_index]["word_nm"]+words_frequency_source[word_index+1]["word_nm"],
#                           words_frequency_source[word_index]["word_cnt"])
#                     _words_dict["word"] = words_frequency_source[word_index]["word_nm"]+words_frequency_source[word_index+1]["word_nm"]
#                     _words_dict["word_cnt"] = words_frequency_source[word_index]["word_cnt"]
#                 else:
#                     print(words_frequency_source[word_index]["word_nm"], words_frequency_source[word_index]["word_cnt"])
#                     _words_dict["word"] = words_frequency_source[word_index]["word_nm"]
#                     _words_dict["word_cnt"] = words_frequency_source[word_index]["word_cnt"]
#             except IndexError:
#                 continue
#             _words_list.append(_words_dict)
#         words_dict["value"] = _words_list
#     element_c["word_combined_list"] = _words_list
#     full_words_list.append(words_dict)
#
# words_frequency = set([i["word"] for r in full_words_list for i in r["value"]])

with open("addr_cut_words_result_freq.csv", "w+", newline="") as wr_freq:
    writer = csv.writer(wr_freq)
    for row in temp_words_frequency_dict_list:
        writer.writerow(row)


