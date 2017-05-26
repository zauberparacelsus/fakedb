#!/usr/bin/python3

import os, types, uuid
import json, bson, hjson

from fcntl import flock, LOCK_EX, LOCK_NB, LOCK_UN


class FakeDB:
	datadir = ""
	readflag = "r"
	writeflag = "w"
	fileformat = ".json"
	test = 0
	codec = None
	def __init__(self, directory="./data", jsonformat="json"):
		self.test = 0
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
		
		#if(os.path.isfile(outfile)):
		try:
			with open(outfile, self.readflag) as f:
				try:
					flock(f, LOCK_EX | LOCK_NB)
				except:
					return None
				ignoreRev = False
				try:
					oldfile = self.codec.loads(f.read())
				except self.codec.decoder.JSONDecodeError:
					ignoreRev = True
				
				if(ignoreRev == False):
					try:
						if(body['revision'] != oldfile['revision']):
							flock(f, LOCK_UN)
							return None
					except KeyError:
						flock(f, LOCK_UN)
						pass
				flock(f, LOCK_UN)
		except IOError:
			pass
		
		body["revision"] = uuid.uuid4().hex
		
		if not os.path.exists(os.path.dirname(outfile)):
			os.makedirs(os.path.dirname(outfile))
		try:
			with open(outfile, self.writeflag) as f:
				try:
					flock(f, LOCK_EX | LOCK_NB)
				except BlockingIOError:
					return None
				#print(">> " + self.codec.dumps(body))
				f.write(self.codec.dumps(body))
				flock(f, LOCK_UN)
		except IOError:
			return None
		return body["revision"]
	
	def read(self, name=""):
		if not name.endswith(self.fileformat):
			name += self.fileformat
		infile = os.path.join(self.datadir, name)
		ret = None
		
		try:
			with open(infile, self.readflag) as f:
				data = f.read()
				try:
					ret = self.codec.loads(data)
				except self.codec.decoder.JSONDecodeError:
					pass
		except IOError:
			pass
		return ret


if __name__ == "__main__":
	a = FakeDB(jsonformat="hjson")
	
	testdoc = a.read("test")
	if(testdoc == None):
		testdoc = {"a":1, "b":2, "c":3}
	a.write(testdoc, "test")
	
	testdoc = a.read("test")
	
	testdoc["a"] += 1
	testdoc["b"] += 2
	testdoc["c"] += 3
	a.write(testdoc, "test")
	print(testdoc)
