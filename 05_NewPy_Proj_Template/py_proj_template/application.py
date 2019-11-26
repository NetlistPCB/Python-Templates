import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import views as v
from . import models as m


class Application(tk.Tk):
	"""Application root window"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.title("ABQ Data Entry Application")
		self.resizable(width=False, height=False)

		ttk.Label(
			self,
			text="ABQ Data Entry Application",
			font=("TkDefaultFont", 16)
		).grid(row=0)

		self.recordform = v.DataRecordForm(self, m.CSVModel.fields)
		self.recordform.grid(row=1, padx=10)

		self.savebutton = ttk.Button(self, text="Save", command=self.on_save)
		self.savebutton.grid(sticky="e", row=2, padx=10)

		# status bar
		self.status = tk.StringVar()
		self.statusbar = ttk.Label(self, textvariable=self.status)
		self.statusbar.grid(sticky="we", row=3, padx=10)

		self.records_saved = 0

	def on_save(self):
		"""Handles save button clicks"""

		# Check for errors first

		errors = self.recordform.get_errors()
		if errors:
			self.status.set(
				"Cannot save, error in fields: {}"
				.format(', '.join(errors.keys()))
			)
			return False

		# For now, we save to a hardcoded filename with a datestring.
		# If it doesnt' exist, create it,
		# otherwise just append to the existing file
		datestring = datetime.today().strftime("%Y-%m-%d")
		filename = "abq_data_record_{}.csv".format(datestring)
		model = m.CSVModel(filename)
		#~ newfile = not os.path.exists(filename)

		data = self.recordform.get()

		model.save_record(data)

		#~ with open(filename, 'a') as fh:
			#~ csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
			#~ if newfile:
				#~ csvwriter.writeheader()
			#~ csvwriter.writerow(data)

		self.records_saved += 1
		self.status.set(
			"{} records saved this session".format(self.records_saved)
		)
		self.recordform.reset()
