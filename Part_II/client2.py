#Echo client program

import socket
import sys
import datetime
import random
import string
import time

#global variables
tokens = []
timing = [] #list of times
type_ =''
inputMsg = ''
host = ''
port = 0
numprobes = 0
size = 0
beginning = 0
finish = 0

def average_RTT(numprobes):
    #calculate RTT
    global timing
    global beginning
    global finish

    r_sum = 0
    for t in timing:
        r_sum += t
    r_sum = r_sum / len(timing)

    avg_rtt = (r_sum) * (10**(3)) #millisecs
    print("Average RTT in millisecs: ", avg_rtt)

def average_TPUT(size):
    #calculate TPUT

    r_sum = 0
    for t in timing:
        r_sum += (int(size)/ t)
    r_sum = r_sum / len(timing)

    avg_tput = r_sum
    print("Average Throughput in bits per second: ", avg_tput )# bits per sec

# Connection Termination Phase
def CTP(s):
    inputMsg = ''
    inputMsg = raw_input('Please enter a message to send to server:')
    s.send(inputMsg+'\n')

    data = []
    data.append(s.recv(1024))
    while data[-1][-1] != '\n':
        data.append(s.recv(1024))

    print 'Received From Server (CTP):', repr("".join(data))

# generateMsg - generates a randomly sized string for MP
def generateMsg(size):
    listOfChar = [random.choice(string.ascii_letters + string.digits)
           for n in range(size)]
    randomMsg = "".join(listOfChar)
    return randomMsg

# Measurement Phase
def MP(s, size):
    global numprobes, timing

    print ("Number of Probes: ",int(numprobes))
    for i in range(int(numprobes)):
        randomMsg = generateMsg(int(size))

        beginning = time.time() #start getting the time

        inputMsg = ("m " + str(i+1)+ " "+randomMsg+"\n")
        s.sendall(inputMsg)

        #retrieving data from server
        data = []
        data.append(s.recv(1024))
        while data[-1][-1] != '\n':
            data.append(s.recv(1024))

        data = ' '.join(data)
        if data == '404 ERROR: Invalid Measurement Message\n':
            s.close()
            exit(1)
        print 'Received from server: (MP)', repr(data)

        finish = time.time() #end getting the time
        timing += [finish - beginning]




# Connection Setup Phase
def CSP(s):
    global numprobes, type_, size

    inputMsg = ''
    print('Please enter a setup message in the format:')
    print('<PROTOCOL PHASE> <MEASUREMENT TYPE> <NUMBER OF PROBES> <MESSAGE SIZE> <SERVER DELAY>')
    inputMsg = raw_input('Enter your message: ')
    s.send(inputMsg + '\n')

    data = []
    data.append(s.recv(1024))
    while data[-1][-1] != '\n':
        data.append(s.recv(1024))

    print 'Received From Server: (CSP)', repr("".join(data))

    #Setup was ok, so we can parse the message and store variables
    tokens = inputMsg.split()
    type_ = tokens[1]
    numprobes = tokens[2]
    size = tokens[3]

# main method
if __name__ == "__main__":
    HOST = sys.argv[1]    # The remote host
    PORT = int(sys.argv[2])  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create socket and bind to host on specified port

    s.connect((HOST, PORT)) #connect with host and port
    CSP(s)
    MP(s, size)
    CTP(s)
    s.close() #close connection

    if type_ == 'rtt':
        average_RTT(numprobes)
    elif type_ == 'tput':
        average_TPUT(size)
