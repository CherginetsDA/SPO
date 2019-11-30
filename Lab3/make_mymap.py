#!/usr/bin/env python3
from IPython.display import HTML, display
import folium
import json
import os
import webbrowser

regions_coords = [59.9749, 30.4715]

mapS = folium.Map(location=regions_coords)

regions_json_file = open('./data_map.geojson')
regions_json = json.load(regions_json_file)

clear_features=[]
for reg in regions_json["features"]:
    prop = reg["properties"]
    if "is_in:city" in prop:
        if prop["is_in:city"]=='Санкт-Петербург':
            clear_features.append(reg)
    regions_json["features"] = clear_features



folium.GeoJson(
    regions_json,
    name='all'
).add_to(mapS)

folium.Marker([59.936638, 30.498124], popup='<i>УИК_1023 Информация_по_УИК: Число_избирателей:2042 Явка:47%</i>', tooltip="УИК 1023").add_to(mapS)
folium.Marker([59.937057, 30.492449], popup='<i>УИК 1022 Информация_по_УИК: Число_избирателей:2083 Явка:33%</i>', tooltip="УИК 1022").add_to(mapS)
folium.Marker([59.937318, 30.486342], popup='<i>УИК 1011 Информация_по_УИК: Число_избирателей:1174 Явка:31%</i>', tooltip="УИК 1011").add_to(mapS)
folium.Marker([59.937795, 30.479980], popup='<i>УИК 1008 Информация_по_УИК: Число_избирателей:2232 Явка:42%</i>', tooltip="УИК 1008").add_to(mapS)
folium.Marker([59.942234, 30.480497], popup='<i>УИК 1002 Информация_по_УИК: Число_избирателей:1162 Явка:36%</i>', tooltip="УИК 1002").add_to(mapS)
folium.Marker([59.943158, 30.486232], popup='<i>УИК 1005 Информация_по_УИК: Число_избирателей:2334 Явка:33%</i>', tooltip="УИК 1005").add_to(mapS)
folium.Marker([59.941664, 30.492336], popup='<i>УИК 1014 Информация_по_УИК: Число_избирателей:1882 Явка:51%</i>', tooltip="УИК 1014").add_to(mapS)
folium.Marker([59.943496, 30.499942], popup='<i>УИК 1018 Информация_по_УИК: Число_избирателей:2172 Явка:20%</i>', tooltip="УИК 1018").add_to(mapS)
folium.Marker([59.947379, 30.481896], popup='<i>УИК 998 Информация_по_УИК: Число_избирателей:849 Явка:63%</i>', tooltip="УИК 998").add_to(mapS)
folium.Marker([59.952234, 30.479657], popup='<i>УИК 996 Информация_по_УИК: Число_избирателей:1564 Явка:40%</i>', tooltip="УИК 996").add_to(mapS)
folium.Marker([59.954867, 30.478928], popup='<i>УИК 992 Информация_по_УИК: Число_избирателей:1785 Явка:26%</i>', tooltip="УИК 992").add_to(mapS)
folium.Marker([59.948349, 30.466545], popup='<i>УИК 981 Информация_по_УИК: Число_избирателей:1121 Явка:36%</i>', tooltip="УИК 981").add_to(mapS)
folium.Marker([59.951935, 30.465329], popup='<i>УИК 976 Информация_по_УИК: Число_избирателей:1354 Явка:31%</i>', tooltip="УИК 976").add_to(mapS)
folium.Marker([59.952999, 30.465074], popup='<i>УИК 974 Информация_по_УИК: Число_избирателей:1953 Явка:41%</i>', tooltip="УИК 974").add_to(mapS)
folium.Marker([59.947848, 30.485198], popup='<i>УИК 1001 Информация_по_УИК: Число_избирателей:2275 Явка:32%</i>', tooltip="УИК 1001").add_to(mapS)
folium.Marker([59.956050, 30.472610], popup='<i>УИК 989 Информация_по_УИК: Число_избирателей:2354 Явка:38%</i>', tooltip="УИК 989").add_to(mapS)


folium.LayerControl().add_to(mapS)
mapS.save("mymap.html")
