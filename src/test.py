#!/usr/bin/python3

import os, sys, time, random
from fakedb import FakeDB
from multiprocessing import Pool

def Tester(name, rounds=100):
	fails = 0
	session = FakeDB(directory="/tmp/fakedb", jsonformat="hjson")
	for value in range(0, rounds+1):
		while(True):
			testdoc = session.read("test2")
			testdoc[name] = value
			result = session.write(testdoc, "test2")
			if(result != None):
				break
		testdoc = session.read("test2")
		try:
			if(testdoc[name] != value):
				fails += 1
		except:
			fails += 1
	return fails

if(True):
	path = os.path.join("/tmp/fakedb", "test2.hjson")
	if os.path.isfile(path):
		os.remove(path)
	tempsession = FakeDB(directory="/tmp/fakedb", jsonformat="hjson")
	testdoc = {}
	tempsession.write(testdoc, "test2.hjson")

names = ["a", "b", "c", "d", "e", "f", "g", "h"]

rounds = 100
pool = Pool(processes=len(names))
print("Total Failures: {0} / {1}".format(sum(pool.map(Tester, names, rounds)), rounds * len(names)))
