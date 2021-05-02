# program init
DECIMAL_COUNT = 3
pos_dict = {}

# read file
lines = open("../data/poi.txt", "r").readlines()
for line in lines:
    split_reuslt = line.split(",")
    if len(split_reuslt) >= 5:
        try:
            lng = float(split_reuslt[5])
            lat = float(split_reuslt[6])
            if 126.48 < lng < 126.83 and 45.64 < lat < 45.86:
                lng = round(lng, DECIMAL_COUNT)
                lat = round(lat, DECIMAL_COUNT)
                count = 0
                if lng in pos_dict:
                    if lat in pos_dict[lng]:
                        count = pos_dict[lng][lat]
                count += 1
                if lng in pos_dict:
                    pos_dict[lng].update({ lat: count })
                else:
                    pos_dict.update({ lng : { lat: count } })
        except:
            pass

# write to file
out_file = open("../data/heat_data.js", "w")
out_file.write("var poi_list=[")


start = True
for lng in pos_dict:
    for lat in pos_dict[lng]:
        if not start:
            out_file.write(",")
        else:
            start = False
        out_file.write("{{lng:{},lat:{},count:{}}}".format(lng, lat, str(pos_dict[lng][lat] / 3)))

out_file.write("];")
out_file.close()
