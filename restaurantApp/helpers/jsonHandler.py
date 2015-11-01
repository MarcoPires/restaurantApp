import json

def loadsJSON(file):
	return json.loads( file )

def openLocalJSON(path):
	return loadsJSON( open( path,'r' ).read() )