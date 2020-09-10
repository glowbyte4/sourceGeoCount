import json
from geopy.distance import geodesic
#lat long
north_zapad = (55.913006885343325, 37.37426023632813)
north_vostok = (55.913006885343325, 37.852805890625014)
south_vostok = (55.54821795443864, 37.852805890625014)
south_zapad = (55.54821795443864, 37.37426023632813)
#координаты москвы #55.732133, 37.374284 запад #55.745218, 37.840778 восток #55.570642, 37.665142 юг #55.913005, 37.567413 север
stores = open("stores.json", 'r')
stores_dict = json.loads(stores.read())

buildings = open("build2.json", 'r')
buildings_dict = json.loads(buildings.read())

metro = open("moscow_metro.json", 'r')
metro_dict = json.loads(metro.read())


def calc_delta(delta_meters=500):
    all_dist_long = geodesic(north_zapad, north_vostok).meters
    all_dist_lat = geodesic(north_zapad, south_vostok).meters
    delta_long = (north_vostok[1] - north_zapad[1]) * delta_meters / all_dist_long
    delta_lat = (north_zapad[0] - south_zapad[0]) * delta_meters / all_dist_lat
    return delta_lat, delta_long


delta_lat, delta_long = calc_delta()


def get_competitors(n_w, n_e, s_w, s_e, data):
    res = 0
    for item in data:
        cur_coord = data[item]
        if ((n_w[1] < cur_coord['geometry.location.lng']) and (n_e[1] > cur_coord['geometry.location.lng']) and
                (n_e[0] > cur_coord['geometry.location.lat']) and (s_w[0] < cur_coord['geometry.location.lat'])):
            res += 1
    return res


def get_buildings(n_w, n_e, s_w, s_e, data):
    res = 0
    for item in data:
        cur_coord = item
        if ((n_w[1] < cur_coord['center_lng']) and (n_e[1] > cur_coord['center_lng']) and
                (n_e[0] > cur_coord['center_lat']) and (s_w[0] < cur_coord['center_lat'])):
            res += 1
    return res


def min_metro_dist(coord):
    dist = 100000
    lines = metro_dict['lines']
    for line in lines:
        stations = line['stations']
        for station in stations:
            c_dist = geodesic(coord, (station['lat'], station['lng'])).meters
            if c_dist < dist:
                dist = c_dist
    return dist


def calc_weight(comp, build, metro_dis):
    weight = build / (comp * 5 + 1)
    if metro_dis < 300:
        weight *= 3
    elif metro_dis < 600:
        weight *= 2
    return weight

#print(get_competitors(north_zapad, north_vostok, south_zapad, south_vostok, stores_dict))
#print(get_buildings(north_zapad, north_vostok, south_zapad, south_vostok, buildings_dict))
max_weight = 0
result = []
sum_com = 0
sum_build = 0
start_long = north_zapad[1]
end_long = north_vostok[1]
i = 0
while start_long < end_long:

    start_lat = south_zapad[0]
    end_lat = north_vostok[0]
    j = 0
    while start_lat < end_lat:
        #here
        #print(start_lat, start_long)
        s_w = (start_lat, start_long)
        s_e = (start_lat, start_long + delta_long)
        n_w = (start_lat + delta_lat, start_long)
        n_e = (start_lat + delta_lat, start_long + delta_long)
        center = ((n_e[0] + s_w[0]) / 2, (n_e[1] + s_w[1]) / 2)
        cur_com = (get_competitors(n_w, n_e, s_w, s_e, stores_dict))
        cur_build = (get_buildings(n_w, n_e, s_w, s_e, buildings_dict))
        metro_dist = min_metro_dist(center)
        weight = calc_weight(comp=cur_com, build=cur_build, metro_dis=metro_dist)
        if (weight > max_weight):
            max_weight = weight
        square = {
            's_w': s_w,
            's_e': s_e,
            'n_w': n_w,
            'n_e': n_e,
            'center': center,
            'competitors': cur_com,
            'buildings': cur_build,
            'metro_dist': metro_dist,
            'weight': weight,
        }
        result.append(square)
        sum_build += cur_build
        sum_com += cur_com
       # print(cur_com, cur_build, metro_dist)
        start_lat += delta_lat
        j += 1
    start_long += delta_long
    i += 1
print(sum_com)
print(sum_build)
print(max_weight)
fout = open('result.json', 'w')
fout.write(json.dumps(result))
fout.close()

#print(geodesic(north_east, north_west).meters)
#print(geodesic(north_east, south_east).meters)
#print(delta_lat, delta_long)
