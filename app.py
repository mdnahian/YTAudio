import logging
from random import randint
import youtube_dl
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, audio, current_stream
import subprocess
from bs4 import BeautifulSoup
import urllib
import urllib2
import json


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("SearchIntent", convert={'term': str})
def search_term(term):
    
    term = term.replace("for", "")
    term = term.replace("search", "")
    term = term.strip()

    s = { 'search_query':term }

    url = 'https://www.youtube.com/results?'+urllib.urlencode(s)

    print url

    raw = urllib2.urlopen(url)
    html = BeautifulSoup(raw, "html.parser")

    videos = html.findAll(match_class(["yt-lockup-title"]))

    audio = []

    for video in videos:
        link = video.findAll('a')[0]
        audio.append([link.text, link['href']])

    audio.pop(0)
    audio.pop(0)

    results = render_template('notfound', term=term)

    if len(audio) >= 3:
        results = render_template('choose', audio1=audio[0][0], audio2=audio[1][0], audio3=audio[2][0])
        session.attributes['term'] = term
        session.attributes['results'] = audio

    return question(results)


@ask.intent("SelectionIntent", convert={'selection': int})
def select(selection):
    audio = session.attributes['results']
    term = session.attributes['term']

    if selection == 'one':
        selection = 0
    elif selection == 'two':
        selection = 1
    elif selection == 'three':
        selection = 2
    else:
        return statement(render_template('again'))

    session.attributes['url'] = 'https://www.youtube.com'+str(audio[selection][1])

    selected = render_template('selected', term=audio[selection][0])

    return question(selected)


@ask.intent("PlayIntent")
def play():
    url = session.attributes['url']

    response = subprocess.Popen(["youtube-dl", url, "-j"], stdout=subprocess.PIPE)

    # response = response[:-2]

    raw = json.loads(response.stdout.read())

    source = ''

    for format in raw['formats']:
        if format['ext'] == 'mp4':
            source = format['url']

    return audio('Playing').play(source)
    



@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the stream.').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()


@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)



if __name__ == '__main__':
    app.run(port=80, debug=True)