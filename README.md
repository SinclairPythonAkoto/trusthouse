# Trust House v. 0.3 #


In this version I will include map the postcodes to a map I will create using `Folium`.

For this to work the way I intend, I will create another table for the longitude & latitude - and give it a *one to one* relationship between the `Address` table and the `Maps` table.

For now, every new postcode is stored in the `Address` table will be linked to the `Maps` table with their latitude & longitude co-ordinates, to user the same coordinates to plot on a generated map.

For each point plotted on the map, I will include information of the address - i.e... street name & postcode. ***Please note that the Folium library is not as accurate as the Google Maps API, so the street names may not always match.  Instead, it will display a property number or the name of the area (in which the building is located). ***

For my next step I will need to calculate the length of the reviews and then add it to the associated address.
The `Address` table will have an additional column - `total reviews`.


### One to One Relationship ###
I created a *One to One* relationship between the `Address` table & the `Maps` table so when we create a new address, the coordinate of the postcode is also stored.
```
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    geo_map = db.relationship('Maps', backref='location', uselist=False)

# One to one
class Maps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.String(15), nullable=False)
    lat = db.Column(db.String(15), nullable=False)
    addres_id = db.Column(db.Integer, db.ForeignKey('address.id'))
```
Let us look how this *One to One* relationship is created. 
In the `Address` table we have created a variable `geo_map` which is a **relationship object**, that points to the `Maps` db model.
Next, we create a name which will be the link between the two models and store it in the `backref` variable (as you can see above).
By setting `backref` to `'location'` we are telling Python that we want to access the `Address` model when we have created an object of the `Maps` model by attaching `. location` then followed by the `Address` class attribute.  It would look something similar to: `Maps.location.street` (to get access to the street of the map's coordinates).
Now we need to add `uselist=False`, to let Python, know that in this relationship we do not want to create a list - *so essentially telling Python that we just want one instance stored in this relationship*.
Finally, to make it all work we need to create a variable in the `Maps` table that will link the coordinates stored to the address in the `Address` table.
We do this by creating a `ForeignKey` and place the `address.id` inside the brackets.  ***The reference to the class & id you are relating to needs to be in lowercase. ***


### One to Many Relationship ###
```
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    geo_map = db.relationship('Maps', backref='location', uselist=False)
    reviews = db.relationship('Review', backref='address')

# One to many
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
```
Above we have a *One to Many* relationship between the `Address` table and the `Review` table.  
This is so that we can create various reviews under a single address. 
As you may have already seen, a ***One to Many*** relationship is remarkably similar to a *One to One* relationship; they have almost identical matching attributes but without the `uselist` variable in the relationship object.
If we look closely at our `reviews` variable within the `Address` table, we can see that the relationship points to the `Review` table and that the `backref` is `'address'` - meaning that this will allow access to obtain the address information for each review made. To do this we invoke the `.address` after the `Review` object, followed by the `Address` attributes e.g. `Review.address.door_num`.
Again, to create the link between the two I will need a `ForeignKey` that will be linked to the `address.id`.

I found this way of navigating through the data extremely helpful as it enables me to split up the data obtained and use it dynamically for when producing the results on the map or returning a JSON response.


### Creating a Map ###
To create the map, I used the `Folium` library - which I installed in my virtual environment.
```
pip install folium
```
I want my map to be fixed around the area of London when the user first opens the map. to do this, I will need to gather the latitude & longitude of a chosen location (I chose 10 Downing Street!).
I create a variable called `map` which will be a `folium.Map` object; inside the parenthesis we will state its location by adding the latitude & longitude, next the type of map (satellite, hybrid, black & white etc) and then how much you would like to zoom in.  Below is a little snippet.
```
location = float(latitude), float(longitude)
map = folium.Map(
    location=location,
    tiles='Stamen Terrain',
    zoom_start=9,
)
```
Now the map has been created, this allows me to get all the coordinates from the `Maps` table and use the same coordinates as plots by running a for loop. 
I have also used the `geopy` library to get the street name by reverse geolocation mapping from each latitude & longitude stored.  *(A list of installation requirements will be provided). *
This will give me the full UK address of the coordinates returned in a single string - which I store in a variable called `street_location`.
Because this is essentially one long string, I used the `street_location.split(',')` in order to split up elements of the address into separate values, stored inside of a list.
Now each element has a *list index*, I can safely say that the **street name** will be the second list object (*list index 1*).  This is what I will use to add as a marker on the map along with each postcode.
To create a marker, I first had to create a for loop to loop through all the stored coordinates in the `Maps` table.
Then I capture the latitude & longitude to get the street name and store it in a list variable called `data`.  Now lastly, I can create the marker by creating a `folium.Marker` object.  Within the object we will include information such as the location, data for the popup, an icon & also text that appears every time the mouse hovers over the icon by using `tooltip`. We complete the creation the marker by adding `.add_to(map)` at the end of the `folium.Marker` object.
Let’s look at a piece of the code below:
```
for geocode in coordinates:
    long = geocode.lon
    lat = geocode.lat
    # Get street name from latitude & longitude
    street_location = geolocator.reverse(f'{lat},{long}')
    street_location = str(street_location)
    data = street_location.split(',')

    # Adding the points to the map
    folium.Marker(
        location=[float(lat), float(long)],
        popup=f'{data[1]}, {geocode.location.postcode.upper()}',
        tooltip='check address',
        icon=folium.Icon(color='red', icon='home', prefix='fa') 
    ).add_to(map)
```
To be able to show the map as a webpage for the class route I had to execute the following for the last line:
```
return map._repr_html()
```


# Trust House v 0.4 #
In this version I will refactor the codebase with **Flask Blueprint**.
***This app is incomplete.***


# Trust House v. 0.4.1 #
In this version I will be refactoring the web app and split it up in a modular layout.  
I will also attempt to reduce the amount of repetition used throughout the codebase.

By combining the [*Flask Documentation*](https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/) on application factories and tutorial by [*Pretty Printed*](https://www.youtube.com/watch?v=WhwU1-DLeVw&t=989s), I was able to reorganise my Flask app.
This allowed me to separate distinct parts of the web app into separate modules, each with separate functionalities, working together to make the app run.
I decided to split the database tables into a module called `models` and created more modules for the web routes & API responses.


### Refactoring: Monolith to Modular ###
To make my refactoring successful, I had to create an `__init__.py` file for every module.
As you can see, the first module is `trusthouse` with an `__init__.py` file.
You may be able to notice one of the differences between this version and the previous version, is that there is no `main.py` file - so you may be wondering where have I created my Flask app?
To answer this, we should look at `trusthouse/__init__.py` - this is where the Flask app is created.
```
from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trusthouse.sqlite3"
app.config["TRACK_MODIFICATIONS"] = True

import trusthouse.routes.welcome_screen
```
In this file we can see that I have not only created my Flask app, but also configured my database (I have used SQLite3 until the app grows, then will think about migrating the db to MYSQL or even AWS).
We import `welcome_screen` from the `routes` module at the bottom of the script to run the file.
In `welcome_screen.py` we can see that we have imported the `app` from the `trusthouse` module.
```
from flask.views import MethodView
from flask import render_template
from ..extensions import app

class LandingPage(MethodView):
    def get(self):
        return render_template('landingPage.html')

app.add_url_rule('/', view_func=LandingPage.as_view(name='landingpage'))
```
As mentioned before, we can see that `welcome_screen.py` depends on the `trusthouse` module and vice versa.  
*This is a ***Circular Import***; circular imports are advised to be avoided as it can cause problems with your code in your app.*
*However, for my scenario, because I want to have the possibility to easily extend my app, I will use this design pattern as recommended by the Flask documentation. *


### Setup.py ###
If we try to run our file now you will see it will not work.
This is because Python is *stopping us from setting up a module as a start-up file*.
We can avoid our code from breaking by creating a file called `setup.py` in the *parent directory*.
```
from setuptools import setup

setup(
    name='trusthouse',
    packages=['trusthouse'],
    include_package_data=True,
    install_requires=[
        'flask',
    ]
)
```
The app is not yet ready to run, I will build the database tables first then go through the final steps of running the app. 


### Setting Up the Database Tables ###
To set up the database tables I created the `models` module, then made each database table a separate Python file.  
This is in case I wish to make changes I can selectively alter the app without having to change rest of the code.

Because my code base is no longer all in one monolithic file, and rather now set up in modules, I created a file called `extensions` in the `trusthouse` directory to create by database instance.
```
from flask_sqlalchemy import SQLAlchemy
from trusthouse import app

db = SQLAlchemy()

db.init_app(app)
``` 
By doing this, it allows me to use the `db` instance across the app without causing any complications or code breaks.
I can now use the `db` instance to create the tables like in `trusthouse/models/address.py`, and when creating a new review in `trusthouse/routes/create_review.py`.
Let us take a look at how the `Address` table is made:
```
from ..extensions import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    geo_map = db.relationship('Maps', backref='location', uselist=False)
    reviews = db.relationship('Review', backref='address')
```
With all the tables created as an individual Python file, we can go into the *Python interpreter* to create the models.
```
# Make sure you are in the parent directory
from trusthouse.extensions import db
from trusthouse import app
from trusthouse.models import *
db.init_app(app)
db.create_all(app=app)
```


### Creating the Trust House API ###
I wanted to create a backend service for this map, to allow a buisness-to-buisness collaberation with others.
The idea is to create an opportunity for buisness owners and other developers to utilise the **Trust House API** directly from the website, or as a third party within their own apps/systems.

To do this successfully, I had to query the part of the database I wanted, then return the result in a dictionary before converting it into a JSON format.
This here is a good example of why a *One to Many* relationship becomes usefull - it allows me to get access to data from the `Address` table while using a `Review` class object.
Let's see how this looks like in `filter_door.py`.
```
class FilterByDoorAPI(MethodView):
    def get(self, door):
        user_door_request = door
        check_val = db.session.query(
            db.session.query(Address).filter_by(door_num=user_door_request).exists()
        ).scalar()
        if check_val == False:
            void = 'Error'
            message = 'No match found'
            data = {void:message}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_door_request == review.address.door_num:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Type': review.type,
                    'Date': review.date,
                    'Address ID': review.address_id,
                    'Address': {
                        'id': review.address.id,
                        'Door Number': review.address.door_num,
                        'Street': review.address.street,
                        'Postode': review.address.postcode,
                    },
                }
                res.append(result)
        success = 'Successful upload'
        message = 'Your address has been uploaded to Trust House.'
        data = {
            success:message,
            'Reviews by door number': res
        }
        return jsonify(data)
```
First I check if the door number the user has given us exists in the database.
```
user_door_request = door
        check_val = db.session.query(
            db.session.query(Address).filter_by(door_num=user_door_request).exists()
        ).scalar()
```
This returns a `True` or `False` value; so this is very good when checking if the data you want is in the database.
***A good idea would be to change this into a separate function when refactoring the code.***
If the data exists, I then query the `Review` table and check if the user's request matches the door number we have in the database.
```
get_reviews = Review.query.all()
        for review in get_reviews:
            if user_door_request == review.address.door_num:
```
By using `.address` attribute on the `review` variable, I am able to gain access to the variables address - like the `door_num`.
As the for loop iterates through the table, I append each result in the `res` variable *(I hate the name - it won't be there when I refactor!)*; then I create a dictonary with all the information inside. 
This is then easy for me to convert to a JSON format before returning it to the user.
If the `user_door_request` doesn't exist then I create an error message within a dictonary and convert it into a JSON format, before returning it back to the user.


### New Address API ###
For this API I wanted to enable the possiblity for users to create and upload their own address into the Trust House database.  
This would be then relayed on the map for users to see.
I thought this would be good for letting agencies, businesses and landlords.
The logic is almost identical to the `create_review.py`; while `create_review.py` is a post request, `new_address.py` is however a get request!
Bceause `create_review.py` is a large file I will only show a snippet but feel free to check out the full code.
```
class NewAddressAPI(MethodView):
    def get(self, address_door_num, address_street_name, address_location, address_postcode):
        # address data
        door = address_door_num
        street_name = address_street_name
        town_city = address_location
        postcode = address_postcode
```
Here I have created the variables that the user will pass through the web browser, and then use them query the data base as well as other functions.
```
app.add_url_rule(
    '/api/new-address/<address_door_num>,<address_street_name>,<address_location>,<address_postcode>',
    view_func=NewAddressAPI.as_view(
        name='create_new_address'
    ),
)
```
Here is where I create the variables and also *the layout*.
The user must follow the same index as above otherwise the user will end up having ***data in thr wrong columns***, which would give the user unintended results.


# Trust House v.0.4.2 # 
In this version, now that is set up as a modular app it is easier for me to cherry pick areas of code where I would like to refactor.

In most cases, the need to refactor will be due to the coe being repeated across the codebase.
Most of the refactoring will be changing repetative tasks *(like checking if a value exists in the database)* into functions.


# Trust House v.0.4.3.1 #
In this version I will create the functionality for users to be able to add their business details to the Trust House map via a backend API.

I will have to include an extra database table for the buisness names, contact etc.  
For now I will recreate the database tables again, but in the future I will have to know how to migrate database tables.

I will create a new file in the `models` module called `buisness.py` - this is where I will create an extra database table called `Buisness` *(spelling mistake will be amended)*.
The `Buisness` table will have a *One to Many* relationship with the `Address` table.
It will store the buisness name, business category, short description of services and contact details.
The table will also have a `ForeignKey` that will be linked ot the `Address` db model.
```
class Buisness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    services = db.Column(db.String(160), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    addres_id = db.Column(db.Integer, db.ForeignKey('address.id'))
```
In the `Address` table I will then create an additional db realtionship called `buisnesses`,
where I link it to the `Buisness` table and give it an attribute called `address`.
```
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    geo_map = db.relationship('Maps', backref='location', uselist=False)
    reviews = db.relationship('Review', backref='address')
    buisnesses = db.relationship('Buisness', backref='place')
```
To create the database tables I found that that process before wasn't creating all the tables, if not any at all.
To solve this, I found I had to individually import each db model instead of trying to import them all in one line.
```
from trusthouse.extensions import db
from trusthouse import app
from trusthouse.models.address import Address
from trusthouse.models.maps import Maps
from trusthouse.models.review import Review
from trusthouse.models.buisness import Buisness

db.init_app(app)
db.create_all(app=app)
```

### Uploading New Business ###
The idea behind this is to allow any user to upload their business credentials into the Trust House map.  The identification on the map will be different from the reviews located on the map.

First I check if the user's postcode exists:
```
check_postcode = validate_postcode_request(postcode)
```
Next what I do is a little different, because my logic is based around the map co-ordinates, the same process is taken whether `check_postcode` is `True` or `False`.  *You could argue that I would not need to validate the user postcode, but fir now I will leave it as it is until I make futher updates.*

From the user's postcode, I attempt to obtain the co-ordinates (longitude & latitude).
```
user_postcode_coordinates = get_postcode_coordinates(postcode)
```

If `user_postcode_coordinates` is `False` or returns an empty list, it means that even if I save the details in the database, I will not be able to display the information back to the map because there was no co-ordinates.  
For this raeson, an error message will be returned as a jason format.
```
if user_postcode_coordinates == []:
    message = error_message()[3]
    data = {
        'Error': message
    }
    return jsonify(data)
```

If there is a positive response from the usr request (if the list is not empty), it means it will have the longitude & latitude co-ordinates needed to create a point on the map later.
The buisness address is stored in the `Address` table, which stores it's co-ordinates in the `Maps` table, and then the buisness details are stored in the `Buisness` table.
```
elif user_postcode_coordinates:
    new_address = create_new_address(
        door_num.lower(),
        streetname.lower(),
        location.lower(),
        postcode.lower(),
    )
    latitude = user_postcode_coordinates[0].get('lat')
    longitude = user_postcode_coordinates[0].get('lon')
    create_new_map(longitude, latitude, new_address)
    create_new_buisness(
        name.lower(),
        category.lower(),
        services.lower(),
        contact.lower(),
        new_address,
    )
    data = {
        'Successful upload': ok_message()[4],
        'Status': ok_message()[3],
        'New Upload': {
            'Business Name': name.lower(),
            'Business Category': category.lower(),
            'Services': services.lower(),
            'Contact': contact.lower(),
            'Business Address': {
                'Door Number': door_num.lower(),
                'Street': streetname.lower(),
                'Location': location.lower(),
                'Postcode': postcode.lower(),
            },
        },
    }
    return jsonify(data)
``` 
As mentioned before, the same logic would be executed for both True and False outcomes - so essentially I would be repeating the same code twice if I extended the *if-else* statements.


### Map Pointers ###
With the Trust House app now layed out in a modular setting, it makes it easier to add addition to the code - both new & existing.

To make an additional marker to the map I would simply have to create an additional **Folium Marker** to *add* to the map (in the `map` variable).
I create a *nested for-loop* to *first* iterate through all the co-ordinates, then *secondly* iterate through all the buisness entries.
I would check if any had matching `address_id` numbers, then only display the information if the ID matched.
The colour of the marker has been changed to green, along with the sign being changed to the GBP pound sign - to create a clear distinction between the two markers.
```
for trusthouse_map in coordinates:
    for buisness in business_data:
        if trusthouse_map.address_id == buisness.address_id:
            folium.Marker(
                location=[float(trusthouse_map.lat), float(trusthouse_map.lon)],
                popup=f'{buisness.name.upper()}\n{buisness.category}\n{buisness.services}\n{buisness.contact}\n{buisness.place.postcode.upper()}',
                tooltip='View Buisness',
                icon=folium.Icon(color='green', icon='gbp', prefix='fa')
            ).add_to(map)
``` 


### Run the App ###
Now we have successfully created the database tables we can *install* our app to be able to run it with `flask --app`.

**Install app in command line: **
```
pip install -e .
```

**Run app: **
```
flask --app trusthouse run
```


### Installation Requirements ###
These are the following libraries that you will need to install on your virtual environment:
```
pip install Flask
pip install Flask-SQLAlchemy
pip install datetime
pip install geopy
pip install folium
pip install gunicorn
```

### Create requirements.txt File ###
The `requirements.txt` file is needed to enable the app to be able to run all the libraries installed.  You can either manually add all the libraries, or you can automate the process by using the following command in the terminal:
```
pip3 freeze > requirements.txt
```


#### The Next Update(s) ####
- Include functionality to include pictures - how to save more than one pic
- Save pictures in db and display back to user
- May need to do a **Many to Many** relationship between `Review` table and `Pictures` table.
- Include functionality for users to upload thier buisness address details to be displayed on the map (part of self local advertisement)
- Build a business directory
- Create a drop down selection for users to search reviews by tenant, neighbours, vistors.
- Create functionality for users to upload buisness via web browser API
  - it should be linked to the addres model
  - one to many relationship
  - each new entry creates a new marker on the map
  - the marker will be a differnt color and different icon from the reviews
- Create functionality for users to search reviews by tenant, neighbour, visitor
- Return more data in the JSON objects (include the map coordinates of the addresses)

