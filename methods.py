from src import top_restaurant, nextRestaurants, photos


def get_top(city, category, day, time):
    top = top_restaurant.top_resturant_using_neo4j(city, category, day, time)
    
    if top['Resturant_name'] != None:   
        top['Stars'] = int(top['Stars'])

    return top
    
def get_other(userID, businessID, city, category):
    if userID == None:
        userID = nextRestaurants.bestReviewer(businessID)
    
    other = nextRestaurants.getNext(userID, businessID, city, category)
    
    for rest in other:
        rest['stars'] = round(rest['stars'])
        rest['photo'] = photos.get_photos(rest['id'])
        
    return other
    
