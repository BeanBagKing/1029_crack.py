#!/usr/bin/python3

import hashlib
import base64
import traceback
import argparse

# Global colour variables
RED='\033[1;31m'
GRN='\033[1;32m'
YEL='\033[1;33m'
BLU='\033[1;34m'
GRY='\033[1;90m'
LRD='\033[1;41m' # Red Background, White Letters
NC='\033[0m' # No Color

def decode_event_1029_hash():
    '''
     Event ID 1029 hashes, given a starting hash and a list of usernames
     Thanks to reddit's /u/RedPh0enix and /u/Belgarion0 for basically everything.
     https://www.reddit.com/r/AskNetsec/comments/8kid7k/microsoft_rdp_logs_base64sha256username/
     They did all the hard work and figured out Microsoft's formatting.


     Sample - Psudocode would be better spelled out as Base64(SHA256binary(UTF-16LE(UserName))
     Event ID 1029 Description is = Base64(SHA256(UserName)) is = UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc=-

     username = "ServerUser01"
     username = username.decode('utf-8').encode('utf-16le')
     hash = hashlib.sha256(username).digest() # note NOT .hexdigest()
     print base64.b64encode(hash)

     --- Some Notable Hashes ---
     Administrator:	UmTGMgTFbA35+PSgMOoZ2ToPpAK+awC010ZOYWQQIfc=
     administrator:	WAlZ81aqzLQmoWEfQivmPQwJxIm/XQcDjplQdjznr5E=
     Guest:		EYafGFixlNF6rmWxFFF7o4CrI0VoyuqZr6O60Igzr0I=
     guest:		OsLcy6J+ON0FM13n1l5aMCOw8K4paLSthgtHiWDnGzk=
    '''

    # Instantiate argeparse Object
    parser = argparse.ArgumentParser(description='Event ID 1029 hashes', 
             formatter_class=argparse.RawDescriptionHelpFormatter)

    # Add parser Arguments
    parser.add_argument('--hash',
                        '-H',
                        type=str,
                        required=True,
                        help='The hash to crack')
    
    parser.add_argument('--file',
                        '-f',
                        type=str,
                        required=True,
                        help='File of potential usernames')

    # Execute parse_args()
    args = parser.parse_args()

    # Assign input arguments to variables
    hash = args.hash
    wordlist = args.file

    # Check if hash supplied by user are bytes, if not then convert
    if isinstance(hash, bytes):
        pass
    else:
        hash = bytes(hash, 'utf-8')

    # Check that hash supplied by user is in correct format (Base64)
    if base64.b64encode(base64.b64decode(hash)) == hash:
        pass
    else:
        print(RED + f"[*] " + NC + f"Hash does not appear to be valid base64")
        exit()

    # Iterate through username list
    with open(wordlist) as f:
        i = 0
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            try: # Found a string with invalid encoding breaks the script. Toss the user an error and continue
                username = line.encode('utf-16le')
            except:
                print(RED + f"[*] " + NC + f"An error occured with string: " + LRD + f"{line}. " + NC + f"Continuing...")
                traceback.print_exc()

            test = base64.b64encode(hashlib.sha256(username).digest()).strip()

            # For very long scripts, we may want status updates
            i += 1
            if i % 500000 == 0:                 
                print(YEL + f"[-] " + NC + f"Status update: {str(i)} names tested")
                print(YEL + f"[-] " + NC + f"Currently testing: {line}")
            
            # Check if hash matches supplied username
            if test == hash:
                print(GRN + f"[+] " + NC + f"Match Found")
                print(f"Hash: {test.decode('utf-8')}")
                print(f"Username: {line}")
                exit()
        print(BLU + f"[-] " + NC +  f"Sorry, nothing found")

        return()

if __name__ == '__main__':

    decode_event_1029_hash()
