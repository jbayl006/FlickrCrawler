def crawlFlickr(keywords):
    createDB()
    #uploadFile("test.json")
    #print("inside crawlFLickr")
    dataKeywords = []
    
    for keyword in keywords:
        print("Current Point is:")
        print(keyword)
        photos = []
        time.sleep(5)
        now=datetime.now()
        minUploadDate = now.strftime("%m/%d/%Y %H:%M:%S")
        for eachPoint in dataKeywords:
            if(eachPoint['keywords']==keyword):
                minUploadDate = eachPoint["download_time"]

       
        try:
            photos = flickr.walk(text=keyword,
                         tag_mode='all',
                         extras='views, url_c, comments, favorites, tags',          # may be you can try different numbers..
                         sort='relevance',
                         has_geo = '1')
        #min_upload_date = minUploadDate
        except flickrapi.exceptions.FlickrError as e:
            print("Caught an Exception in Location:!")
            print(keyword)
            raise Error(e)
            print(e)
	  
        comments=0
        countPhotos=0

        for i, photo in enumerate(photos):
            
            id = int(photo.get('id'))
            idExists=checkPhotoExists(id)
            #check if the ID already exists in the json
            for eachPoint in dataKeywords:
                if(eachPoint["id"]==id):
                    idExists=1

            #if id does not exist, go ahead
            if(idExists==0):
                pair = {}
                #to make sure we have the json format intact, even if an exception occurs in the middle
                pair["url"]=""
                pair["views"]=""
                pair["keywords"]=""
                pair["favorites"]=""
                pair["comments"]=""
                pair["name"]=""
                pair["id"]=""
                pair["tags"]=[]
               # pair["localId"]=""
                pair["description"] = ""
                pair["locality"]=""
                pair["region"]=""
                pair["country"] = ""
                pair["neighbourhood"] = ""
                pair["latitude"]=""
                pair["longitude"]=""
                pair["location"] = ""
                url = photo.get('url_c')
                name = ""
                tags = photo.get('tags')
                #get views, favorites, description, comments and location(locality, region, neighborhood, country)
                views = int(photo.get('views'))
                favorites = flickr.photos_getFavorites(photo_id=id)
                desc = FlickrLib.get_descripttion(id)
                location = FlickrLibLoc.get_location(id)
                countfaves=int(favorites.find('photo').get('total'))
                
                comments=flickr.photos_comments_getList(photo_id=id)
                countcomments=len(comments.findall('.//comment'))
                name = str(id)+'.jpg'
                pair["url"]=url
                pair["views"]=views
                pair["favorites"]=countfaves
                pair["comments"]=countcomments
                pair["name"]=name
                pair["id"]=id
                pair["tags"]=tags
                #pair["localId"]=keyword+str(i)
                try:
                    pair["description"] = desc
                    pair["locality"]=location["locality"]
                    pair["region"]=location["region"]
                    pair["country"] = location["country"]
                    pair["neighbourhood"] = location["neighbourhood"]
                    pair["latitude"]=location["latitude"]
                    pair["longitude"]=location["longitude"]
                   # print(getlocation(location["latitude"], location["longitude"]))
                    #pair["location"]= getlocation(location["latitude"], location["longitude"])
                    
                except:
                    print("Caught an Exception in Location:!")
                    print(keyword)
                now=datetime.now()
                dateTime = now.strftime("%Y-%m-%dT%H:%M:%S")
                pair["download_time"] = dateTime
                pair["keywords"] =  keyword
                #print(pair)
                insertRecord(pair)
                print("Record inserted successfully!")
                dataKeywords.append(pair)
                
                

                #insertRecord(dataKeywords)
                with open('data_' + keyword + '.json', 'w') as outfile:
                    #dump collected data in json file
                    json.dump(dataKeywords, outfile)
                #print(keyword+": appended successfully!")
               
                urls.append(pair)
                countPhotos = countPhotos + 1
                # get 20 images per keyword
                if countPhotos > 3:
                    break
        #print(dataKeywords)
        #insertRecord(dataKeywords)


        print("new photos for "+keyword+" are:")
        print(countPhotos)
        # Download image from the url and save it to '<name>.jpg'
        n=len(urls)
        for j in range(0, n):
            if urls[j]['url'] != None:
                urllib.request.urlretrieve(urls[j]["url"], './Photos/' + urls[j]["name"])
                # image = Image.open(urls[j]["name"])
                # saveName = urls[j]["name"]
                # image_path = "/Users/juliabayless/Desktop/Master\'s Project Deliverables Fall 18-2/Crawler for Local/Photos/" + saveName 
                # image.save(image_path, 'JPEG')
            else:
                name = None
                urls[j]["name"]=name
                j=j+1
            
    #print(dataKeywords)    
    #insertRecord(dataKeywords)

    keywords=[]



import flickrapi
import urllib
from PIL import Image
import json
import os
import os.path
from os import path
import time
from datetime import datetime
from xml.dom import minidom
from flickr_lib import *
from getLocation import *
from asterixDB_functions import *
from asterixDB_python import *

# Flickr api access key of Zoama Hassan
flickr=flickrapi.FlickrAPI('cdb5888830de9d064820bbd62bc198af', '24979cce607d1887', cache=True)
#createDB()
#def main():
filename = "keywords.txt"
with open(filename) as file:
    keywords = [line.rstrip() for line in file]
urls = []
try:
    #print("got to crawling flickr")
    #print(keywords)
    crawlFlickr(keywords)
except flickrapi.exceptions.FlickrError as e:
    print("Caught an exception")
    print("running program again")
    crawlFlickr(keywords)
keywords = []
