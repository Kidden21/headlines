from flask import Flask, render_template, request
import feedparser
import json
import urllib2
import urllib
app = Flask(__name__)

##@app.route('/')
##def main():
##    return render_template('j2_query.html')
##
##@app.route('/process', methods=['POST'])
##def process():
##    _username = request.form.get('username')
## 
##    if _username:
##        return render_template('j2_response.html', username=_username)
##    else:
##        return 'Please go back and enter your name...', 400

##BBC_FEED = "https://feeds.bbci.co.uk/news/rss.xml"

##@app.route('/')
##def get_news():
##  feed = feedparser.parse(BBC_FEED)
##  first_article = feed['entries'][0]
##  return """<html>
##    <body>
##        <h1> BBC Headlines </h1>
##        <b>{0}</b> <br/>
##        <i>{1}</i> <br/>
##        <p>{2}</p> <br/>
##    </body>
##</html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))

##@app.route('/')
##
##@app.route('/bbc')
##def bcc():
##  return get_news('bbc')
##
##@app.route('/cnn')
##def cnn():
##  return get_news('cnn')
##
##def get_news(publication):
##  feed = feedparser.parse(RSS_FEEDS[publication])
##  first_article = feed['entries'][0]
##  return """<html>
##    <body>
##        <h1>Headlines </h1>
##        <b>{0}</b> </ br>
##        <i>{1}</i> </ br>
##        <p>{2}</p> </ br>
##    </body>
##</html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc',
            'city': 'London,UK'}

api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=360e421adefdbcf3969725a2c809c0ff"


@app.route('/')
def home():
  publication = request.args.get('publication')
  if not publication:
    publication = DEFAULTS['publication']
  articles = get_news(publication)
  city = request.args.get('city')
  if not city:
    city = DEFAULTS['city']
  weather = get_weather(city)
  return render_template("home.html", articles=articles,weather=weather)

def get_news(query):
  if not query or query.lower() not in RSS_FEEDS:
    publication = "bbc"
  else:
    publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed["entries"]

def get_weather(query):
  query = urllib.quote(query)
  url = api_url.format(query)
  data = urllib2.urlopen(url).read()
  parsed = json.loads(data)
  weather = None
  if parsed.get("weather"):
    weather = {'description': parsed['weather'][0]['description'],
           'temperature': parsed['main']['temp'],
           'city': parsed['name'],
           'country': parsed['sys']['country']
          }
  return weather
##  feed = feedparser.parse(RSS_FEEDS[publication])
##  first_article = feed['entries'][0]
##  return render_template("home.html",articles=feed['entries'])

if __name__ == '__main__':
    app.run(debug=True)
