package main

// This script is used to test S3 upload performance,
// You can tune object size, upload count and thread count
// to see their relations.

import (
	"fmt"
	"os"
	"strconv"
	"sync"
	"time"

	"launchpad.net/goamz/aws"
	"launchpad.net/goamz/s3"

	"github.com/gorilla/feeds"
)

var bytes []byte

const filetype = "application/octet-stream"

var bucket *s3.Bucket

func main() {
	objSize, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	cnt, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	threadCnt, err := strconv.Atoi(os.Args[3])
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	AWSAuth := aws.Auth{
		AccessKey: "<Your ID>", // change this to yours
		SecretKey: "<Your Secret>",
	}

	region := aws.USWest2
	// change this to your AWS region
	// click on the bucketname in AWS control panel and click Properties
	// the region for your bucket should be under "Static Website Hosting" tab

	connection := s3.New(AWSAuth, region)

	bucket = connection.Bucket("<Bukcet Name>") // change this your bucket name

	file, err := os.Open("/dev/urandom")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	bytes = make([]byte, objSize)
	if readCnt, err := file.Read(bytes); readCnt != objSize {
		fmt.Printf("read /dev/urandom error, %v\n", err)
		os.Exit(1)
	}

	file.Close()

	// start to run workers.
	ch := make(chan int)
	var wg sync.WaitGroup

	start := time.Now()

	for i := 0; i < threadCnt; i++ {
		wg.Add(1)
		go worker(ch, &wg)
	}

	for j := 0; j < cnt; j++ {
		ch <- j
	}

	close(ch)
	wg.Wait()

	t := time.Since(start)
	fmt.Printf("total spent time: %v\n", t)
}

func worker(ch chan int, wg *sync.WaitGroup) {
	for {
		_, ok := <-ch
		if ok {
			for i := 0; i < 3; i++ {
				if doUpload() == nil {
					break
				}
			}
		} else {
			wg.Done()
			break
		}
	}
}

func doUpload() error {
	path := feeds.NewUUID().String()
	err := bucket.Put(path, bytes, filetype, s3.BucketOwnerRead)

	// NOTE : If you get this error message
	// Get : 301 response missing Location header

	// this is because you are using the wrong region for the bucket
	// and if you want to figure out the bucket location automatically
	// see http://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETlocation.html
	// I've try it out with http.Get() and just getting the authenticating
	// requests part right is already too much
	// work for this tutorial.
	// See http://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html

	// UPDATE 15th Jan 2015: See http://camlistore.org/pkg/misc/amazon/s3/#Client.BucketLocation
	if err != nil {
		fmt.Println(err)
	}
	return err
}
