#!/usr/bin/python3

import os, types, uuid
import json, bson, hjson

class FakeDB:
	datadir = ""
	readflag = "r"
	writeflag = "w"
	fileformat = ".json"
	codec = None
	def __init__(self, directory="./data", jsonformat="json"):
		self.datadir = os.path.abspath(directory)
		if(jsonformat == "json"):
			self.codec = json
		elif(jsonformat == "bson"):
			self.codec = bson
			self.readflag = "rb"
			self.writeflag = "wb"
		elif(jsonformat == "hjson"):
			self.codec = hjson
		
		self.fileformat = jsonformat if jsonformat.startswith(".") else "." + jsonformat
	
	def write(self, body, name):
		if not name.endswith(self.fileformat):
			name += self.fileformat
		outfile = os.path.join(self.datadir, name)
		
		if(os.path.isfile(outfile)):
			with open(outfile, self.readflag) as f:
				oldfile = self.codec.loads(f.read())
				try:
					if(body['revision'] != oldfile['revision']):
						return ""
				except KeyError:
					return ""
		
		body["revision"] = uuid.uuid4().hex
		
		os.makedirs(os.path.dirname(outfile), exist_ok=True)
		with open(outfile, self.writeflag) as f:
			f.write(self.codec.dumps(body))
		return body["revision"]
	
	def read(self, name=""):
		if not name.endswith(self.fileformat):
			name += self.fileformat
		infile = os.path.join(self.datadir, name)
		
		with open(infile, self.readflag) as f:
			if(os.path.isfile(infile)):
				return self.codec.loads(f.read())
			else:
				return ""


if __name__ == "__main__":
	a = FakeDB(jsonformat="json")
	
	testdoc = {"a":1, "b":2, "c":3}
	a.write(testdoc, "test")
	
	testdoc = a.read("test")
	testdoc["a"] += 1
	testdoc["b"] += 2
	testdoc["c"] += 3
	a.write(testdoc, "test")
	print(testdoc)
