'''
Connektion - Functional Tests
'''
import unittest
from google.appengine.ext import testbed
from webtest import TestApp
from main import application
import models


app = TestApp(application)

class Test_Function(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.test_call = {
                'AccountSid': 'test',
                'From': '+12223334444',
                'To': '+17778889999',
                'FromCity': 'test',
                'FromState': 'test',
                'FromCountry': 'test',
                'FromZip': 'test',
                'RecordingUrl': 'test'
                }

    def tearDown(self):
        self.testbed.deactivate()

    def assertTwiML(self, response):
        self.assertEqual('200 OK', response.status)
        self.assertTrue('<Response>' in response, "Received instead: %s" % str(response))
        self.assertTrue('</Response>' in response, "Received instead: %s" % str(response))
        self.assertFalse('Error' in response, "Received instead: %s" % str(response))
	self.assertFalse("Terribly sorry" in response, "Found error: %s" % str(response))

    def setupUsers(self, integer):
	users = []
	for i in range(integer):
	    setup_call = self.test_call.copy()
	    setup_call['From'] = "+1555555555%i" % i
	    app.post("/recording", setup_call)
	    users.append(setup_call)
	return users 

class Test_FirstTimeUser(Test_Function):
    def test_voice(self):
        response = app.post("/voice", self.test_call)
        self.assertTwiML(response)
        self.assertTrue("newuser" in response, "Did not find 'newuser'" + 
            "response, instead found: %s" % str(response))

    def test_newuser(self):
        response = app.post("/newuser", self.test_call)
        self.assertTwiML(response)
        self.assertTrue("Record" in response, "Did not find Record verb" +
                " in response, instead found: %s" % str(response))
	self.assertTrue("Say" in response, "Did not find warning catch" +
		" in response, instead fonud: %s" % str(response))
        self.assertTrue("Redirect" in response, "Did not find Redirect verb" +
                " in response, instead found: %s" % str(response))

    def test_recording(self):
        response = app.post("/recording", self.test_call)
        self.assertTwiML(response)
        self.assertEqual(1, len(models.User().all().fetch(2)))
        self.assertTrue("connect" in response, "Did not find connect ref" +
                " in response, instead found: %s" % str(response))

    def test_connect(self):
	users = self.setupUsers(2)
        response = app.post("/connect", users[1])
        self.assertTwiML(response)
        self.assertEqual(2, len(models.User().all().fetch(2)))
        self.assertTrue("Dial" in response, "Did not find Dial verb" +
                " in response, instead found: %s" % str(response))
        self.assertTrue(users[0]['From'] in response, "Did not find " +
                " test number, instead found: %s" % str(response))
	self.assertTrue(users[1]['To'] in response, "Did not find to" +
		" number, instead found: %s" % str(response))
	self.assertTrue("callerId" in response, "Did not find callerId " +
		" reference, instead found: %s" % str(response))

class ReturningUser(Test_Function):
    def test_voice(self):
	users = self.setupUsers(1)
        response = app.post("/voice", users[0])
        self.assertTwiML(response)
        self.assertTrue("Connection" in response, "Did not find return " +
                "user welcome.  Instead found: %s" % str(response))
        self.assertTrue("Redirect" in response, "Did not find redirect " +
                "verb in response. Instead found: %s" % str(response))
        self.assertTrue("/connect" in response, "Did not find connect " +
                "redirect in response. Instead found: %s" % str(response))
	self.assertTrue("/unsubscribe" in response, "Did not find unsubscribe" +
		" option in response.  Instead found: %s" % str(response))

class Unsubscribe(Test_Function):
    def test_unsubscribe(self):
	users = self.setupUsers(1)
	users[0]['Digits'] = "8"
	response = app.post("/unsubscribe", users[0])
	self.assertTwiML(response)
        self.assertEqual(1, len(models.User().all().filter('active = ', 
		False).fetch(2)))

    def test_unsubscribeIncorrectDigit(self):
	users = self.setupUsers(1)
	users[0]['Digits'] = "7"
	response = app.post("/unsubscribe", users[0])
	self.assertTwiML(response)
	self.assertEqual(1, len(models.User().all().filter('active = ',
		True).fetch(2)))

    def test_callInAfterUnsubscribe(self):
	users = self.setupUsers(1)
	users[0]['Digits'] = "8"
	app.post("/unsubscribe", users[0])
	response = app.post("/voice", users[0])
	self.assertTwiML(response)
	self.assertEqual(1, len(models.User().all().filter('active = ',
		True).fetch(2)))
	self.assertTrue("coming back" in response, "Did not find welcome" +
		" back message in response. Instead found: %s" % str(response))
