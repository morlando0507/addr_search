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

csv_reader = csv.reader(open("cut_words_source.csv"))
csv_headers = ["main_addr", "addr_title"]
result_list = [row for row in csv_reader]
final_list = list("")
for row in result_list[1:]:
    seg_list = list(jieba.cut(row[0].split("\t")[1].replace(" ","")))
    temp_list = list("")
    temp_list.append(row[0].split("\t")[0])
    temp_list.append(row[0].split("\t")[1])
    temp_list.extend(seg_list)
    final_list.append(temp_list)
list_len = max([len(r) for r in final_list]) - 2
for i in range(list_len + 1):
    csv_headers.append("col" + str(i))

with open("addr_cut_words_result.csv", "w+", newline="") as wr:
    writer = csv.writer(wr)
    for row in final_list:
        writer.writerow(row)

final_addr_dict = {"main_addr": "",
                   "addr_title": "",
                   "full_addr": "",
                   "words_frequency": ""}

for i in final_list:
    i.append(str(i[0]) + str(i[1]))

with open("addr_result.csv", "r") as ar:
    ar_list = list(csv.reader(ar))[1:]
    main_addr_set = list("")
    addr_words_frequency_source = list("")
    for ar_row in ar_list:
        for fa_row in final_list:
            if ar_row[0] == fa_row[-1]:
                addr_words_frequency_source.append([ar_row[0], ar_row[4], fa_row[2:-1]])

addr_words_frequency_set_a = list("")
addr_words_frequency_set_b = list("")
location_index = set([s_row[1] for s_row in addr_words_frequency_source])
for li in location_index:
    temp_words_list = list("")
    for addr_row in addr_words_frequency_source:
        if li == addr_row[1]:
            temp_words_list.extend(addr_row[2])
        else:
            continue
    addr_words_frequency_set_a.append([li, list(set(temp_words_list))])
    addr_words_frequency_set_b.append([li, list(temp_words_list)])

words_frequency_dict_list = list("")

for set_a_row in addr_words_frequency_set_a:
    words_frequency_dict = {}
    for set_b_row in addr_words_frequency_set_b:
        if set_a_row[0] == set_b_row[0]:
            for w in set_a_row[1]:
                words_frequency_dict[w] = set_b_row[1].count(w)
    words_frequency_dict_list.append([set_a_row[0], sorted(words_frequency_dict.items(), key=lambda x:x[1], reverse=True)])

with open("words_frequency_result.csv", "w+", newline="") as wfr:
    csvwriter = csv.writer(wfr)
    for write_row in words_frequency_dict_list:
        csvwriter.writerow(write_row)

    a = 1


