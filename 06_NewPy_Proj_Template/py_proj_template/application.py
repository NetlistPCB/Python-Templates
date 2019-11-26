import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
from . import views as v
from . import models as m
from tkinter import messagebox


class Application(tk.Tk):
	""" Application root window """

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.title("ABQ Data Entry Application")
		self.resizable(width=False, height=False)

		ttk.Label(
			self,
			text="ABQ Data Entry Application",
			font=("TkDefaultFont", 16)
		).grid(row=0)

		datestring = datetime.today().strftime("%Y-%m-%d")
		defaultFilename = "abq_data_record_{}.csv".format(datestring)
		self.filename = tk.StringVar(value=defaultFilename)

		self.settingsModel = m.SettingsModel()
		self.loadSettings()

		#~ self.settings = {
			#~ 'autofill date': tk.BooleanVar(),
			#~ 'autofill sheet data': tk.BooleanVar()
		#~ }

		self.callbacks = {
			'file->select': self.onFileSelect,
			'file->quit': self.quit
		}

		menu = v.MainMenu(self, self.settings, self.callbacks)
		self.config(menu=menu)

		self.recordform = v.DataRecordForm(self, m.CSVModel.fields, self.settings)
		self.recordform.grid(row=1, padx=10)

		self.savebutton = ttk.Button(self, text="Save", command=self.onSave)
		self.savebutton.grid(sticky="e", row=2, padx=10)

		# status bar
		self.status = tk.StringVar()
		self.statusbar = ttk.Label(self, textvariable=self.status)
		self.statusbar.grid(sticky="we", row=3, padx=10)

		self.records_saved = 0

	def loadSettings(self):
		""" Load settings into self.settings dict. """

		varTypes = {
		'bool': tk.BooleanVar,
		'str': tk.StringVar,
		'int': tk.IntVar,
		'float': tk.DoubleVar
		}

		self.settings = {}
		for key, data in self.settingsModel.variables.items():
			varType = varTypes.get(data['type'], tk.StringVar)
			self.settings[key] = varType(value=data['value'])

		for var in self.settings.values():
			var.trace('w', self.saveSettings)

	def saveSettings(self, *args):
		""" Save the current settings to a preferences file. """

		for key, variable in self.settings.items():
			self.settingsModel.set(key, variable.get())
		self.settingsModel.save()

	def onSave(self):
		""" Handles save button clicks """

		# Check for errors first
		message = "Cannot save record"
		errors = self.recordform.get_errors()
		if errors:
			detail = "The following fields have errors: \n  * {}".format('\n  * '.join(errors.keys()))
			self.status.set(
				"Cannot save, error in fields: {}"
				.format(', '.join(errors.keys()))
			)
			messagebox.showerror(title='Error', message=message, detail=detail)
			return False

		# For now, we save to a hardcoded filename with a datestring.
		# If it doesnt' exist, create it,
		# otherwise just append to the existing file
		filename = self.filename.set(filename)
		model = m.CSVModel(filename)

		data = self.recordform.get()

		model.save_record(data)

		self.records_saved += 1
		self.status.set(
			"{} records saved this session".format(self.records_saved)
		)
		self.recordform.reset()

	def onFileSelect(self):
		""" Handle the file->select action from menu. """

		filename = filedialog.asksaveasfilename(
			title='Select the target file for saving records',
			defaultextension='.csv',
			filetypes=[('Comma-Separated Values', '*.csv *.CSV')]
		)

		if filename:
			self.filename.set(filename)
