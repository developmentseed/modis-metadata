import requests
from bs4 import BeautifulSoup
import re
import csv
import datetime
import sys

start_date = datetime.datetime(2015, 1, 1, 0, 0)
end_date = datetime.datetime.now()

if len(sys.argv) > 1:
    start_date = sys.argv[1]
if len(sys.argv) > 2:
    end_date = sys.argv[2]

bounds = ['lowerLeftCorner','upperLeftCorner','upperRightCorner','lowerRightCorner']
### MODIS
# 36 Horizontal Tiles, 18 Vertical (10x10 degrees at the equator)
# 460 Total Scenes (not all combinations are possible)
# It's hard to figure out file names programmatically because they are based on the timestamp that it was processed
# So go to the date pages and just start grabbing

process_date = start_date
while (str(process_date.year) + "-" + str(process_date.month) + "-" + str(process_date.day)) < (str(end_date.year) + "-" + str(end_date.month) + "-" + str(end_date.day)):
    date_formatted = str(process_date.year) + "." + str(process_date.month).zfill(2) + "." + str(process_date.day).zfill(2)
    print "Date: " + date_formatted
    page = requests.get("http://e4ftl01.cr.usgs.gov//MODIS_Dailies_A/MOLT/MOD09GA.005/" + date_formatted)
    page_soup = BeautifulSoup(page.text)
    scene_list = []
    for a in page_soup.findAll('a',text=re.compile("xml")):
        scene_list.append(a.text)

    print "Going after " + str(len(scene_list)) + " scenes"

    metadata = []
    for scene in scene_list:
        ## get a url
        print "Getting scene " + scene
        r = requests.get("http://e4ftl01.cr.usgs.gov//MODIS_Dailies_A/MOLT/MOD09GA.005/" + date_formatted + "/" + scene)

        ## make into a soup object
        soup = BeautifulSoup(r.text, 'xml')

        ## find the things we want and store them on our dict
        one_file = {}
        one_file['File Name'] = soup.find('DistributedFileName').text
        one_file['File Size'] = soup.find('FileSize').text
        one_file['Platform'] = soup.find('PlatformShortName').text
        one_file['DayNightFlag'] = soup.find('DayNightFlag').text
        one_file['RangeEndingTime'] = soup.find('RangeEndingTime').text
        one_file['RangeEndingDate'] = soup.find('RangeEndingDate').text
        one_file['RangeBeginningTime'] = soup.find('RangeBeginningTime').text
        one_file['RangeBeginningDate'] = soup.find('RangeBeginningDate').text

        ## Appears that bounds are always in the order: bottom left, top left, top right, bottom right
        for index, point in enumerate(soup.find('GPolygon').find('Boundary').find_all('Point')):
            for inner_index, child in enumerate(point.findAll(True)):
                if inner_index == 0:
                    one_file[bounds[index] + 'Longitude'] = float(child.text)
                else:
                    one_file[bounds[index] + 'Latitude'] = float(child.text)

        one_file['HorizontalTile'] = soup.find("PSAName", text="HORIZONTALTILENUMBER").next_sibling.next_sibling.text
        one_file['VerticalTile'] = soup.find("PSAName", text="VERTICALTILENUMBER").next_sibling.next_sibling.text
        one_file['TileID'] = soup.find("PSAName", text="TileID").next_sibling.next_sibling.text

        metadata.append(one_file)

    keys = metadata[0].keys()
    date_format2 = str(process_date.year) + "-" + str(process_date.month) + "-" + str(process_date.day)
    with open(date_format2 + '_modis.csv','wb') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(metadata)

    ## increment day
    process_date += datetime.timedelta(days=1)
