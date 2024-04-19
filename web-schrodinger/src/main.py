#!/bin/pytho

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from subprocess import check_output, CalledProcessError, STDOUT
from zipfile import is_zipfile
import os
import shutil

ALLOWED_EXTENSIONS = {"zip"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "ignoreThisNotUseful"

class UploadFileForm(FlaskForm):
	file = FileField("File", validators=[InputRequired()])
	submit = SubmitField("Upload File")

@app.route('/', methods=["GET", "POST"])

def home():
	form = UploadFileForm()
	if form.validate_on_submit():

		# save file that was uploaded
		file = form.file.data
		file_base = os.path.abspath(os.path.dirname(__file__))
		file_path = os.path.join(file_base,
			                     secure_filename(file.filename))
		file.save(file_path)

		# Want to make sure the file is a ZIP file
		file_contents = ""
		if is_zipfile(file_path):
			try:
				check_output(["unzip", "-q", file_path, "-d", "files/"], stderr=STDOUT)
			except:
				file_contents = "Could not unzip, you sure this is a valid ZIP file?"

			for filename in os.listdir("files"):
				filename = os.path.basename(os.path.normpath(filename))
				try:
					single_file = open(f"files/{filename}", "r", encoding="utf-8", errors="strict")
					file_contents += "-" * 15 + filename + "-" * 15 + "\n\n"
					file_contents += single_file.read() + "\n\n"
					single_file.close()

				except UnicodeDecodeError:
					file_contents += "Data is not human-readable\n\n"
				except:
					file_contents += "Something went wrong...\n\n"

				if os.path.isdir(f"files/{filename}") and not os.path.islink(f"files/{filename}"):
					shutil.rmtree(f"files/{filename}")
				else:
					os.remove(f"files/{filename}")
		else:
			file_contents = "This is not a ZIP file!"

		# whether the file is a ZIP file or not, the file is no longer needed
		# at this point
		os.remove(file_path)

		return(render_template("file_upload.html", content=file_contents))

	return(render_template("index.html", form=form))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=9000)