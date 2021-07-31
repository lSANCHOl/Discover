# ping-scanner
Discover devices on a network using the ICMP protocol


<p align="center">
    <img alt="ViewCount" src="https://views.whatilearened.today/views/github/lSANCHOl/ping-scanner.svg">
</p>

Usage:
```
usage: ping-scanner [-h] [-q] [-w] [-l] [-a]

Scan for devices on a network using pings

optional arguments:
  -h, --help        show this help message and exit
  -q, --quiet       don't display banner
  -w , --WifiCard   Specify NIC to use
  -l, --list        Save IP's to a list
  -a, --all_list    Save IP's, and hostnames to a list
  ```
 
Example:
```
python3 ping-scanner.py -w <NIC> -l
```
