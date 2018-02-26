'''
Dataset has a list of jobs by industry and their locations.
https://data.ny.gov/api/views/pxa9-czw8/rows.json?accessType=DOWNLOAD
Imported into database by going through the lists of jobs and turning them into dictionaries
with industry and location, then inserting that list of documents into the database.
'''

import pymongo
import json

connection = pymongo.MongoClient('homer.stuy.edu')

db = connection['ahmedF-parkP']
collection = db['jobs']

def importJobs():
    jobs = []
    jobData = json.load(open("jobs.json"))['data']
    #jobData consists of lists of lists so turning it into a list of dictionaries
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
    for i in location:
        print i

#location("New York City")
        
def industry(j):
    industry = collection.find({'industry' : j})
    for i in industry:
        print i

#industry("Accommodation and Food Services")
