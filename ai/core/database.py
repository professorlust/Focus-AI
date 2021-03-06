# Rushy Panchal
# ai/core/database.py

import mongokit
import numpy as np

from models.rule import Rule
from models.state import Gamestate

import config

converter = Gamestate()

class Database(mongokit.Connection):
	'''Specific database wrapper for a MongoDB database'''
	def getStimuli(self):
		'''Get all of the stimuli from the database'''
		cursor = self.Rule.find({}, {"condition": 1})
		return map(lambda rule: rule.condition, list(cursor))

	def getMatchingRules(self, state, stimuli, piece):
		'''Finds the rules matching the patterns'''
		if len(stimuli) > 0 and isinstance(stimuli[0], np.ndarray):
			stimuli = map(converter.to_bson, stimuli)
		results = list(self.Rule.find({
			"condition": {"$in": stimuli},
			"piece": {"$in": [piece, -piece, 0]},
			}).sort("combinedWeight", -1).limit(config.RULE_MATCHES))
		results.sort(key = lambda item: Gamestate.compare(state, item.state) * item.strength, reverse = True)
		# both the state similarity and strength are required in the sorting
		return results

	def newRule(self, *args, **kwargs):
		'''Creates a new Rule in the database'''
		rule = self.Rule.new(*args, **kwargs)
		return rule
