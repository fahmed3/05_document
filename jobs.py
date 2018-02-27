'''
Dataset has a list of jobs by industry and their locations.
https://data.ny.gov/api/views/pxa9-czw8/rows.json?accessType=DOWNLOAD
Imported into database by going through the lists of jobs and turning them into dictionaries
with industry and location, then inserting that list of documents into the database.
'''
from flask import Flask, render_template, redirect, url_for, request
import pymongo
import json


app = Flask(__name__)
connection = pymongo.MongoClient('homer.stuy.edu')

db = connection['ahmedF-parkP']
collection = db['jobs']

def importJobs():
    jobs = []
    jobData = json.load(open("jobs.json"))['data']
    for j in jobData:
        job = {}
        job["location"] = j[9]
        job["industry"] = j[11]
        jobs.append(job)
    #print jobs
    collection.insert_many(jobs)

#importJobs()
    
def location(l):
    location = collection.find({'location' : l})
    retList = []
    for i in location:
        retList.append(i)
    return retList

#print location("New York City")
        
def industry(j):
    industry = collection.find({'industry' : j})
    retList = []
    for i in industry:
        retList.append(i)
    return retList

#print industry("Accommodation and Food Services")


@app.route('/')
def index():
    db.collection.drop()
    importJobs()
    return render_template('index.html')

@app.route('/results', methods=["GET","POST"])
def results():
    if request.method == 'POST':
        l = request.form['loc']
        i = request.form['ind']
    loc = [{'location': 'No Selected Location'}]
    ind = [{'industry': 'No Selected Industry'}]
    if l != '':
        loc = location(l)
    if i != '':
        ind = industry(i)
    return render_template('results.html', loc = loc,
                           ind = ind)

if __name__ == '__main__':
    app.debug = True
    app.run()
