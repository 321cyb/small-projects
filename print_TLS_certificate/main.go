package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
        "log"
)

func main() {
	config := tls.Config{InsecureSkipVerify: true}
	conn, err := tls.Dial("tcp", "cis.citrix.com:443", &config)
	if err != nil {
		log.Fatalf("client: dial: %s", err)
	}
	defer conn.Close()
	log.Println("client: connected to: ", conn.RemoteAddr())

	state := conn.ConnectionState()
	for _, v := range state.PeerCertificates {
		fmt.Println(v.Subject)
		fmt.Println(x509.MarshalPKIXPublicKey(v.PublicKey))
		fmt.Println("")
	}
	log.Println("client: handshake: ", state.HandshakeComplete)
	log.Println("client: mutual: ", state.NegotiatedProtocolIsMutual)

	log.Print("client: exiting")
}
