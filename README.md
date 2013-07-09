# New York Times Conference Room 

Instead of hold music for your [Twilio
Conference](http://www.twilio.com/docs/api/twiml/conference), read the caller
the latest headlines from [The New York Times](http://www.nytimes.com).

[![Build
Status](https://secure.travis-ci.org/RobSpectre/New-York-Times-Conference-Room.png)]
(http://travis-ci.org/RobSpectre/New-York-Times-Conference-Room)


## Features

Look at all these crazy features!

* Dynamic Conferencing - Create new conferences by passing the name as parameter
  (e.g. `http://example.com/conference/my_awesome_conference`).
* Easy Configuration - Use `local_settings.py` to set your Twilio and New York
  Times credentials.
* Alice - Get the news with the soothing voice of
  [Alice](http://www.twilio.com/blog/2013/07/twilio-tts-improvements.html),
  Twilio's new <Say> voice.
* Tests - Fully tested? You betcha.
* PEP8 - It's good for you!


## Dependencies

* [Twilio account](https://www.twilio.com/try-twilio)
* [New York Times developer account](http://developer.nytimes.com/)
* [Flask](http://flask.pocoo.org/)
* [Requests](http://docs.python-requests.org/)

*Optional for tests*

* [Nose](https://nose.readthedocs.org/)
* [Mock](http://www.voidspace.org.uk/python/mock/)
* [simplejson](http://simplejson.readthedocs.org/)


## Usage

This project ships with two ready-to-go endpoints for your Twilio conference.
One dials the user into the Conference, the other serves the wait room.

To setup a Twilio phone number with a conference room that plays the hold music,
just set the Voice Request URL to your number to the conference endpoint with
the name of your conference as a parameter:

`http://example.com/conference/my_awesome_conference`

To just hear the headlines, point the Twilio phone number's Voice Request URL
directly to the wait room: 

`http://example.com/wait`

Want to try without installing?  Call (646) 430-9298!


## Installation

Step-by-step on how to deploy, configure and develop on this project.

### Getting Started 

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/New-York-Times-Conference-Room.git 
</pre>

2) Navigate to folder and create new Heroku Cedar app
<pre>
heroku create
</pre>

3) Deploy to Heroku
<pre>
git push heroku master
</pre>

4) Scale your dynos
<pre>
heroku scale web=1
</pre>

5) Configure your New York Times API Key for the dyno.
<pre>
heroku config:add NYTIMES_API_KEY=xxxxx
</pre>


### Configuration

Want to configure your dev environment to hack on this project?

#### local_settings.py

local_settings.py is a file available for you to configure
your Twilio and New York Times account credentials manually.
Be sure not to expose your Twilio account to a public repo though.

```python
ACCOUNT_SID = "ACxxxxxxxxxxxxx" 
AUTH_TOKEN = "yyyyyyyyyyyyyyyy"
TWILIO_APP_SID = "APzzzzzzzzz"
TWILIO_CALLER_ID = "+17778889999"
export NYTIMES_API_KEY=wooooooo
```

#### Setting Your Own Environment Variables

The configurator will automatically use your environment variables if you
already have a TwiML app and phone number you would prefer to use.  When these
environment variables are present, it will configure the Twilio and Heroku apps
all to use the hackpack.

1) Set environment variables locally.
<pre>
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=yyyyyyyyyyyyyyyyy
export TWILIO_APP_SID=APzzzzzzzzzzzzzzzzzz
export TWILIO_CALLER_ID=+15556667777
export NYTIMES_API_KEY=wooooooo
</pre>


### Development

Getting your local environment setup to work with this hackpack is similarly
easy.  After you configure your hackpack with the steps above, use this guide to
get going locally:

1) Install the dependencies.
<pre>
make init
</pre>

2) Launch local development webserver (using the great
[Foreman](http://ddollar.github.io/foreman/))
<pre>
foreman start
</pre>

3) Open browser to [http://localhost:5000](http://localhost:5000).

4) Tweak away on `app.py`.


## Testing

This project comes with a full testing suite ready for nose.

<pre>
make test
</pre>



## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 
* Inspired by a [tweet from Amit
  Jotwani](https://twitter.com/amit/status/354670570811572224).
