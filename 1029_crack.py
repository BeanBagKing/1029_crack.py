#!/usr/bin/python
import hashlib,base64

# "Cracks" Event ID 1029 hashes, given a starting hash and a list of usernames
# Thanks to reddit's /u/RedPh0enix and /u/Belgarion0 for basically everything.
# They did all the hard work and figured out Microsoft's formatting.
#
#
# Sample - Psudocode would be better spelled out as Base64(SHA256binary(UTF-16LE(UserName))
# Event ID 1029 Description is = Base64(SHA256(UserName)) is = UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc=-
#
# username = "ServerUser01"
# username = username.decode('utf-8').encode('utf-16le')
# hash = hashlib.sha256(username).digest() # note NOT .hexdigest()
# print base64.b64encode(hash)
#
# --- Some Notable Hashes ---
# Administrator:	UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc=
# administrator:	WAlZ81aqzLQmoWEfQivmPQwJxIm/XQcDjplQdjznr5E=
# Guest:		EYafGFixlNF6rmWxFFF7o4CrI0VoyuqZr6O60Igzr0I=
# guest:		OsLcy6J+ON0FM13n1l5aMCOw8K4paLSthgtHiWDnGzk=
#

# Relace these two variables with your own
hash = "UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc=-"
wordlist = "/usr/share/wordlists/rockyou.txt"

if base64.b64encode(base64.b64decode(hash)) == hash:
	pass;
else:
	print "Hash does not appear to be valid base64"
	print "To force continue, comment out exit() below"
	exit()

with open(wordlist) as f:
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		username = line.decode('utf-8').encode('utf-16le')
		test = hashlib.sha256(username).digest().encode('base64').strip()
		test = test.strip() # not sure why, but we get a line break added, so .strip()
		if test == hash:
			print "Hash: " + test
			print "Username: " + line
			exit()
	print "Sorry, nothing found"
