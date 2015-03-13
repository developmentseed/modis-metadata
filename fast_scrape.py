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
        one_file = {}
        one_file['File Name'] = scene.replace('.xml','')
        one_file['Date'] = process_date
        one_file['Tile'] = scene.split('.')[2]

        metadata.append(one_file)

    keys = metadata[0].keys()
    date_format2 = str(process_date.year) + "-" + str(process_date.month) + "-" + str(process_date.day)
    with open(date_format2 + '_modis_fast.csv','wb') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(metadata)

    ## increment day
    process_date += datetime.timedelta(days=1)
