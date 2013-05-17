package main

//LImitations: tcp.stream can't be too big, seq and ack can't be too big.
//Right now don't consider ack.



import (
    "fmt"
    "log"
    "os"
    "os/exec"
    "flag"
//    "time"
    "runtime"
    "strconv"
    "strings"
    "io/ioutil"
)


type tcpPacket struct {
    seq uint32
    ack uint32
    next_seq uint32
}

type tcpConnection struct {
    one_direction []tcpPacket
    the_other_direction []tcpPacket
    ip_src             string
}


type bigTcpPacket struct {
    seq uint64
    ack uint64
    next_seq uint64
}

func split_streams(out string) (streams map[uint32]tcpConnection){
    var line string
    var m   =  make(map[uint32]tcpConnection)

    //TODO: better handling this.
    lines := strings.Split(out, "\n")
    for i := range lines {
        line = lines[i]

        if line == "" {
            continue
        }
        fields := strings.Split(line, "\t")

        if len(fields) < 5  {
            fmt.Printf("Wrong line: %v\n", line)
            continue
        }

        tcp_stream_index,_ := strconv.ParseUint(fields[0], 10, 32)
        tcp_seq, _         := strconv.ParseUint(fields[1], 10, 32)
        tcp_ack, _         := strconv.ParseUint(fields[2], 10, 32)
        tcp_nxtseq, _      := strconv.ParseUint(fields[3], 10, 32)

        ip_src           := fields[4]
        tcp_packet := tcpPacket{seq: uint32(tcp_seq), ack: uint32(tcp_ack), next_seq: uint32(tcp_nxtseq)}


        conn, ok := m[uint32(tcp_stream_index)]
        if ok {
            if ip_src == conn.ip_src {
                conn.one_direction = append(conn.one_direction, tcp_packet)
            } else {
                conn.the_other_direction = append(conn.the_other_direction, tcp_packet)
            }
            m[uint32(tcp_stream_index)] = conn
        } else {
            tmp := *new(tcpConnection)
            tmp.ip_src = ip_src
            tmp.one_direction = append(tmp.one_direction, tcp_packet)
            m[uint32(tcp_stream_index)] = tmp
        }
    }

    return m
}


func get_tshark_output(tshark_path *string, pcap_path string) string{
    temp_file, err := ioutil.TempFile("", "")
    if err != nil {
        log.Fatal(err)
        return ""
    }

    temp_file_name := temp_file.Name()
    err = temp_file.Close()
    if err != nil {
        log.Fatal(err)
        return ""
    }

    fmt.Printf("Copyright @ Chen Yabo, If any problem, please contact me.")
    fmt.Printf("using wireshark to generate information to file %s\n", temp_file_name)
    fmt.Printf("Please be patient, this normally takes several minutes.\n" )
    fmt.Println("")

    //We absolutely trust wireshark can manage TCP streams well.
    out, err := exec.Command(*tshark_path, "-T", "fields", "-e", "tcp.stream", "-e", "tcp.seq", "-e", "tcp.ack", "-e", "tcp.nxtseq", "-e", "ip.src",  "-r", pcap_path, "-R", "tcp.len>0").Output()
    if err != nil {
        log.Fatal(err)
    }

    ioutil.WriteFile(temp_file_name, out, 0644)

    return string(out)
}


func sort_and_unique_one_side(one_side []tcpPacket) {
    AscByField(one_side, "seq")
    for index := 1; index < len(one_side); index++ {
        if one_side[index] == one_side[index-1] {
            one_side = append(one_side[:index], one_side[index+1:]...)
        }
    }
}


func sort_and_unique_tcpConnection(tcpConnections map[uint32]tcpConnection) {
    for _, conn := range tcpConnections {
        sort_and_unique_one_side(conn.one_direction)
        sort_and_unique_one_side(conn.the_other_direction)
    }
}


func calc_stats(tcpConnections map[uint32]tcpConnection) (uint64, uint64){
    var total uint64
    var loss  uint64
    for index, conn := range tcpConnections {
        fmt.Printf("starting to analyze tcp_stream: %v ... \n", index)
        total_of_conn, loss_of_conn := calc_one_connection(conn)
        fmt.Printf("for tcp_stream[%v], expect %v bytes, %v bytes lost\n", index, total_of_conn, loss_of_conn)
        total += uint64(total_of_conn)
        loss  += uint64(loss_of_conn)
    }
    return total, loss
}


