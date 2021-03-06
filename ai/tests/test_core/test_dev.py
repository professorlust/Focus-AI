# Rushy Panchal
# ai/tests/core/test_dev.py

import unittest
import baseTests

from core.dev import DevelopmentServer

import pymongo

class TestDevelopmentServer(unittest.TestCase, baseTests.BaseTest):
	'''Test the core.dev.DevelopmentServer class'''
	testClass = DevelopmentServer

	def setUp(self):
		'''Set up the test case'''
		self.testObject = self.testClass()

	def test_startStop(self):
		'''DevelopmentServer.start and stop work'''
		self.assertEquals(self.testObject.running, False)

		self.testObject.start()
		self.assertEquals(self.testObject.running, True)
		try:
			connection = pymongo.Connection()
			self.assertEquals(connection.alive(), True)
		except pymongo.errors.ConnectionFailure:
			self.fail("Connection Failed")

		self.testObject.stop()
		connection.close()

		self.assertEquals(self.testObject.running, False)
		self.assertEquals(connection.alive(), False)
