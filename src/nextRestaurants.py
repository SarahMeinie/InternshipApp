from py2neo import Graph
import importlib.util
from src import friendsList

'''

FUNCTION getNext
INPUTS
 - userID of most useful review
 - businessID of top review
 - city
 - category
OUTPUT
 - list of 5 recommended restaurants (each restaurant a dict with keys business_id, name, stars, address)
'''
def getNext(userID, busID, city, category):  
    # access the Neo4j database
    uri ="bolt://167.99.89.23:8000/"
    graph = Graph(uri, auth=('neo4j', 'YourPassword')) 
    
    top_user = {"id" : userID}

    listOfFriends = getFriends(userID)
    if listOfFriends == None:
        return 'No recommendations can be made based on similar users'
    else:
        listOfFriends.append(top_user) # adds top reviewer to list
        
        # find businesses that match specifications
        matches = set() # sets contain only unique values
        for user in listOfFriends:
            businesses = graph.evaluate("MATCH (:User {id: '" + user["id"] + "'})-[:REVIEWS]->(b:Business {city: '" + city + "'})-[:IN_CATEGORY]->(:Category {id: '" + category + "'}) WHERE NOT b.id = '" + busID + "' RETURN COLLECT(b)")
            matches.update(businesses)
            
        print('got others')

        if matches == None:
            return 'There are no other restaurants that match the given criteria'
        else:
            # sort restaurants: primary sort on stars and secondary sort on review count  
            restaurants_sorted = sorted(matches, key = lambda k: (k['stars'],k['review_count']), reverse=True)
            return restaurants_sorted[:5]

def getFriends(userID):
    uri ="bolt://167.99.89.23:8000/"
    graph = Graph(uri, auth=('neo4j', 'YourPassword')) 
    
    friends = set()
    f = graph.evaluate("MATCH (:User {id:'" + userID + "'})-[:FRIEND]->(a:User) "
                       "WITH a.review_count as count, a as user "
                       "WHERE NOT count = 0 "
                       "RETURN COLLECT(user) ")
    friends.update(f)
    fof = graph.evaluate("MATCH (:User {id:'" + userID + "'})-[:FRIEND]->(:User)-[:FRIEND]->(b:User) "
                         "WITH b.review_count as count, b as user "
                         "WHERE NOT count = 0 "
                         "RETURN COLLECT(user)")
    friends.update(fof)
    
    if friends != None:   
        friends_sorted = sorted(friends, key = lambda k: k['review_count'], reverse=True)
        ans = friends_sorted[:50]
    else:
        ans = None
        
    # print(friends_sorted[0])
    
    return ans

def bestReviewer(busID):
    uri ="bolt://167.99.89.23:8000/"
    graph = Graph(uri, auth=('neo4j', 'YourPassword')) 
    
    reviews = graph.evaluate("MATCH (u:User)-[:REVIEWS]->(:Business {id: '" + busID + "'}) RETURN COLLECT(u.id)")
    users = []
    for item in reviews:
        user = {}
        user['id'] = item
        user['useful'] = graph.evaluate("MATCH (:User {id: '" + item + "'})-[r:REVIEWS]->(b:Business {id: '" + busID + "'}) RETURN r.useful")
        users.append(user)
        
    best_user = sorted(users, key = lambda k: (k['useful']), reverse=True)[0]
        
    return best_user['id']
    





def main():
    userID = '2emKfhlaCUzzr1xbI0CM2A'
    busID = 'trKyIRyjKqVSZmcU0AnICQ'
    city = 'Toronto'
    cate = 'Seafood'

    top_5 = getNext(userID, busID, city, cate)
    return top_5

if __name__ == '__main__':
    main()
