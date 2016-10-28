from flask import Flask,render_template,jsonify,request,redirect,url_for
import json
import shepard
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
from bs4 import BeautifulSoup
from urllib.parse import quote
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
client = MongoClient()
db = client['flock-db']

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                        ssl_version=ssl.PROTOCOL_TLSv1)

@app.route("/")
def index():
    return render_template('index.html', title='Home')

@app.route("/chat")
def chat():
    return render_template('chat.html', title='Chat')

@app.route("/about")
def about():
    return render_template('index.html', title='About')

@app.route("/blog")
def blog():
    return render_template('index.html', title='Blog')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        db.users.insert_one({
            'fname':request.form['first_name'],
            'lname':request.form['last_name'],
            'username':request.form['username'],
            'password':request.form['password']
        })
        return redirect(url_for("chat"))

    else:
        return render_template('signup.html', title='Sign Up')

@app.route("/api/questions", methods=['GET'])
def questions():
    questions_cursor = db.questions.find()
    return dumps(questions_cursor)

@app.route("/api/ask", methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':

        # Get our search query
        query = request.form['query']

        #Save the query to the database
        db.questions.insert_one({"question":query})

        # Get Location from Request
        locations = request.form['location'].split(',')
        location = quote(locations[2] + locations[3],safe='')

        # Get important words via shepard
        shep_result = shepard.recognize(query)
        print(shep_result)
        if(len(shep_result['nouns']) == 0):
            words = str(query)
        else:
            words = str(shep_result['nouns'])


        # Create our searching URL
        url_formatted_query = quote(words.strip('[]'),safe='')
        print(url_formatted_query)
        url = "https://www.bing.com/search?q="
        full_url = url + url_formatted_query + location
        print(full_url)

        # Create a request Session to search with
        s = requests.Session()
        s.mount('https://', MyAdapter())
        results = s.get(full_url)

        # Scrape our result with BeautifulSoup
        soup = BeautifulSoup(results.content, 'html.parser')
        titles = soup.find_all('h2')
        links = list()

        for title in titles:
            if str(title).find(',Ads" ') is -1:
                links.append(str(title))

        # Return all the links we found
        return json.dumps({'links': links})


if __name__ == "__main__":
    app.run(debug=True,port=9000)
