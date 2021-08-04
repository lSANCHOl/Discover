#!/usr/bin/python3

from datetime import datetime
import threading        
import queue           
import ipaddress       
import subprocess      
import time            
import argparse
import os
import sys
import socket


def banner():
    print('\n'+'-'*50)
    print('''╔═╗╦╔╗╔╔═╗  ┌─┐┌─┐┌─┐┌┐┌┌┐┌┌─┐┬─┐
╠═╝║║║║║ ╦  └─┐│  ├─┤││││││├┤ ├┬┘
╩  ╩╝╚╝╚═╝  └─┘└─┘┴ ┴┘└┘┘└┘└─┘┴└─By Sancho''')


def ping_sweep(cidr_network):
    print("-"*50)
    def worker():         
        global hosts
        global hostnames
        #global macs
        hosts = []
        hostnames = []
        #macs = []
        while True:
            target = q.get()
            send_ping(target)
            q.task_done()

    def send_ping(target):
        icmp = subprocess.Popen(['ping', '-c', '1', str(target)], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        with thread_lock:
            if "1 received" in icmp[0].decode('utf-8'):
                try:
                    hostname =  socket.gethostbyaddr(str(target)) 
                except:
                    hostname = 'unknown' 
                print(f'[+] {target} ({hostname[0]}) is UP')
                hosts.append(target)
                hostnames.append(hostname[0])       
    # Define a print lock
    thread_lock = threading.Lock()

    # Create our queue
    q = queue.Queue()

    # Define number of threads
    for r in range(100):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    # Network to scan
    all_hosts = list(ipaddress.ip_network(cidr_network).hosts())
    print(f'Scanning network of: {cidr_network}')
    print(f'Time started: {str(datetime.now())}')
    print('-'*50)
    t1 = datetime.now()

    # send ten task requests to the worker
    for item in all_hosts:
        q.put(item)

    # block until all tasks are done
    q.join()
    
    t2 = datetime.now()
    total = t2 - t1

    print(f'Ping scan completed in {total}')
    print('-'*50)
    print(f'Total of {len(hosts)} hosts up')
    print('-'*50)

def subnet_calc(ip_cidr):
    addr = [0, 0, 0, 0]
    mask = [0, 0, 0, 0]
    cidr = 0
    (addr, cidr) = ip_cidr.split('/')
    addr = [int(x) for x in addr.split(".")]
    cidr = int(cidr)
    mask = [( ((1<<32)-1) << (32-cidr) >> i ) & 255 for i in reversed(range(0, 32, 8))]
    netw = [addr[i] & mask[i] for i in range(4)]
    network = '.'.join(map(str, netw))
    final = str(network)+'/'+str(cidr)
    return(final)


parser = argparse.ArgumentParser(description='Scan for devices on a network using pings')
parser.add_argument('-q', '--quiet', action='store_true', help='don\'t display banner')
parser.add_argument('-w', '--WifiCard', metavar='', help='Specify NIC to use')
parser.add_argument('-l', '--list', action='store_true', help='Save IP\'s to a list')
parser.add_argument('-a', '--all_list', action='store_true', help='Save IP\'s, and hostnames to a list')
args = parser.parse_args()

ip_cidr = os.popen('ip address | grep brd | grep '+args.WifiCard+' | cut -d \" \" -f 6').read()
ip_cidr = ip_cidr.rstrip()

if __name__=="__main__":
    if args.quiet:
        one = 1
    else:
        banner()
    try:
        ping_sweep(subnet_calc(ip_cidr)) 
        if args.list:
            file1 = open('ip_list.txt', 'w')    
            for i in range(len(hosts)):
                n = file1.write(f'{str(hosts[i])} \n')
            file1.close()
        elif args.all_list:
            file1 = open('all_list.txt', 'w')
            for i in range(len(hosts)):
                n = file1.write(f'[+] {str(hosts[i])} ({str(hostnames[i])})\n')
            file1.close()
    except KeyboardInterrupt:
        print('GoodBye!')
        sys.exit()

