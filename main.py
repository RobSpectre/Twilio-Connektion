'''
Connektion
Connect with a random stranger via phone at a conference.

Written by /rob, 5 November 2011.

Inspired by Mozilla Festival.
'''


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from twilio import twiml
from random import choice
import models

'''
Controllers
'''
class ConnektionResponse(twiml.Response):
    def __init__(self):
	twiml.Response.__init__(self)
	self.name = "Response"

    def speak(self, string):
        return self.say(string, language="gb-en", voice="woman")


class DefaultHandler(webapp.RequestHandler):
    def __init__(self):
	self.r = ConnektionResponse()
	webapp.RequestHandler.__init__(self)

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("Make a Connektion with a stranger.")
        
    def renderTwiML(self, twiml_response_object):
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(str(twiml_response_object))

    def getUsers(self, phone_number):
        query = db.Query(models.User)
        query.filter('active = ', True).filter('From = ',
            phone_number).order('-date') 
        return query.fetch(limit=500)

    def getConnections(self, phone_number):
        query = db.Query(models.Connection)
        query.filter('phone_number = ', phone_number).order('-date')
        return query.fetch(limit=500)

    def handle_exception(self, e, debug):
        logging.exception(e)
        self.r.speak("Terribly sorry - we've encountered an error making " +
                "your connection.  Please try again shortly.")
        self.renderTwiML(self.r)

class VoiceHandler(DefaultHandler):
    def post(self):
        # Establish call parameters
        phone_number = self.request.get("To")
        From = self.request.get("From")

        # See if user exists
        query = db.Query(models.User)
        query.filter('phone_number = ', phone_number).filter('From = ', From)
        user = query.fetch(limit=1)

        if not user:
            self.r.redirect("/newuser")
        else:
            user[0].active = True
            self.r.speak("Welcome to Mozilla Festival Connection.")
            self.r.speak("Please press 8 if you would like to unsubscribe.")
            self.r.gather(action="/unsubscribe", numDigits="1")
            self.r.redirect("/connect")

        self.renderTwiML(self.r)

class ConnectUserHandler(DefaultHandler):
    def post(self):
        # Establish call parameters
        phone_number = self.request.get("To")
        From = self.request.get("From")

        users_query = db.Query(models.User)
        users_query.filter('phone_number = ', phone_number).filter('From != ',
			From)
        users = users_query.fetch(limit=500)

        if users:
            self.r.speak("Lovely - just one moment while we connect you with " +
                    "someone new.")
            user = choice(users)
            self.r.dial(user.From, callerId=phone_number)
        else:
	        self.r.speak("No connection can be found.  Expect a phone call from " +
			    "someone new soon.")

        self.renderTwiML(self.r)

class NewUserHandler(DefaultHandler):
    def post(self):
        # Get recording from user
        self.r.speak("Welcome to Mozilla Festival Connection.  Say your name" +
            " after the beep and press pound when you are finished.")
        self.r.record(finishOnKey="#", action="/recording")
        self.r.speak("I'm sorry - I did not catch that.")
        self.r.redirect("/newuser")
        self.renderTwiML(self.r)       

class RecordingHandler(DefaultHandler):
    def post(self):
        user = models.User()
        user.AccountSid = self.request.get("AccountSid")
        user.From = self.request.get("From")
        user.phone_number = self.request.get("To")
        user.Body = self.request.get("Body")
        user.City = self.request.get("City")
        user.State = self.request.get("State")
        user.Zip = self.request.get("Zip")
        user.Country = self.request.get("Country")
        user.RecordingUrl = self.request.get("RecordingUrl")
        user.put()
        self.r.speak("Lovely - now wait for a moment while we connect you to" +
            " to someone new.")
        self.r.redirect("/connect")
        self.renderTwiML(self.r)

class UnsubscribeHandler(DefaultHandler):
    def post(self):
        # Establish call parameters
        phone_number = self.request.get("To")
        From = self.request.get("From")

        users_query = db.Query(models.User)
        users_query.filter('phone_number = ', phone_number).filter('From = ',
			From)
        users = users_query.fetch(limit=500)

        if users and self.request.get("NumDigits") == "8":
            user = users.pop()
            user.active = False
            user.put()
            self.r.speak("Thank you - you are now unsubscribed. Good day.")
            self.r.hangup()
        else:
            self.r.speak("I'm sorry - did not understand that.")
            self.r.redirect("/voice")
        self.renderTwiML(self.r)

application = webapp.WSGIApplication([('/', DefaultHandler),
                                      ('/voice', VoiceHandler),
                                      ('/connect', ConnectUserHandler),
                                      ('/recording', RecordingHandler),
                                      ('/newuser', NewUserHandler),
                                      ('/unsubscribe', UnsubscribeHandler)],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
