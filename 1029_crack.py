#!/usr/bin/python3
import hashlib,base64,traceback

# "Cracks" Event ID 1029 hashes, given a starting hash and a list of usernames
# Thanks to reddit's /u/RedPh0enix and /u/Belgarion0 for basically everything.
# https://www.reddit.com/r/AskNetsec/comments/8kid7k/microsoft_rdp_logs_base64sha256username/
# They did all the hard work and figured out Microsoft's formatting.
#
#
# Sample - Pseudocode would be better spelled out as Base64(SHA256binary(UTF-16LE(UserName))
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

# Replace these two variables with your own
hash = "UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc="
wordlist = "/mnt/c/Tools/1029crack/rockyou.txt" # Dear God don't actually use this, it's just here for a placeholder

RED='\033[1;31m'
GRN='\033[1;32m'
YEL='\033[1;33m'
BLU='\033[1;34m'
GRY='\033[1;90m'
LRD='\033[1;41m' # Red Background, White Letters
NC='\033[0m' # No Color

if str(base64.b64encode(base64.b64decode(hash)), 'utf-8') == hash:
	pass;
else:
	print("Hash does not appear to be valid base64")
	print("To force continue, comment out exit() below this line in the script")
	exit()

with open(wordlist) as f:
	i = 0
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		try: # Found a string with invalid encoding breaks the script. Toss the user an error and containue
			username = line.encode('utf-16le')
		except:
			print(LRD + "An error occured with string:" + NC + " " + line + " " + LRD + "Continuing..." + NC)
			traceback.print_exc()
		test = hashlib.sha256(username).digest()
		test = base64.b64encode(test).strip()
		test = test.strip() # not sure why, but we get a line break added, so .strip()
		test = str(test, 'utf-8')
		print(test)
		i += 1
		if i % 50000 == 0: # For very long scripts, we may want status updates
			print(YEL + "Status update: " + str(i) + " names tested" + NC)
			print(YEL + "Currently testing: " + line + NC)
		if test == hash:
			print(GRN + "--- MATCH FOUND ---" + NC)
			print(GRN + "Hash: " + test + NC)
			print(GRN + "Username: " + line + NC)
			exit()
	print(BLU + "Sorry, nothing found" + NC)
