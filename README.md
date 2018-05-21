1029_crack.py

"Cracks" Event ID 1029 hashes, given a starting hash and a list of usernames

Thanks to reddit's /u/RedPh0enix and /u/Belgarion0 for basically everything.

https://www.reddit.com/r/AskNetsec/comments/8kid7k/microsoft_rdp_logs_base64sha256username/

They did all the hard work and figured out Microsoft's formatting.


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
