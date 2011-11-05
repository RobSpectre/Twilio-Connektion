'''
Connektion - Unit Tests
'''
import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
import models

class Test_Model(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

class Test_User(Test_Model):
    def test_insertUser(self):
	user = models.User()
	user.AccountSid = "test"
	user.From = "test"
	user.phone_number = "test"
	user.City = "test"
	user.State = "test"
	user.Zip = "test"
	user.Country = "test"
	user.RecordingUrl = "test"
	user.put()

        self.assertEqual(1, len(models.User().all().fetch(2)))

class Test_Connection(Test_Model):
   def test_insertConnection(self):
	connection = models.Connection()
	connection.CallSid = "test"
	connection.phone_number = "test"
	connection.From = "test"
	connection.To = "test"
	connection.Duration = 60
	connection.put()

        self.assertEqual(1, len(models.Connection().all().fetch(2)))
