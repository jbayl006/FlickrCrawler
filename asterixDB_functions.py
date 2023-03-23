from asterixDB_python import AsterixConnection
#import asterixdb_python

def createDB():
    asterix_conn = AsterixConnection()

    asterix_conn.query(f'''
        DROP dataverse metadata IF EXISTS;
        create dataverse metadata;
        use metadata;

        create type metadata_type as {{
        
        id: int,
        url: string,
        views: int,
        keywords: string,
        tags: string,
        favorites: int,
        comments: int,
        name: string,
        description: string,
        locality: string,
        region: string,
        country: string,
        neighbourhood: string,
        download_time: string
          }};
        
        create dataset metadata_set (metadata_type) primary key id;
          
    
    ''')



def checkPhotoExists (id):
    asterix_conn = AsterixConnection()
    response = asterix_conn.query(f'''
        use metadata;
        FROM metadata_set d
        WHERE d.id = {id}
        select *;  ''')

    #print(len(response.results))
    return (len(response.results))

def uploadFile (file):
    asterix_conn = AsterixConnection()

    asterix_conn.query(f'''
    use metadata;

    load dataset metadata_set using localfs
      (("path"="127.0.0.1:///Users/juliabayless/Desktop/Flickr Crawler/Crawler for Local/{file}"),
      ("format"="json"),
      ("delimiter"=","),
      ("NULL"=""));  ''')
    
    #print(response.results)

def insertRecord(record):
    asterix_conn = AsterixConnection()
    asterix_conn.query(f'''
    use metadata;
        INSERT INTO metadata_set
        ({record});
     
    ''')



def getlocation(lat, long):
    asterix_conn = AsterixConnection()
    response = asterix_conn.query(f'''

    st_make_point({lat}, {long});
     
    ''')
    print(response)
def insertdate(date):
    asterix_conn = AsterixConnection()
    response = asterix_conn.query(f'''
    datetime('{date})
    ''')
    print(response)
if __name__ == '__main__':
    #uploadFile("data_Dog")
    record = "[{'url': 'https://live.staticflickr.com/65535/5338762379_6b105a8f9b_c.jpg', 'views': 239518, 'keywords': 'Dog', 'favorites': 139, 'comments': 162, 'name': '5338762379.jpg', 'id': 5338762379, 'tags': 'dog', 'description': 'Dog            ', 'locality': 'St. Petersburg', 'region': 'Florida', 'country': 'United States', 'neighbourhood': '', 'latitude': '', 'longitude': '', 'download_time': '02/21/2023 11:40:15'}]"
    createDB()
    #uploadFile("test.json")
    #insertRecord(record)
    #checkPhotoExists(33336453970)
    #checkPhotoExists(5338762379)
    getlocation(71,30)
