from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars_info_data = scrape_costa.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_info_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
