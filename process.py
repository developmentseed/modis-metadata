## Meant for processing MODIS metadata produced by scrape.py
# GeoJSON bounds will be in lon/lat order, we'll switch for the API so it can be easily rendered in Leaflet

import csv
import sys
import fiona

file = sys.argv[1]

delimiter = ';'
name_addition = '_process'

with fiona.drivers():
    with open(file,'rU') as open_file:
        with fiona.open('modisTiles.geojson') as modis:
            with open(file.replace('.csv', '') + name_addition + '.csv','wb') as output:

                reader = csv.DictReader(open_file)
                to_write = []

                ## make a dict from our modis tiles
                # key is h00v00, value is coordinates array
                modis_tiles = {}
                for m in modis:
                    h = str(int(m['properties']['h'])).zfill(2)
                    v = str(int(m['properties']['v'])).zfill(2)
                    modis_tiles['h' + h + 'v' + v] = m['geometry']['coordinates'][0][0]

                print
                for row in reader:
                    lat_temp = 0
                    lon_temp = 0

                    ## find our tile
                    tile = row['File Name'].split('.')[2]
                    bounds = modis_tiles[tile]
                    ### Make a scene centroid.
                    for bound in bounds:
                        lat_temp += bound[1]
                        lon_temp += bound[0]

                    row['sceneCenterLatitude'] = lat_temp / len(bounds)
                    row['sceneCenterLongitude'] = lon_temp / len(bounds)
                    row['boundsArray'] = '[' + ','.join('[' + str(bound[1]) + ',' + str(bound[0]) + ']' for bound in bounds) + ']'
                    row['acquisitionDate'] = str(row['Date']).split(' ')[0]
                    to_write.append(row)

                writer = csv.DictWriter(output, to_write[0].keys(), delimiter=delimiter)
                writer.writeheader()
                writer.writerows(to_write)
