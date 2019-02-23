from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()

    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scraper():
    # Declare mongodb objects (collections)
    mars = mongo.db.mars
    # Get mars and hemisphere data from scrapping
    mars_data = scrape_mars.scrape()
    # Update MongoDB
    mars.update({}, mars_data, upsert=True)
    # Refresh page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
