# Twilio Connektion

A Twilio Voice app that connects you to someone new.


## Summary

Twilio Connektion is a Twilio Voice app that lets conference goers connect to
people they have not yet met.  Using a "chat roulette" style random pool, Twilio
Connektion creates a central number that people can call and creates new users
for people who want to "connekt."  

Folks who call that number go through a very quick voice registration and then
are connected to someone they haven't spoke with before at random.

Callers' phone numbers or other identifying information are never revealed - it
is up to the participants to choose whether or not to make a personal
connection.


## Technology

* [Python](http://python.org)
* [Google App Engine](http://appengine.google.com)
* [Twilio](http://www.twilio.com)
* You. :)


## Usage

If you're at [MozFest](https://mozillafestival.org/), call +44 20 3475 2916 to
make a Connektion.


## Hacking

Accepting pull requests - if you're at MozFest, just seek out the guys with the
[Twilio](http://www.twilio.com) lab coats.

### Installation

1) Install [Google App Engine for
Python](http://code.google.com/appengine/docs/python/gettingstarted/).

2) Clone repo

<pre>
git clone git@github.com:RobSpectre/Twilio-Connektion.git
</pre>

3) Use the following URL for your Voice Request URL for any Twilio phone number:

<pre>
http://example.appspot.com/voice
</pre>

TODO:

* Unsubscribe
* Time zones / hour limitations
* Tracking for who you've talked to
* Banning
* Multiple number support


### Testing

Twilio Connektion relies on [Nose](http://code.google.com/p/python-nose/) for
testing.  Be sure to also install the [nose-gae
plugin](http://pypi.python.org/pypi/NoseGAE/0.1.3).

<pre>
nosetests -v --with-gae
</pre>


## Credits

* Contributors: [Rob Spectre](http://www.brooklynhacker.com)
* License: [Mozilla Public License](http://www.mozilla.org/MPL/)
* Written: 6 November 2011 at [Mozilla Festival](https://mozillafestival.org/)
