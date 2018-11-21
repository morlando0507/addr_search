# coding = utf-8

import requests
import random
import json
import csv


get_url = "https://apis.map.qq.com/ws/geocoder/v1/?address=%s&key=%s"

key_list = ["WZQBZ-S5AKJ-U7LFP-F4M5K-W2RL2-7AFX4",
            "J4DBZ-2G7CF-LGCJK-JE64Q-CET2S-PTFFB",
            "2AUBZ-ZZJC4-TJBUA-DRIMF-SXJSZ-U4BCR",
            "TYFBZ-IXW6J-HZEFA-FNEPP-6LFLE-H2BVW",
            "FLHBZ-MVEKI-P3JGW-5OBZO-WUV7J-NOFRJ",
            "2TQBZ-IICC3-PQP3R-YC5DB-6Q4E6-QLFNE",
            "DKZBZ-4SWCI-FMEGU-53GK5-4TKZ5-7LBHY",
            "CG2BZ-7MR65-IRWIP-Q4VTM-AULDT-6DB4E",
            "DXYBZ-3LA6F-AQDJK-J2BQQ-MUBB3-V7F3S",
            "L23BZ-JAPKX-WLX4Z-Z3RQ3-UKLIS-YJBSJ"]

result_list = []

with open("recv_address.txt", "rb") as fp:
    addr_list = [i.strip() for i in fp.readlines()]
    for ad in addr_list:
        result_dict = {}
        _get_url = get_url %(ad.decode().replace("\ufeff","").replace(",","").replace(";","").replace(" ","").replace("#","号").replace("全区","").replace("\xa0",""), random.choice(key_list))
        try:
            result = json.loads(requests.get(_get_url).content.decode())
        except Exception:
            continue
        result_dict["origin_addr"] = ad.decode().replace("\ufeff", "")
        if result['status'] == 0:
            result_dict["title"] = result["result"]["title"]
            result_dict["lng"] = result["result"]["location"]["lng"]
            result_dict["lat"] = result["result"]["location"]["lat"]
            result_dict["province"] = result["result"]["address_components"]["province"]
            result_dict["city"] = result["result"]["address_components"]["city"]
            result_dict["district"] = result["result"]["address_components"]["district"]
            result_dict["street"] = result["result"]["address_components"]["street"]
            result_dict["street_number"] = result["result"]["address_components"]["street_number"]
        else:
            result_dict["title"] = ""
            result_dict["lng"] = ""
            result_dict["lat"] = ""
            result_dict["province"] = ""
            result_dict["city"] = ""
            result_dict["district"] = ""
            result_dict["street"] = ""
            result_dict["street_number"] = ""
            print(ad.decode() + " " + result["message"])
        result_list.append(result_dict)
        # a = 1

headers = [k for k in result_list[0]]

with open("addr_result.csv", "w+", newline="") as wr:
    writer = csv.DictWriter(wr, headers)
    writer.writeheader()
    for row in result_list:
        try:
            writer.writerow(row)
        except Exception:
            continue

