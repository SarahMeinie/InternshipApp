# Yelp Restaurant Recommender 


<img src="https://imgur.com/GZ46zUM.png" width="100">


Use the Yelp dataset to develop a web application that will make restaurant
recommendations. The recommendations will be based off of criteria specified
by the user. This criteria is: Cuisine served at the restaurant, the city that
the restaurant is located in, the day and time that the user would like to
visit the restaurant.


### How to run the code locally:
0. Open the folder src/neo4j and follow the README. This will set up the database and populate it with the data from src/dataset 

1. Setup a virtual environment, using the requirements.txt provided:\
1.1 If you have not already, install virtualenv:
```bash
sudo pip3 install virtualenv
``` 

1.2 Now, create a virtual environment: In the main directory type:
```bash
virtualenv venv
``` 

1.3 Lastly activate your virtual environment:
```bash
source venv/bin/activate
``` 

2. Connect to the neo4j database with the following details:\
username: neo4j\
password: YourPassword
3. Use the python3 to run the main file.

```bash
python3 main.py
``` 
4. Follow the link to the website produced

## Submission Resources
- [Live Website Server](http://167.99.89.23:5000)
- Video walk-through of app available at [Video Link](https://youtu.be/3QvssOyfHdM)






