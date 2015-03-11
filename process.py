## Meant for processing MODIS metadata produced by scrape.py

import csv
import sys

file = sys.argv[1]

delimiter = ','
name_addition = '_process'
if len(sys.argv) > 2:
    if sys.argv[2] == 'qgis':
        delimiter = ';'
        name_addition = '_qgis'

bounds = ['lowerLeftCorner','upperLeftCorner','upperRightCorner','lowerRightCorner']

with open(file,'rU') as open_file:
    with open(file.replace('.csv', '') + name_addition + '.csv','wb') as output:
        reader = csv.DictReader(open_file)
        to_write = []
        for row in reader:
            lat_temp = 0
            lon_temp = 0

            lon_extent = [float(row[bound + 'Longitude']) for bound in bounds]

            ### Make a scene centroid.
            ## latitude first
            for bound in bounds:
                lat_temp += float(row[bound + 'Latitude'])

            row['sceneCenterLatitude'] = lat_temp / len(bounds)

            signs = [cmp(float(row[bound + 'Longitude']),0) for bound in bounds]

            ## next longitudes
            # easy case first
            if 300 > max(lon_extent) - min(lon_extent):

                for bound in bounds:
                    lon_temp += float(row[bound + 'Longitude'])
                row['sceneCenterLongitude'] = lon_temp / len(bounds)

            # handle edge cases
            else:
                # this means one corner needs to be temporarily shifted by 360 degrees to calculate the center
                # print max(lon_extent) - min(lon_extent), row['HorizontalTile'], row['VerticalTile'], '\n', lon_extent
                signs = [cmp(float(row[bound + 'Longitude']),0) for bound in bounds]
                # store the odd man out as temp and recalculate the center
                # else is handles the negative case
                if (sum(signs) > 0):
                    temp = float(row[[bound + 'Longitude' for bound in bounds if float(row[bound + 'Longitude']) < 0][0]]) + 360
                    in_bounds = [bound for bound in bounds if float(row[bound + 'Longitude']) > 0]
                    for bound in in_bounds:
                        lon_temp += float(row[bound + 'Longitude'])
                    row['sceneCenterLongitude'] = (lon_temp + temp) / len(bounds)
                else:
                    temp = float(row[[bound + 'Longitude' for bound in bounds if float(row[bound + 'Longitude']) > 0][0]]) - 360
                    in_bounds = [bound for bound in bounds if float(row[bound + 'Longitude']) < 0]
                    for bound in in_bounds:
                        lon_temp += float(row[bound + 'Longitude'])
                    row['sceneCenterLongitude'] = (lon_temp + temp) / len(bounds)

            ## for QGIS
            if name_addition == '_qgis':
                row['WKT'] = 'POLYGON((' + ', '.join([row[bound + 'Longitude'] + ' ' + row[bound + 'Latitude'] for bound in bounds]) + ', ' + row[bounds[0] + 'Longitude'] + ' ' + row[bounds[0] + 'Latitude'] + '))'

            to_write.append(row)

        writer = csv.DictWriter(output, to_write[0].keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(to_write)