//LIMITATION: assume one_side can have no more than 1G bytes.
func calc_one_side(one_side []tcpPacket, the_other_side []tcpPacket) (uint32, uint32) {
    var total_of_this_side, loss_of_this_side uint32

    if len(one_side) > 1 {
        var wraps_around bool = false
        var max_seq_val uint32 = 0
        var min_seq_val uint32 = 0xFFFFFFFF

        for index := range one_side {
            if max_seq_val < one_side[index].seq {
                max_seq_val = one_side[index].seq
            }

            if min_seq_val > one_side[index].seq {
                min_seq_val = one_side[index].seq
            }
        }

        if (max_seq_val > 0xC0000000) && (min_seq_val < 0x40000000) {
            wraps_around = true
        }

        if wraps_around {
            fmt.Printf("WARNING, invalid input from tshark.")
            fmt.Println(one_side)
            total_of_this_side = 0
            loss_of_this_side = 0
        } else {
            total_of_this_side = one_side[len(one_side) - 1].next_seq - one_side[0].seq

            for index := 1; index <  len(one_side); index++ {
                if one_side[index].seq != one_side[index-1].next_seq {
                    //More than 0x1FFFF bytes are lost in a row, unlikely.
                    if (one_side[index].seq - one_side[index-1].next_seq) < 0x1FFFF {
                        loss_of_this_side += (one_side[index].seq - one_side[index-1].next_seq)
                    }
                }
            }
        }
    } else if len(one_side) == 1 {
        if (one_side[0].seq > 0xFFFF0000) && (one_side[0].next_seq < 0xFFFF) {
            total_of_this_side = one_side[0].next_seq + (0xFFFFFFFF - one_side[0].seq) + 1
        } else {
            total_of_this_side = one_side[0].next_seq - one_side[0].seq
        }
    }

    if (total_of_this_side > 0x80000000) || (loss_of_this_side > 0x80000000) {
        fmt.Printf("WARNING, invalid input from tshark.")
        fmt.Println(one_side)
        total_of_this_side = 0
        loss_of_this_side = 0
    }
    return total_of_this_side, loss_of_this_side
}


func calc_one_connection(conn tcpConnection) (uint32, uint32) {
    total_of_side1, loss_of_side1 := calc_one_side(conn.one_direction, conn.the_other_direction)
    total_of_side2, loss_of_side2 := calc_one_side(conn.the_other_direction, conn.one_direction)
    return total_of_side1 + total_of_side2, loss_of_side1 + loss_of_side2
}


func usage() {
    fmt.Fprintf(os.Stderr, "Usage for %v:\n", os.Args[0])
    fmt.Fprintf(os.Stderr, "%v [flags]  /path/to/pcap\n", os.Args[0])
    flag.PrintDefaults()
    os.Exit(2)
}

func main() {
    var tshark_path *string
    var pcap_path  string
    if "windows" == runtime.GOOS {
        tshark_path = flag.String("tshark-path", "C:\\Program Files (x86)\\Wireshark\\tshark.exe", "path to tshark")
    } else if "linux" == runtime.GOOS {
        tshark_path = flag.String("tshark-path", "/usr/sbin/tshark", "path to tshark")
    }

    flag.Usage = usage
    flag.Parse()

    if len(flag.Args()) != 1 {
        usage()
    } else {
        pcap_path =  flag.Arg(0) 
    }


//    fmt.Println("start tshark, current time is", time.Now().String())

    out := get_tshark_output(tshark_path, pcap_path)

//    fmt.Println("tshark over, current time is", time.Now().String())

    streams := split_streams(out)

    sort_and_unique_tcpConnection(streams)

    total, loss := calc_stats(streams)

    fmt.Println("")
    fmt.Println("FINAL RESULT IS:")
    fmt.Printf("totally expect %v bytes, %v bytes lost, loss rate is %f%%\n", total, loss, float64(loss) / float64(total) * 100.0)

//    fmt.Println("program over, current time is", time.Now().String())
}
