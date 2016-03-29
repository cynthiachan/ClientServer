#!/usr/bin/env python

# Echo server program
import socket
import sys

type_ = '';
numprobes = 0;
protocol = '';
size = 0 ;
delay = 0;

def CTP(tokens,conn):
    if tokens[0] == 't':
        return "200 OK: Closing Connection\n"
    else:
        return "404 ERROR: Invalid Connection Termination Message\n"

def MP(tokens, data, expected):
    print ("tokens[1]: ", tokens[1])
    print ("expected: ", expected)
    if (not int(tokens[1]) == expected):
        return "404 ERROR: Invalid Measurement Message\n"
    else:
        return ("PROBE MESSAGE: " + str(data) + '\n')

def CSP(tokens) :
    #Parse input
    protocol = tokens[0]
    type_ = tokens[1]

    try:
        numprobes = int(tokens[2])
        size = int(tokens[3])
        delay = int(tokens[4])
    except ValueError:
        return "404 ERROR: Invalid Connection Setup Message\n"

    if type_ == 'rtt' or type_ == 'tput':
        return "200 OK: Ready\n";
    else:
        return "404 ERROR: Invalid Connection Setup Message\n"


if __name__ == "__main__":
    HOST = ''                 # Symbolic name meaning the local host
    PORT = int(sys.argv[1])              # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Create socket and bind to host on specified port
    s.bind((HOST, PORT))
    s.listen(1)
    print "Server Started"

    conn = 0

    expected = 0
    while 1:
        print "conn: "+str(conn)
        if conn == 0:
            conn, addr = s.accept()
            print 'Connected by', addr

        if conn != 0:

            data = []
            #data is the message being recieved from the client
            data.append(conn.recv(1024))
            print ('string is' + str(data))
            while data[-1][-1] != '\n':
                data.append(conn.recv(1024))

            print "Data Received:", data
            tokens = data[0].split()  #split data recieved into pieces by space

            #CSP
            if tokens[0] == 's': #if first character is s, then call connection setup phase
                m = CSP(tokens)
                conn.send(m)
                if m == "404 ERROR: Invalid Connection Setup Message\n":
                    conn.close()
                    conn = 0
                    expected = 0

            #MP
            if tokens[0] == 'm':
                print("Processing MP")
                expected += 1

                m = MP(tokens, data, expected)
                conn.send(m)
                if m == "404 ERROR: Invalid Measurement Message\n":
                    conn.close()
                    conn = 0
                    expected = 0


            #CTP
            if tokens[0] == 't':
                m = CTP(tokens,conn)
                conn.send(m)
                conn.close()
                conn = 0
                expected = 0
