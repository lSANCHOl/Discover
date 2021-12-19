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


# Colours
BANNER = '\033[1;91m'
HEADER = '\033[95m'#!/usr/bin/python3

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


# Colours
BANNER = '\033[1;91m'
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
OKPINK = '\033[0;95m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# Banner
def banner():
    print('\n'+'-'*50)
    print(f'''{BANNER}{BOLD}░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█░█░█▀▀░█▀▄
░█░█░░█░░▀▀█░█░░░█░█░▀▄▀░█▀▀░█▀▄
░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀ By Sancho{ENDC}''')


def ping_sweep(cidr_network):
    print('-'*50)
    time.sleep(1)
    def worker():         
        global hosts
        global hostnames
        global macs
        hosts = []
        hostnames = []
        macs = [] 
        while True:
            target = q.get()
            send_ping(target)
            q.task_done()

    def send_ping(target):
        icmp = subprocess.Popen(['ping', '-c', '1', str(target)], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        with thread_lock:
            if '1 received' in icmp[0].decode('utf-8'):
                mac = os.popen(f'arp -a {str(target)} | cut -d " " -f 4').read()
                mac = mac.strip()  
                try:
                    hostname =  socket.gethostbyaddr(str(target)) 
                except:
                    hostname = ('','') 
                print(f'{OKGREEN}[+] {OKCYAN}{target} {OKPINK}{mac}{ENDC} ({OKCYAN}{hostname[0]}{ENDC})')
                hosts.append(target)
                hostnames.append(hostname[0])
                macs.append(mac)
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
    ip = ipaddress.ip_address(me)
    index = all_hosts.index(ip)
    del all_hosts[index] 

    print(f'Scanning network of: {WARNING}{cidr_network}{ENDC} [{BOLD}{OKPINK}{me}{ENDC}]')
    print(f'Time started: {BOLD}{str(datetime.now())}{ENDC}')
    print('-'*50)
    t1 = datetime.now()

    # send ten task requests to the worker
    for item in all_hosts:
        q.put(item)

    # block until all tasks are done
    q.join()
    
    t2 = datetime.now()
    total = t2 - t1
    print('-'*50)
    print(f'Scan completed in: {BOLD}{total}{ENDC}')
    print(f'Total of {OKGREEN}{len(hosts)}{ENDC} hosts up')
    print('-'*50)

def subnet_calc():
    addr = [0, 0, 0, 0]
    mask = [0, 0, 0, 0]
    cidr = 0
    (addr, cidr) = ip_cidr.split('/')
    addr = [int(x) for x in addr.split('.')]
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

ip_cidr = os.popen('ip address | grep brd | grep '+args.WifiCard+' | cut -d " " -f 6').read().strip()
me = os.popen('ip address | grep brd | grep '+args.WifiCard+' | cut -d / -f 1').read().strip().split(' ')[-1]


if __name__=='__main__':
    if args.quiet:
        one = 1
    else:
        banner()
    try:
        ping_sweep(subnet_calc()) 
        if args.list:
            file1 = open('ip_list.txt', 'w')    
            for i in range(len(hosts)):
                n = file1.write(f'{str(hosts[i])} \n')
            file1.close()
        elif args.all_list:
            file1 = open('all_list.txt', 'w')
            for i in range(len(hosts)):
                n = file1.write(f'{i+1}. {hosts[i]} {macs[i]} ({hostnames[i]})\n')
            file1.close()
    except KeyboardInterrupt:
        print('GoodBye!')
        sys.exit()


OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
OKPINK = '\033[0;95m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# Banner
def banner():
    print('\n'+'-'*50)
    print(f'''{BANNER}{BOLD}░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█░█░█▀▀░█▀▄
░█░█░░█░░▀▀█░█░░░█░█░▀▄▀░█▀▀░█▀▄
░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀ By Sancho{ENDC}''')


def ping_sweep(cidr_network):
    print('-'*50)
    time.sleep(1)
    def worker():         
        global hosts
        global hostnames
        global macs
        hosts = []
        hostnames = []
        macs = [] 
        while True:
            target = q.get()
            send_ping(target)
            q.task_done()

    def send_ping(target):
        icmp = subprocess.Popen(['ping', '-c', '1', str(target)], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        with thread_lock:
            if '1 received' in icmp[0].decode('utf-8'):
                mac = os.popen(f'arp -a {str(target)} | cut -d " " -f 4').read()
                mac = mac.strip()  
                try:
                    hostname =  socket.gethostbyaddr(str(target)) 
                except:
                    hostname = ('','') 
                print(f'{OKGREEN}[+] {OKCYAN}{target} {OKPINK}{mac}{ENDC} ({OKCYAN}{hostname[0]}{ENDC})')
                hosts.append(target)
                hostnames.append(hostname[0])
                macs.append(mac)
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
    ip = ipaddress.ip_address(me)
    index = all_hosts.index(ip)
    del all_hosts[index] 

    print(f'Scanning network of: {WARNING}{cidr_network}{ENDC} [{BOLD}{OKPINK}{me}{ENDC}]')
    print(f'Time started: {BOLD}{str(datetime.now())}{ENDC}')
    print('-'*50)
    t1 = datetime.now()

    # send ten task requests to the worker
    for item in all_hosts:
        q.put(item)

    # block until all tasks are done
    q.join()
    
    t2 = datetime.now()
    total = t2 - t1
    print('-'*50)
    print(f'Scan completed in: {BOLD}{total}{ENDC}')
    print(f'Total of {OKGREEN}{len(hosts)}{ENDC} hosts up')
    print('-'*50)

def subnet_calc():
    addr = [0, 0, 0, 0]
    mask = [0, 0, 0, 0]
    cidr = 0
    (addr, cidr) = ip_cidr.split('/')
    addr = [int(x) for x in addr.split('.')]
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

ip_cidr = os.popen('ip address | grep brd | grep '+args.WifiCard+' | cut -d " " -f 6').read().strip()
me = os.popen('ip address | grep brd | grep '+args.WifiCard+' | cut -d / -f 1').read().strip().split(' ')[-1]


if __name__=='__main__':
    if args.quiet:
        one = 1
    else:
        banner()
    try:
        ping_sweep(subnet_calc()) 
        if args.list:
            file1 = open('ip_list.txt', 'w')    
            for i in range(len(hosts)):
                n = file1.write(f'{str(hosts[i])} \n')
            file1.close()
        elif args.all_list:
            file1 = open('all_list.txt', 'w')
            for i in range(len(hosts)):
                n = file1.write(f'{i+1}. {hosts[i]} {macs[i]} ({hostnames[i]})\n')
            file1.close()
    except KeyboardInterrupt:
        print('GoodBye!')
        sys.exit()

