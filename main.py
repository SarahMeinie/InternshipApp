from flask import Flask, render_template, request, flash
from datetime import datetime
import json
import methods

app = Flask(__name__)
# Load the file into memory
with open("./src/datasets/full/restaurant_categories.json", "r") as f:
    data = json.load(f)

with open("./src/datasets/sub/cities.json", "r") as g:
    cities = json.load(g)

@app.route('/', methods = ['POST', 'GET'])
def index() :
    if request.method == 'POST' :
        
        city = request.form['city_input']
        day = request.form['day_input']
        category = request.form['category_input']
        time = request.form['time_input']
        if not day :
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            d = datetime.today().weekday()
            day = days[d]
        if not time :
            t = datetime.now()
            time = t.strftime("%H:%M")

        top = {
            "Resturant_name" : "",
            "Address" : "",
            "Stars" : 0,
            "Review_Count" : 0,
            "Most Useful Review Author" : 0,
            "Most Useful Review" : "",
            "Photo Urls" : [],
            "usID": "",
            "busID": ""
        }
        top = methods.get_top(city, category, day, time)
      
        #print(top)
        if top['Resturant_name'] != None:
            businessID = top['busID']
            userID = top['usID']

            #userID = '2emKfhlaCUzzr1xbI0CM2A'
            #businessID = 'trKyIRyjKqVSZmcU0AnICQ'
            #print_dict(top)
            other = methods.get_other(userID, businessID, city, category)
            print(other)
        else:
            other = None
        
        return render_template('results.html', title='Results', content=top, categories=data, other=other, cities=cities )
        
    else:
        return render_template('front_page.html', title='Home', categories=data, cities=cities)

if __name__ == "__main__" :
    app.run(debug=True)

def print_dict(dict) :
    for key in dict :
        print(key, ": ", dict[key])
