# DISCOVER
Discover who's on your network by pinging devices using the ICMP protocol


<p align="center">
    <img alt="ViewCount" src="https://views.whatilearened.today/views/github/lSANCHOl/ping-scanner.svg">
</p>

Dependencies:
  - <p> netifaces: <br> 
      - <a href='https://pypi.org/project/netifaces/'> PyPI </a> <br>
      - <a href='https://github.com/al45tair/netifaces'> GitHub </a> <br>
      - <a href='https://0xbharath.github.io/python-network-programming/libraries/netifaces/index.html'> documentation </a> <br>



Usage:
```
usage: discover [-h] [-q] [-w] [-l] [-a]

Scan for devices on a network using pings

optional arguments:
  -h, --help        show this help message and exit
  -q, --quiet       don't display banner
  -w , --WifiCard   Specify wifi card to use
  -l, --list        Save IP's to a list
  -a, --all_list    Save IP's, and hostnames to a list
  ```
 
Example:
```
python3 discover.py -w {iface} -a
```
