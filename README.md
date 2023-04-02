1029_crack.py  
"Cracks" Event ID 1029 hashes, given a starting hash and a list of usernames  
Thanks to reddit's /u/RedPh0enix and /u/Belgarion0 for basically everything.  
https://www.reddit.com/r/AskNetsec/comments/8kid7k/microsoft_rdp_logs_base64sha256username/  
They did all the hard work and figured out Microsoft's formatting.

**Update 1 Jun 2022 - Updated for Python 3**
**Update 1 Apr 2023 - Update to add Golang script, see very bottom*

Sample - Psudocode would be better spelled out as Base64(SHA256binary(UTF-16LE(UserName))  
Event ID 1029 Description is **Base64(SHA256(UserName)) is = UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc=-**

Manual calculation of a hash can be done using the below:
```
import hashlib,base64
username = "ServerUser01"
username = username.decode('utf-8').encode('utf-16le')
hash = hashlib.sha256(username).digest() # note NOT .hexdigest()
print base64.b64encode(hash)
```

--- Some Notable Hashes ---  
Administrator:	UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc=  
administrator:	WAlZ81aqzLQmoWEfQivmPQwJxIm/XQcDjplQdjznr5E=  
Guest:		EYafGFixlNF6rmWxFFF7o4CrI0VoyuqZr6O60Igzr0I=  
guest:		OsLcy6J+ON0FM13n1l5aMCOw8K4paLSthgtHiWDnGzk= 

#### m91029.pm - Hashcat test_module added 7/15/2021
I thought about opening a seperate repo for this, and if I do figure out how to build a proper hashcat plugin I will.
However, I felt like this script is more appropriate here as it gives a sample in another language (Perl).

For usage, reference the Hashcat Test Suite: https://github.com/hashcat/hashcat/blob/master/docs/hashcat-plugin-development-guide.md#test-suite

Nearly everything you would need to incorporate this into your own script is on line 21 though.

**Update 1 Apr 2023 - Update to add Golang script*
Playing around with ChatGPT/Bing Chat and writing code, used this one as a simple test case. It got a lot of things wrong, but in a lot of places got it close enough that I could fix the logic errors or the order of operations wtihout really knowing the language. It's pretty incredible. 

New changes are command line flags, e.g. it should now be run as:

`go run .\1029_crack.go -hash UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc= -wordlist C:\Users\Mike\Downloads\rockyou.txt`

or compiled with `go build` into an executable that you can run. This version is much faster.
 
