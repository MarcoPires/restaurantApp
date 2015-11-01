import os
from restaurantApp import app
from restaurantApp import config
from werkzeug import secure_filename
from hashlib import md5
from time import localtime

def allowedFile(filename):
	"""Checks allowed file extension"""
	ALLOWED_EXTENSIONS = set(config.data["allowed_extensions"])
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def getFilesFolder():
	"""Returns the file full path"""
	return os.path.join( config.data["read_folder"] )


def uploadImage(file):
	"""Save image"""
	if file and allowedFile(file.filename):
		file.filename = fileName( file.filename.rsplit('.', 1)[1] )
		filename = secure_filename(file.filename)
		filePath = os.path.join( app.config['UPLOAD_FOLDER'], filename )
		file.save( filePath )
		return file.filename
	return None


def fileName(extension):
	"""Generate new file name"""
	return "%s.%s" % (md5(str(localtime())).hexdigest(), extension )