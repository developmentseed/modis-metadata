# modis-metadata
scraping and processing MODIS metadata

- [scrape.py](https://github.com/developmentseed/modis-metadata/blob/master/scrape.py): Given specific date ranges, grabs daily MODIS metadata from http://e4ftl01.cr.usgs.gov/MODIS_Dailies_A/
- [process.py](https://github.com/developmentseed/modis-metadata/blob/master/process.py): Process files downloaded from above to add characteristics like scene centroids.
- [populate.js](https://github.com/developmentseed/modis-metadata/blob/master/populate.js): upload the data to an elasticsearch instance. Currently streaming but can be modified to use bulk upload.
