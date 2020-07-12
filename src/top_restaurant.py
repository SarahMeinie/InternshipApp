import json 
from src import photos
import datetime
from datetime import date
import csv

#Return true if x is in the range [start, end]
def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

#print dictionary neatly
def print_dict(dictionary):
    for key in dictionary:
        print(key + ":")
        print(dictionary[key])
        print("")

#find all resturants in the given city and given category
def filter_businesses(businesses, city, category):
    filtered = []
    for business in businesses:
        if business['city'] == city:
            if business['categories'] != None and category in business['categories']:
                filtered.append(business)
    return filtered

#find the resturant (that is open at the given day and time) with the highest rating for stars, using review count as a tie breaker.
def find_top_rated(resturants_hours, day, time, businesses):
    filtered = []
    filtered_no_time = []
    for resturant in resturants_hours:
        hours = resturant['hours']
        if hours != None and day in hours:
            if hours[day] != None and hours[day] != 'None':
                hours1 = hours[day].split('-')
                min_ = (hours1[0]).split(':')
                max_ = (hours1[1]).split(':')

                min_time = datetime.time(int(min_[0]), int(min_[1]), 0)
                max_time = datetime.time(int(max_[0]), int(max_[1]), 0)

                if time_in_range(min_time, max_time, time):
                    #find the resturant with the corrosponding business id
                    for business in businesses:
                        if business['business_id'] == resturant['business_id']:
                            filtered.append(business)
        else:
            for business in businesses:
                        if business['business_id'] == resturant['business_id']:
                            filtered.append(business)

    sort = sorted(filtered, key = lambda kv:(kv['stars'], kv['review_count']), reverse=True)
    if filtered == None or len(filtered) == 0:
        return None
    else:    
        return sort[0]


#find the most useful review of the resturant, using the resturants business id
def useful_reiew(business_id, reviews_json, users, review_texts):
    reviews = []
    today = date.today()
    twoyearsago = date(today.year - 2, today.month, today.day)

    for review in reviews_json:
        reviewdate = date(int(review['date'][0:4]), int(review['date'][5:7]), int(review['date'][8:10]))
        if reviewdate >= twoyearsago: 
            if review['business_id'] == business_id:
                reviews.append(review)  
                    
    if len(reviews) > 0:
        #find the most recent and most useful review from the last two years
        sorted_reviews = sorted(reviews, key = lambda kv:(kv['useful'], kv['date']), reverse=True)
        useful = sorted_reviews[0]

        #if there has been a review in the last 2 years
        for user in users:
            if user['user_id'] == useful['user_id']:
                review_user = user
                #find review text 
                most_useful_review = {
                    "Most Useful Review Author": review_user['name'],
                    "Stars of most useful review": int(useful['stars']),
                    "Most Useful Review": None,
                    "usID": useful['user_id']
                }
                break

        for review_text in review_texts:
            if useful['review_id'] == review_text['review_id']:
                most_useful_review["Most Useful Review"] = review_text['text']
                break
    else:
        #if there haven't been any reviews in the last 2 years
        most_useful_review = {
                    "Most Useful Review Author": None,
                    "Stars of most useful review": None,
                    "Most Useful Review": "There haven't been any reviews in the last two years",
                    "usID": None
                }
        
    return most_useful_review
#using all of the above functions to compile a dictionary containing all of the required info to send to front end
def top_resturant_using_neo4j(city, category, day, time):
    time_split = time.split(":")
    time_hour = int(time_split[0])
    time_min = int(time_split[1])
    time = datetime.time(time_hour, time_min, 0)

    #Assuming the .json files are stored in a folder called yelp-dataset. This can be changed later.
    business_path = './src/datasets/sub/business_sub.json'
    review_path = './src/datasets/sub/review_sub.json'
    user_path = './src/datasets/sub/user_sub.json'
    business_hours_path = './src/datasets/sub/business_hours.json'
    reviews_text_path = './src/datasets/sub/review_text.json'

    resturants = []
    reviews = []
    users = []
    hours = []
    reviews_text = []

    with open(business_path) as f:
        resturants = json.load(f)
    with open(review_path) as f:
        reviews = json.load(f)
    with open(user_path) as f:
        users = json.load(f)
    with open(business_hours_path) as f:
        hours = json.load(f)
    with open(reviews_text_path) as f:
        reviews_text = json.load(f)

    resturants = filter_businesses(resturants, city, category)
    top_resturant = find_top_rated(hours, day, time, resturants)
    if top_resturant == None:
          #create dictionary for top resturant
        top_resturant_dict = {
            'Resturant_name': None,
            "Address": None,
            "Stars": None,
            "Review_Count": None,
            "Most Useful Review Author": None,
            "Most Useful Review": None,
            "Photo Urls and captions": None,
            "Stars of most useful review": None,
            "usID": None,
            "busID": None
        }
    else:
        use = useful_reiew(top_resturant['business_id'], reviews, users, reviews_text)
        photo_urls = photos.get_photos(top_resturant['business_id'])

        #create dictionary for top resturant
        top_resturant_dict = {
            'Resturant_name': top_resturant['name'],
            "Address": top_resturant['address'],
            "Stars": top_resturant['stars'],
            "Review_Count": top_resturant['review_count'],
            "Most Useful Review Author": use['Most Useful Review Author'],
            "Most Useful Review": use['Most Useful Review'],
            "Stars of most useful review": use["Stars of most useful review"],
            "Photo Urls and captions": photo_urls,
            "usID": use['usID'],
            "busID": top_resturant['business_id']
        }


    return top_resturant_dict

def main():
    ##################  INPUT/TESTING  #####################
    city = 'Toronto'
    category = 'Seafood'
    day = 'Sunday'
    time = '10:00'                      #in 24 hour format
    #######################################################

    # - USING .JSON
    #top = top_resturant_using_json(city, category, day, time)
    #print_dict(top)

    top = top_resturant_using_neo4j(city, category, day, time) 
    print(top)

if __name__ == "__main__":
    main()

