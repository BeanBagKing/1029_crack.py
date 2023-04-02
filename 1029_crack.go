package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/binary"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"sync"
)

func main() {
	hashPtr := flag.String("hash", "", "a string")
	wordlistPtr := flag.String("wordlist", "", "a string")
	flag.Parse()
	fmt.Println("Hash Provided:",*hashPtr)
	fmt.Println("Wordlist:",*wordlistPtr)

	if *hashPtr == "" || *wordlistPtr == "" {
		fmt.Println("Usage:",os.Args[0],"-hash <hash> -wordlist <wordlist>")
		os.Exit(1)
	}

	content, err := ioutil.ReadFile(*wordlistPtr)
	if err != nil {
		panic(err)
	}

	lines := strings.Split(string(content), "\n")
	var wg sync.WaitGroup
	for _, line := range lines {
		wg.Add(1)
		go func(line string) {
			defer wg.Done()
			line = strings.TrimSpace(line)
			username := utf8ToUtf16le(line)
			test := sha256.Sum256(username)
			testBase64 := base64.StdEncoding.EncodeToString(test[:])
			if testBase64 == *hashPtr {
				fmt.Println("--- MATCH FOUND ---")
				fmt.Println("Hash: " + testBase64)
				fmt.Println("Username: " + line)
				os.Exit(0)
			}
		}(line)
	}
	wg.Wait()
	fmt.Println("Sorry, nothing found")
}

func utf8ToUtf16le(input string) []byte {
	var buffer bytes.Buffer
	for _, r := range input {
		if r <= 0xFFFF {
			binary.Write(&buffer, binary.LittleEndian, uint16(r))
		} else {
			r -= 0x10000
			highSurrogate := (r >> 10) | 0xD800
			lowSurrogate := (r & 0x3FF) | 0xDC00
			binary.Write(&buffer, binary.LittleEndian, highSurrogate)
			binary.Write(&buffer, binary.LittleEndian, lowSurrogate)
		}
	}
	return buffer.Bytes()
}
