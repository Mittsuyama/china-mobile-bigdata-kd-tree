# import
import re

# initialization & const variable
DECIMAL_COUNT = 2
RATE = pow(10, 2)
PRECISION = 1
type_to_number = {
    "金融保险服务": 1,       # 金融

    "购物服务": 2,          # 商品交易和售后
    "汽车服务": 2,
    "汽车维修": 2,
    "汽车销售": 2,
    "摩托车服务": 2,

    "风景名胜": 3,          # 景区

    "科教文化服务": 4,       # 科教文化

    "住宿服务": 5,          # 居住
    "商务住宅": 5,
    "地名地址信息": 5,

    "通行设施": 6,          # 交通
    "室内设施": 6,
    "交通设施服务": 6,
    "道路附属设施": 6,

    "政府机构及社会团体": 7,  # 政府和公共设施
    "公共设施": 7,
    "体育休闲服务": 7,
    "事件活动": 7,

    "医疗保健服务": 8,       # 医疗

    "餐饮服务": 9,          # 餐饮

    "生活服务": 10,          # 生活

    "公司企业": 0,          # 公司企业
}
distribution = {}
POI_TYPE_COUNT = 11
count = [0] * POI_TYPE_COUNT
second_type = set()

# define function
def norm_float(f):
    tail = float(int(round(f * RATE * 10, 0)) % 10 // PRECISION * PRECISION) / (RATE * 10.0)
    number = float(int(f * RATE)) / RATE
    return round(number + tail, 3)

# read file
lines = open("../data/poi.txt", "r").readlines()
for line in lines:
    split_reuslt = line.split(",")
    if len(split_reuslt) >= 5:
        try:
            lng = float(split_reuslt[5])
            lat = float(split_reuslt[6])
            if 126.48 < lng < 126.83 and 45.64 < lat < 45.86:
                lng = norm_float(lng)
                lat = norm_float(lat)
                pos = str(lng) + "," + str(lat)
                poi_type = type_to_number[split_reuslt[10]]
                second_type.add(split_reuslt[11])

                vector = []
                if pos in distribution:
                    vector = distribution[pos]
                else:
                    vector = [0] * POI_TYPE_COUNT
                vector[poi_type] += 1
                count[poi_type] += 1
                distribution.update({ pos: vector })
        except:
            pass

# std out
for index in range(0, len(count)):
    t_name = ""
    for key in type_to_number:
        if type_to_number[key] == index:
            t_name = key
            break
    print("{}: {}".format(t_name, count[index]))

print("second type count:" + str(len(second_type)))

# write to file
out_file = open("../data/poi_type.txt", "w")
for pos in distribution:
    out_file.write(pos)
    for res in distribution[pos]:
        out_file.write("|" + str(res))
    out_file.write("\n")
out_file.close()