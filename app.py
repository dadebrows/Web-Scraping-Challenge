from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Instance of Flask
app = Flask(__name__)

# PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# index.html template using Mongo
@app.route("/")
def index():

    # Find record of data from Mongo
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars_data = mars)

# Route to trigger scrape function
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars
    # Run the scrape function
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)