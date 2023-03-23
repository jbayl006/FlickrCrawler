# FlickrCrawler
Data crawler for Flickr that searches for photos based on keywords in keywords.txt

Uploads the information crawled about the photos into the database AsterixDB. 

The information includes id, url, view count, keywords, tags, favorites count, comment count, name, description, locality, region, country, neighbourhood, and download_time

To run file run the command:
python flickrGetData.py keywords.txt  

Make sure to have asterixDB running on localhost:19006
