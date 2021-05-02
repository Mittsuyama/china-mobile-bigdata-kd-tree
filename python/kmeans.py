# import
from sklearn.cluster import KMeans
import numpy as np
import math
import matplotlib.pyplot as plt

# init & const var
DRAW_INERTIA = 0
N_CLUSTERS = 10
lng_lat = []
data = []
lines = open("../data/poi_type.txt", "r").readlines()

# define function
def sse_draw(data):
    print("drawing plot...")
    K_RANGE = 15
    sse_list = []
    for k in range(1, K_RANGE):
        est = KMeans(n_clusters=k, init="k-means++")
        est.fit(np.array(data))
        sse_list.append(est.inertia_)

    x_list = range(1, K_RANGE)
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(x_list, sse_list, 'o-')
    plt.show()

# main
## read file
print("reading file...")
for line in lines:
    split_result = line.replace("\n", "").split("|")
    lng_lat.append(split_result[0])
    lst = split_result[1:]
    tmp = []
    count = 0.0
    for item in lst:
        count += float(item)
    for item in lst:
        tmp.append(math.log10((float(item) / count) * 9 + 1))
    data.append(tmp)

if DRAW_INERTIA == 1:
    sse_draw(data)

## kmeans
print("running k-means...")
est = KMeans(n_clusters=N_CLUSTERS, init="k-means++")
result = est.fit_predict(np.array(data))

## print output
out_file = open("../data/keams_result.txt", "w")
csv_file = open("../data/keams_result.csv", "w")

out_file.write("var data=[")

count = 0
for index in range(0, len(lng_lat)):
    out_file.write("[{},{}],".format(lng_lat[index], result[index]))
    csv_file.write("{},{}\n".format(lng_lat[index], result[index]))
    count += 1

print("district count: " + str(count))

out_file.write("];")
out_file.close()
csv_file.close()
