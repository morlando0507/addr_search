# encoding = utf-8

import jieba
import csv

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

csv_reader = csv.reader(open("addr_result.csv", "r"))
result_list = [row for row in csv_reader]
final_list = list("")
for row in result_list[1:]:
    seg_list = list(jieba.cut(row[0].replace(" ", "").replace("0", "").replace(";", "")))
    temp_list = list("")
    temp_list.append(row[0])
    temp_list.append(row[1])
    temp_list.append(row[-1])
    temp_list.append([row[4], row[5], row[6]])
    temp_list.extend(seg_list)
    final_list.append(temp_list)

with open("addr_cut_words_result.csv", "w+", newline="") as wr:
    writer = csv.writer(wr)
    for row in final_list:
        writer.writerow(row)

final_addr_dict = {"main_addr": "",
                   "addr_title": "",
                   "full_addr": "",
                   "words_frequency": ""}

with open("addr_result.csv", "r") as ar:
    ar_list = list(csv.reader(ar))[1:]
    main_addr_set = list()
    addr_words_frequency_source = list()
    for ar_row in ar_list:
        for fa_row in final_list:
            if ar_row[0] == fa_row[0]:
                addr_words_frequency_source.append([ar_row[0], ar_row[-1], fa_row[3], ar_row[1], fa_row[4:]])

addr_words_frequency_set_a = list()
location_index = set([s_row[1] + s_row[3] for s_row in addr_words_frequency_source])
for li in location_index:
    temp_words_list = list()
    temp_words_list2 = list()
    temp_words_list3 = list()
    for addr_row in addr_words_frequency_source:
        if li == addr_row[1] + addr_row[3]:
            temp_words_list.extend(addr_row[4])
            temp_words_list2.append(addr_row[4])
            temp_words_list3.extend(addr_row[2])
        else:
            continue
    addr_words_frequency_set_a.append([li, temp_words_list3, list(set(temp_words_list)), temp_words_list, temp_words_list2])

temp_words_frequency_dict_list = list()
for set_a_row in addr_words_frequency_set_a:
    temp_buffer = dict()
    temp_buffer["main_addr"] = set_a_row[0]
    temp_buffer["value"] = list()
    for addr_words_list in set_a_row[4]:
        words_frequency_dict_list = list()
        for keyword in addr_words_list:
            if keyword not in set_a_row[1]:
                words_frequency_dict = dict()
                words_frequency_dict["word_nm"] = keyword
                words_frequency_dict["word_cnt"] = set_a_row[3].count(keyword)
                if set_a_row[3].count(keyword) == 0:
                    words_frequency_dict["word_index"] = ""
                else:
                    words_frequency_dict["word_index"] = addr_words_list.index(keyword)
                words_frequency_dict_list.append(words_frequency_dict)
            else:
                continue
        temp_buffer["value"].append(words_frequency_dict_list)
    temp_words_frequency_dict_list.append(temp_buffer)

full_words_list = list()
for element_c in temp_words_frequency_dict_list:
    words_dict = dict()
    _words_list = list()
    words_dict["main_addr"] = element_c["main_addr"]
    for words_frequency_source in element_c["value"]:
        for word_index in range(0, len(words_frequency_source), 2):
            _words_dict = dict()
            try:
                if words_frequency_source[word_index]["word_cnt"] == words_frequency_source[word_index+1]["word_cnt"] \
                        and words_frequency_source[word_index]["word_index"] < words_frequency_source[word_index+1]["word_index"]:
                    print(words_frequency_source[word_index]["word_nm"]+words_frequency_source[word_index+1]["word_nm"],
                          words_frequency_source[word_index]["word_cnt"])
                    _words_dict["word"] = words_frequency_source[word_index]["word_nm"]+words_frequency_source[word_index+1]["word_nm"]
                    _words_dict["word_cnt"] = words_frequency_source[word_index]["word_cnt"]
                else:
                    print(words_frequency_source[word_index]["word_nm"], words_frequency_source[word_index]["word_cnt"])
                    _words_dict["word"] = words_frequency_source[word_index]["word_nm"]
                    _words_dict["word_cnt"] = words_frequency_source[word_index]["word_cnt"]
            except IndexError:
                continue
            _words_list.append(_words_dict)
        words_dict["value"] = _words_list
    full_words_list.append(words_dict)

words_frequency = set([i["word"] for r in full_words_list for i in r["value"]])

a = 1

