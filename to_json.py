# Copyright 2019 Eye OF Horus
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# http://www.apache.\org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from lxml import etree
import json, sys

tree = etree.parse("doc.kml")

def recursive_dict(element):
    return element.tag, \
        dict(map(recursive_dict, element)) or element.text

all_points = []

color_codes = {"Active Satellites": 0, "Inactive Satellites": 1, "Debris": 2}

for folder in tree.findall('.//Folder'):
    group_name = folder.find('.//name').text

    if group_name not in color_codes.keys():
        continue

    group_number = color_codes[group_name]

    points = []

    for placemark in folder.findall('.//Placemark'):
        name = placemark.find('.//name').text
        coords = placemark.find('.//Point/coordinates').text

        lon, lat, alt = map(float, coords.split(','))

        points.append(lat)
        points.append(lon)
        points.append(alt)
        points.append(group_number)

    all_points.extend(points)

# Earth's radius in meters
earth_radius = 6378100.0

for i in xrange(2, len(all_points), 4):
    all_points[i] = float(all_points[i]) / (earth_radius)

print json.dumps(all_points)
