import json
import random
import requests

#check to see if link exists
def sendRequest(url):
    try:
        page = requests.get(url)

    except Exception as e:
        print("error:", e)
        return False

    # check status code
    if (page.status_code != 200):
        return False

    return True

def get_photos(business_id):
    api_key = 'SSJUm_Z0JtJXXmlcU_JMyLy_XggqnzwUWnI4-h5U09YmryUuIJ1Ml3PC_vMJ2GNH0QPn_4VNNfYq9s6qscS96l8xcYQtQChvZfV2TxE89EFQxW7AGL9tu2qgr_meXnYx'

    photos_dictionary = [json.loads(line) for line in open('./src/datasets/full/photo.json', 'r')]
    photos = []             #all of the photo dictionaries for the given business id
    photo_dict = []         #the list of dictionaries for all the photo urls and their captions
    
    for photo in photos_dictionary:
        if photo['business_id'] == business_id and photo['label'] =='food':
            photos.append(photo)

    for photo in photos:
        url = 'https://s3-media2.fl.yelpcdn.com/bphoto/' + photo['photo_id'] + '/o.jpg'
        if sendRequest(url):
            dict = {
                "url": url,
                "caption": photo['caption']
            }
            photo_dict.append(dict)


    return photo_dict

def get_one(business_id):
    api_key = 'SSJUm_Z0JtJXXmlcU_JMyLy_XggqnzwUWnI4-h5U09YmryUuIJ1Ml3PC_vMJ2GNH0QPn_4VNNfYq9s6qscS96l8xcYQtQChvZfV2TxE89EFQxW7AGL9tu2qgr_meXnYx'

    photos_dictionary = [json.loads(line) for line in open('./src/datasets/full/photo.json', 'r')]
    photo = []     
    
    for item in photos_dictionary:
        if item['business_id'] == business_id and item['label'] =='food':
            url = 'https://s3-media2.fl.yelpcdn.com/bphoto/' + item['photo_id'] + '/o.jpg'
            if sendRequest(url):
                photo = {
                    "url": url,
                    "caption": item['caption']
                    }
                break
            
    return photo        
   
    

def main():
    # TESTING   
    urls = get_photos('G4hjhtA_wQ-tSOGpgGlDjw')

if __name__ == "__main__":
    main()
