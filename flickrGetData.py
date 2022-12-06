#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## run
## > python flickr_GetUrl.py tag number_of_images_to_attempt_to_download
from flickrapi import FlickrAPI
import pandas as pd
import sys
import csv
import requests
import os
import time
import datetime
from flickr_lib import *
from getLocation import *
#from get_images import put_images
#from get_images import put_metadata

key='9bec5146f2941ea61f3e59594b93c826'
secret='7a12ddf6dc3fedf7'
flickr = FlickrAPI(key, secret)

def put_image(url):
    print("Starting download {} ".format(url))
    try:
        resp=requests.get(url,stream=True)
        path_to_write=os.path.join(os.getcwd(),FILE_NAME.split("_")[0],url.split("/")[-1])
        outfile=open(path_to_write,'wb')
        outfile.write(resp.content)
        outfile.close()
        print("Done downloading {} of {}".format(url[0]+1,len(urls)))
    except:
        print("Failed to download url number {}".format(url[0]))
    t1=time.time()
    print("Done with download, job took {} seconds".format(t1-t0))  

def put_metadata(photo, keyword, flickr): 
    id = photo.get('id')
    pair = {}
    pair["url"]=""
    pair["views"]=""
    pair["keyword"]=""
    pair["favorites"]=""
    pair["comments"]=""
    pair["zoomLevel"]=""
    pair["name"]=""
    pair["id"]=""
    pair["localId"]=""
    pair["description"] = ""
    pair["locality"]=""
    pair["region"]=""
    pair["country"] = ""
    pair["neighbourhood"] = ""
    pair["latitude"]=""
    pair["longitude"]=""
    url = photo.get('url_o')
    name = ""
    #get views, favorites, description, comments and location(locality, region, neighborhood, country)
    views = photo.get('views')
    favorites = flickr.photos_getFavorites(photo_id=id)
    desc = FlickrLib.get_descripttion(id)
    location = FlickrLibLoc.get_location(id)
    countfaves=favorites.find('photo').get('total')
    comments=flickr.photos_comments_getList(photo_id=id)
    countcomments=len(comments.findall('.//comment'))
    name = keyword+str(id)+'.jpg'
    pair["url"]=url
    pair["views"]=views
    pair["favorites"]=countfaves
    pair["comments"]=countcomments
    pair["name"]=name
    pair["id"]=id
    try:
        pair["description"] = desc
        pair["locality"]=location["locality"]
        pair["region"]=location["region"]
        pair["country"] = location["country"]
        pair["neighbourhood"] = location["neighbourhood"]
        pair["latitude"]=location["latitude"]
        pair["longitude"]=location["longitude"]
    except:
        print("Caught an Exception in Location:!")
        print(keyword)
    pair["keyword"] =  keyword
    print(pair)
    return pair
    

def get_urls(keywords, date, MAX_COUNT):
    flickr = FlickrAPI(key, secret)

    for keyword in keywords:    
        photos = flickr.walk(text="dog, pizza",
                                min_upload_date = date,
                                tag_mode='all',
                                tags=keyword,
                                extras='views, url_o, comments, favorites',
                                per_page=50,
                                sort='relevance',
                                has_geo = '1')
                            
        count=0
        urls=[]
        metadata = []

        for photo in photos:
            if count< MAX_COUNT:
                # get URL
                # get Image and save
                # get photo info into object and json.dump to file 

                count=count+1
                print("Fetching url for image number {}".format(count))
                try:
                    url=photo.get('url_o')
                # put_images(url)
                    metadata.append(put_metadata(photo, keyword, flickr))                    
                    print(keyword + ": appended successfully!")
                    urls.append(url)
                except:
                    print("Url for image number {} could not be fetched".format(count))
            
            else:
                print("Done fetching urls, fetched {} urls out of {}".format(len(urls),MAX_COUNT))
                break
        # urls=pd.Series(urls)
        
        # print("Writing out the urls in the current directory")ß
        # urls.to_csv(keyword+"_urls.csv")
        # print("Done!!!")
        with open(keyword  + '_metadata.json', 'w') as outfile:
                json.dump(metadata, outfile)    
def main():
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    date = input("What date do you want? ")
    print("date:" + date)
    MAX_COUNT = input("How many photos do you want? ")
    MAX_COUNT=int(MAX_COUNT)
    print(MAX_COUNT)
    get_urls(lines, date, MAX_COUNT)
    
if __name__=='__main__':
    main()
