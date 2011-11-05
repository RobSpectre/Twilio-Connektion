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
from local_settings import *
import models

'''
Controllers
'''

class MainPage(webapp.RequestHandler):
    r = ConnektionResponse()

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

class VoiceHandler(MainPage):
    def post(self):
        # Establish call parameters
        phone_number = self.request.get("To")
        From = self.request.get("From")

        # See if user exists
        query = db.Query(models.User)
        query.filter('To = ', phone_number).filter('From = ', From)

        if not query.fetch(limit=1):
            r.redirect("/newuser")
        else:
            r.speak("Welcome to Mozilla Festival Connection - standby while we
            connect you with someone new.")
            r.redirect("/connect")

        self.renderTwiML(r)

class ConnectUserHandler(MainPage):
    def post(self):
        users_query = db.Query(models.User)
        users_query.filter('phone_number = ', phone_number).filter('From
                !=', From)
        users = users_query.fetch(limit=500)
        user = random.choice(users)

        r.dial(user.From)

        self.renderTwiML(r)


class NewUserHandler(MainPage):
    def post(self):
        # Set parameters for the call
        phone_number = self.request.get("To")
        From = self.request.get("From")
        
        # Get recording from user
        with r.record(finishOnKey="#", action="/recording") as record:
            record.say("Welcome to Mozilla Festival Connection.  Say your name
            after the beep and press pound when you are finished.")

        r.speak("Lovely - now wait for a moment while we connect you to someone
        new.")
        r.redirect("/connect")

        self.renderTwiML(r)       

class RecordingHandler(MainPage):
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
                        
class ConnektionResponse(twiml.Response):
    def speak(self, string):
        return twiml.Response().say(string, language="gb-en", voice="woman")

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/voice', VoiceHandler),
                                      ('/connect', ConnectUserHandler),
                                      ('/recording', RecordingHandler),
                                      ('/newuser', NewUserHandler)],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main():
