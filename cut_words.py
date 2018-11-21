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
