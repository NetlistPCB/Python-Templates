""" This file contains data models. """
import csv
import os
import json
from .constants import FieldTypes as FT


class CSVModel:
	""" CSV File Storage """
	fields = {
	"Date": {'req': True, 'type': FT.iso_date_string},
	"Time": {'req': True, 'type': FT.string_list, 'values': ['8','12','16','20']},
	"Technician": {'req': True, 'type': FT.string},
	"Lab": {'req': True, 'type': FT.string_list, 'values': ['A','B','C','D','E']},
	"Plot": {'req': True, 'type': FT.string_list, 'values': [str(x) for x in range(1, 21)]},
	"Seed Sample": {'req': True, 'type': FT.string},
	"Humidity": {'req': True, 'type': FT.decimal, 'min': 0.5, 'max': 52.0, 'inc': 0.01},
	"Light": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 100.0, 'inc': 0.01},
	"Temperature": {'req': True, 'type': FT.decimal, 'min': 4, 'max': 40, 'inc': 0.01},
	"Equipment Fault": {'req': False, 'type': FT.boolean},
	"Plants": {'req': True, 'type': FT.integer, 'min': 0, 'max': 20},
	"Blossoms": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
	"Fruit": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
	"Min Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': 0.01},
	"Max Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': 0.01},
	"Median Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': 0.01},
	"Notes": {'req': False, 'type': FT.long_string}}

	def __init__(self, filename):
		self.filename = filename

	def save_record(self, data):
		""" Save a dict of data to the CSV file """

		newfile = not os.path.exists(self.filename)

		with open(self.filename, 'a') as fh:
			csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
			if newfile:
				csvwriter.writeheader()
			csvwriter.writerow(data)

class SettingsModel:
	""" A model for saving settings """

	variables = {
	'autofill date': {'type': 'bool', 'value': True},
	'autofill sheet data': {'type': 'bool', 'value': True}}
	# Variable, variable type, variable default value.

	def __init__(self, filename='abq_settings.json', path='~'):
		# Determine the file path.
		self.filepath = os.path.join(os.path.expanduser(path), filename)
		self.load()

		print(self.filepath)

	def load(self):
		""" Load the settings from the file. """

		# If the file doesn't exist, don't try to load it.
		if not os.path.exists(self.filepath):
			return

		# Open the file and read the raw values.
		with open(self.filepath, 'r') as fh:
			rawValues = json.loads(fh.read())

		# Don't implicitly trust the raw values.
		# But only get known keys.
		for key in self.variables:
			if key in rawValues and 'value' in rawValues[key]:
				rawValue = rawValues[key]['value']
				self.variables[key]['value'] = rawValue

	def save(self, settings=None):
		jsonString = json.dumps(self.variables)
		with open(self.filepath, 'w') as fh:
			fh.write(jsonString)

	def set(self, key, value):
		if (
		key in self.variables and
		type(value).__name__ == self.variables[key]['type']
		):
			self.variables[key]['value'] = value
		else:
			raise ValueError("Bad key or wrong variable type")
