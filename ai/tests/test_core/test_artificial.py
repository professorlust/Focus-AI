# Rushy Panchal
# ai/tests/core/test_artificial.py

import unittest
import baseTests
import numpy as np

from core.artificial import DynamicScriptingAI, BaseAI, StaticAI
from core.engine import Engine
from core.database import Database

import config
import models

class TestBaseAI(baseTests.NumpyTest, unittest.TestCase):
	'''Test the core.artificial.BaseAI class'''
	testClass = BaseAI

	@classmethod
	def setUpClass(cls):
		'''Sets up the class of testing'''
		cls.db = Database(host = config.DB_HOST, port = config.DB_PORT)
		cls.db.register(models.Rule)
		models.register(cls.db)
		
		cls.engine = Engine(database = cls.db)
		cls.game_id = cls.engine.newGame()
		
		cls.testObject = cls.testClass(database = cls.db, engine = cls.engine, game = cls.game_id)

	@classmethod
	def tearDownClass(cls):
		'''Cleanup the test class'''
		cls.db.close()

	def test_hasMakeMove(self):
		'''DynamicScriptingAI.makeMove method exists'''
		self.assertFunctionExists(self.testObject, "makeMove")

	def test_hasSetState(self):
		'''DynamicScriptingAI.setState method exists'''
		self.assertFunctionExists(self.testObject, "setState")

	def test_setState(self):
		'''DynamicScriptingAI.setState works'''
		newState = "newState"

		self.assertNotEquals(self.testObject.state, newState)
		self.assertNotEquals(self.engine.games[self.game_id], newState)

		self.testObject.setState(newState)

		self.assertEquals(self.testObject.state, newState)
		self.assertEquals(self.engine.games[self.game_id], newState)

class TestDynamicScriptingAI(TestBaseAI):
	'''Test the core.artificial.DynamicScriptingAI class'''
	testClass = DynamicScriptingAI

	@classmethod
	def setUpClass(cls):
		'''Set up the class for unit testing'''
		cls.db = Database(host = config.DB_HOST, port = config.DB_PORT)
		cls.db.register(models.Rule)
		models.register(cls.db)
		
		cls.engine = Engine(database = cls.db)
		cls.game_id = cls.engine.newGame()

		cls.testObject = cls.testClass(database = cls.db, engine = cls.engine, game = cls.game_id)

		cls.rulesAdded = []

		cls.stateC = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[2, 0, 0, 0, 2, 0, 2, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = np.int32)

		cls.rulesAdded.append(
			models.Rule.new(
			cls.stateC,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			[(5, 6), [(3, 4)]]
			))

		cls.stateD = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 0, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 1],
			[0, 0, 0, 0, 0, 0, 2, 0],
			[0, 1, 0, 2, 0, 0, 0, 0],
			[2, 0, 2, 0, 0, 0, 0, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = np.int32)

		modifiedStateD = np.copy(cls.stateD)
		modifiedStateD[-1, -1] = 2 # make this state less similar than the rest

		# For the complex rules only
		cls.rulesAdded.append(
			models.Rule.new(
			modifiedStateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 1],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			[(3, 6), (2, 5)]
			))

		cls.rulesAdded.append(
			models.Rule.new(
			modifiedStateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			[(5, 0), [(3, 2)]]
			))

		cls.rulesAdded.append(
			models.Rule.new(
			modifiedStateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			[(3, 6), [(1, 4)]]
			))

		cls.rulesAdded.append(
			models.Rule.new(
			cls.stateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			[(5, 0), [(3, 2), (1, 4)]],
			initialWeight = 2
			))

	@classmethod
	def tearDownClass(cls):
		'''Tear down the class after unit testing'''
		for rule in cls.rulesAdded:
			rule.delete()
		cls.db.close()

	def setUp(self):
		'''Sets up the test case'''
		self.stimuli = [
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, -1, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 1],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32)
			]
		self.testObject.possibleStimuli = self.stimuli
		self.stateA = np.asarray([
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[2, 2, 0, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2, 2, 2],
			], dtype = np.int32)
		self.stateB = np.asarray([
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[2, 2, 2, 0, 2, 2, 2, 2],
			[2, 2, 2, -1, 2, 2, 2, 2],
			], dtype = np.int32)

	def test_inheritsBaseAI(self):
		'''DynamicScriptingAI inherits from BaseAI'''
		self.assertIsSubclass(self.testClass, BaseAI)
		self.assertIsSubclass(self.testClass, object)

	def test_instanceBaseAI(self):
		'''DynamicScriptingAI is instance of BaseAI'''
		self.assertIsInstance(self.testObject, BaseAI)
		self.assertIsInstance(self.testObject, object)

	def test_hasAnalyzeStimuli(self):
		'''DynamicScriptingAI.analyzeStimuli method exists'''
		self.assertFunctionExists(self.testObject, "analyzeStimuli")

	def test_makeMove(self):
		'''DynamicScriptingAI.makeMove works'''
		self.testObject.setState(self.stateC)
		copyC = np.copy(self.stateC)

		# Make sure they are equal to start with
		self.assertEquals(self.testObject.state, copyC)

		self.testObject.makeMove()
		copyC[5, 6] = 0
		copyC[4, 5] = 0
		copyC[3, 4] = 2

		self.assertEquals(self.testObject.state, copyC)

	def test_makeMoveComplex(self):
		'''DynamicScriptingAI.makeMove works (with more complicated moves'''
		self.engine.gameMeta[self.game_id]["move"] = 2
		self.testObject.setState(self.stateD)
		copyD = np.copy(self.stateD)

		# Make sure the states are equal to start with
		self.assertEquals(self.testObject.state, copyD)

		self.testObject.makeMove()
		copyD[5, 0] = 0
		copyD[4, 1] = 0
		copyD[2, 3] = 0
		copyD[1, 4] = 2

		self.assertEquals(self.testObject.state, copyD)

	def test_analyzeStimuli(self):
		'''DynamicScriptingAI.analyzeStimuli works'''
		self.testObject.setState(self.stateA)
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:1])

		self.testObject.setState(self.stateB)
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:2])
