import os

from flask import Flask

from twilio import twiml

import requests


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')
app.config['API_PATH'] = \
    "http://api.nytimes.com/svc/mostpopular/v2/"\
    "mostviewed/all-sections/1.json?api-key="


# Specify Conference Room
@app.route('/conference/<conference_room>', methods=['POST'])
def voice(conference_room):
    response = twiml.Response()
    with response.dial() as dial:
        dial.conference(conference_room, waitUrl="/wait")
    return str(response)


# Conference Room Hold Music Reading Headlines from New York Times
@app.route('/wait', methods=['POST'])
def waitUrl():
    response = twiml.Response()

    if app.config['NYTIMES_API_KEY']:
        api_request = requests.get("%s%s" % (app.config['API_PATH'],
            app.config['NYTIMES_API_KEY']))
        if api_request.status_code == 200:
            json_response = api_request.json()
            if json_response:
                response.say("While you wait for your conference to connect," \
                        " here are today's headlines from the New York Times.",
                        voice="alice")
                for result in json_response['results']:
                    response.say(result['abstract'], voice='alice')
                    response.pause()
            else:
                response.say("Unable to parse result from New York Times API.")
                response.say("Check your configuration and logs.")
                response.redirect("/music")
        else:
            response.say("Unable to reach New York Times API.")
            response.say("Check your configuration and logs for the error.")
            response.redirect("/music")
    else:
        response.say("Configuration error: You need to set your New York " \
                "Times API Key environment variable. See the README for " \
                "more information.")
        response.redirect("/music")

    return str(response)


# In the event of a failure, deliver hold music.
@app.route('/music', methods=['POST'])
def music():
    response = twiml.Response()
    response.say("Now, enjoy this normal hold music.")
    response.play("http://com.twilio.music.soft-rock.s3.amazonaws.com/"\
            "Fireproof_Babies_-_Melancholy_4_a_Sun-lit_day.mp3")
    return str(response)


# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
