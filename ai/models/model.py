# Rushy Panchal
# ai/models/model.py

import mongokit

class Model(mongokit.Document, object):
	'''Base class for all Models'''
	__database__ = "senior_focus"

	use_dot_notation = True
	skip_validation = True

	@staticmethod
	def autosave(func):
		'''Returns a decorated function to add implicit saving'''
		def decorated(self, *args, **kwargs):
			shouldSave = False
			saveProvided = "save" in kwargs
			# autosave if user wants to save OR if no save parameter provided
			if ((saveProvided and kwargs["save"]) or not saveProvided):
				shouldSave = True
			if saveProvided:
				del kwargs["save"]
			returnValue = func(self, *args, **kwargs)
			if shouldSave:
				self.save()
			return returnValue
		return decorated

class CustomTypeBase(mongokit.CustomType, object):
	'''Base class for a custom Mongokit type'''
	mongo_type = None
	python_type = None
	init_type = None

	def to_bson(self, value):
		'''Converts Python object to BSON'''
		return value

	def to_python(self, value):
		'''Converts BSON to a Python object'''
		return value
