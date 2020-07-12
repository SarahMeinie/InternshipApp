from operator import itemgetter
from py2neo import Graph

uri ="bolt://localhost:8000/"

graph = Graph(uri, auth=('neo4j', 'Phillip1014')) #access to the neo4j database

def getFriendList(userID):
    #makes list of friends(id) and list of friends of friends(id)
    listOfFriends=graph.evaluate("MATCH (n:User)-[r:FRIEND]->(b:User) WHERE n.id='" + userID + "' RETURN COLLECT(b.id)")
    completeListOfFriends=[]
    for d in listOfFriends:
        friendsDictionary={}
        friendsDictionary["id"]=d
        friendsDictionary["reviewCount"]=graph.evaluate("MATCH (n:User)-[r:REVIEWS]->() WHERE n.id='" + d + "'  RETURN COUNT(r)")
        completeListOfFriends.append(friendsDictionary)
        listOfFriendsOfFriends=graph.evaluate("MATCH (n:User)-[r:FRIEND]->(b:User) WHERE n.id='" + d + "' RETURN COLLECT(b.id)")
        #now to list friend of friends
        for x in listOfFriendsOfFriends:
            friendsDictionary={}
            friendsDictionary["id"]=x
            friendsDictionary["reviewCount"]=graph.evaluate("MATCH (n:User)-[r:REVIEWS]->() WHERE n.id='" + x + "'  RETURN COUNT(r)")
            completeListOfFriends.append(friendsDictionary)
    #Sorts the list from highest review count to lowest
    completeListOfFriends =sorted(completeListOfFriends, key=lambda k: k['reviewCount'], reverse=True)
    #removes duplicate friends
    seen = set()
    completeListOfFriendsSorted = []
    for d in completeListOfFriends:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            completeListOfFriendsSorted.append(d)
    #return first 50 dictionaries
    return completeListOfFriendsSorted[:50]
