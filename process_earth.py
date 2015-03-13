## Make earth (in WGS84, then we reproject to use as a clipping bound)

import csv

points = 180

with open('earth.csv', 'wb') as output:
    earth = {}
    earth['id'] = 'earth'
    earth['WKT'] = 'POLYGON((' + ', '.join(['-180 ' + str(-90 + (i * 180)/points) for i in range(points+1)]) + ', ' + ', '.join(['180 ' + str(90 - (i * 180)/points) for i in range(points+1)]) + ', ' + '-180 -90' + '))'
    print earth
    print earth.keys()
    writer = csv.DictWriter(output, earth.keys(), delimiter=';')
    writer.writeheader()
    writer.writerows([earth])
