import sys, time
import multiprocessing as mp
from socket import *

HOST = gethostbyname(gethostname())
PORT = 50007
PORT_COUNT = 200
BUFSIZE = 1024
INDEX = 1

# UDP Wait and Echo
def udp_echo(ipAddr, port):
    # create socket
    sokt = socket(AF_INET, SOCK_DGRAM)
    sokt.bind((gethostbyname(gethostname()), port))
    print '%s:%s' %(ipAddr, port)
    while True:
        data, addr = sokt.recvfrom(BUFSIZE)
        if addr is not ipAddr:
            sokt.sendto('ip address not correct', addr)
            exit()
        else:
            sokt.sendto('accept: %s' + data, addr)
            exit()


# Timeout thread connection
def timeout_connection(func, args = (), kwds = {}, timeout = 5, default = None):
    pool = mp.Pool(processes = 1)
    result = pool.apply_async(func, args = args, kwds = kwds)
    try:
        val = result.get(timeout = timeout)
    except mp.TimeoutError:
        pool.terminate()
        return default
    else:
        pool.close()
        pool.join()
        return val

def get_index():
    if INDEX <= PORT_COUNT:
        INDEX = INDEX + 1
        return INDEX
    else:
        INDEX = 1

def udp_server():
    index  = 1
    m_port = PORT
    sokt = socket(AF_INET, SOCK_DGRAM)
    sokt.bind((HOST, PORT))
    print 'udp server ready'
    while True:
        data, addr = sokt.recvfrom(BUFSIZE)
        if data is not None:
            print 'server received %s from %s' %(data, addr)
            m_port = m_port + index
            index = index + 1
            sokt.sendto('port: %s' %m_port, addr)
            timeout_connection(udp_echo(addr, m_port), args = (), kwds = {}, timeout = 5, default = 'timeout')

udp_server()
