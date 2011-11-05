'''
Connektion - Functional Tests
'''
import unittest
from google.appengine.ext import db
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
        self.assertTrue("Redirect" in response, "Did not find Redirect verb" +
                " in response, instead found: %s" % str(response))
        self.assertTrue("connect" in response, "Did not find connect ref" +
                " in response, instead found: %s" % str(response))

    def test_recording(self):
        response = app.post("/recording", self.test_call)
        self.assertTwiML(response)
        self.assertEqual(1, len(models.User().all().fetch(2)))

    def test_connect(self):
        setup_call = self.test_call.copy()
        setup_call['From'] = "+15555555555"
        app.post("/recording", setup_call)
        app.post("/recording", self.test_call)
        response = app.post("/connect", self.test_call)
        self.assertTwiML(response)
        self.assertEqual(2, len(models.User().all().fetch(2)))
        self.assertTrue("Dial" in response, "Did not find Dial verb" +
                " in response, instead found: %s" % str(response))
        self.assertTrue("+15555555555" in response, "Did not find " +
                " test number, instead found: %s" % str(response))

class ReturningUser(Test_Function):
    def setUp(self):
        Test_Function().setUp()
        self.first_call = app.post("/recording", self.test_call)

    def test_voice(self):
        response = app.post("/voice", self.test_call)
        self.assertTwiML(response)
        self.assertTrue("Connection" in response, "Did not find return " +
                "user welcome.  Instead found: %s" % str(response))
        self.assertTrue("Redirect" in response, "Did not find redirect " +
                "verb in response. Instead found: %s" % str(response))
        self.assertTrue("/connect" in response, "Did not find connect " +
                "redirect in response. Instead found: %s" % str(response))
