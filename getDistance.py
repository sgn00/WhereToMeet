from math import sin, cos, sqrt, atan2, radians

def getDistance(lat1, lon1, lat2, lon2):    
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


# return a list of addresses of top k closest mrt stations around
def getTopKClosest(location_dict, df, k_closest):
    station_lst = []
    output_lst = []
    for i, row in df.iterrows():
        lat = float(row[2])
        lon = float(row[3])
        dist_lst = []
        for location in location_dict.values():
            distance = getDistance(location[0], location[1], lat, lon)
            dist_lst.append(distance)
        max_dist = max(dist_lst)
        tup = (row[0], max_dist)
        station_lst.append(tup)
    station_lst.sort(key=lambda tup: tup[1])
    for i in range(k_closest):
        output_lst.append(station_lst[i][0])
    return output_lst


# return a dictionary of k closest MRT stations with distance to each user

def getTopKClosestDistance(location_dict, df, k_closest):
    output_dic = {}
    station_lst = []
    output_lst = []
    for i, row in df.iterrows():
        lat = float(row[2])
        lon = float(row[3])
        dist_lst = []
        for location in location_dict.values():
            distance = getDistance(location[0], location[1], lat, lon)
            dist_lst.append(distance)
        max_dist = max(dist_lst)
        tup = (row[0], max_dist, row[2], row[3])
        station_lst.append(tup)
    station_lst.sort(key=lambda tup: tup[1])
    for i in range(k_closest):
        output_lst.append([station_lst[i][0], station_lst[i][2], station_lst[i][3]])
        output_dic[station_lst[i][0]] = []
        for j in location_dict:
            output_dic[station_lst[i][0]].append((j, getDistance(location_dict[j][0], location_dict[j][1], output_lst[i][1], output_lst[i][2])))
    return output_dic