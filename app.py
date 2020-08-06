from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    # print(mars)
    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    # data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    # mongo.db.collection.replace_one({}, data, upsert=True)
    # Redirect back to home page

    mars= mongo.db.mars
    mars_data = scrape_mars.scrape()
    # print(mars_data)
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)
    # return "Scrape successful!"

if __name__ == "__main__":
    app.run(debug=True)
