# coding=utf-8


def str_intersection(first_str, second_str):

    alist = list(first_str.replace(";", ""))
    blist = list(second_str.replace(";", ""))

    r = []
    for i in range(0, len(alist)):
        for j in range(0, len(blist)):
            if i == j and alist[i] == blist[j]:
                r.append(alist[i])
            else:
                continue
    return "".join(_ for _ in r)

# def str_levenstein


if __name__=="__main__":

    print(str_intersection("0;;上海市;宝山区;全区;;;;罗泾镇潘沪路69弄120期320号5004hd", "0;;上海市;宝山区;全区;;;;罗泾镇潘沪路69弄20期210号104hd"))