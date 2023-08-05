# pr0cks
python script to transparently forward all TCP traffic through a socks (like ssh -D option) or HTTPS (CONNECT) proxy using iptables -j REDIRECT target. Only works on linux for now.

## Features :
- set up a local transparent proxy compatible with socks4 socks5 and HTTP CONNECT proxies allowing to forward any TCP traffic transparently using iptables
<!-- TODO make sure this works
- set up a local transparent DNS proxy translating UDP port 53 requests to TCP allowing DNS traffic to go through a proxy without UDP support (like ssh -D option)
- DNS caching mechanism to speed up the DNS resolutions through pr0cks
-->
# Usage example: let's rock
As an example we will use the socks5 proxy of openssh (the option -D)
```bash
$ ssh -D 1080 user@sshserver
```
then you can add some iptables rules :
```bash
$ iptables -t nat -A OUTPUT ! -d <my_ssh_server_IP>/32 -o eth0 -p tcp -m tcp -j REDIRECT --to-ports 10080
```
then start pr0cks :
```bash
$ pr0cks --proxy SOCKS5:127.0.0.1:1080
```
All your TCP traffic and DNS traffic should now pass through the ssh server kinda like if you had setup a tun VPN through ssh but without admin rights on the server !
#help
```text
pr0cks -h
usage: procks [-h] [--type {HTTP,SOCKS4,SOCKS5}] [-p PORT] [-n] [-v] [-c]
              [--username USERNAME] [--password PASSWORD]
              proxy_addr proxy_port

Transparent SOCKS5/SOCKS4/HTTP_CONNECT Proxy

positional arguments:
  proxy_addr
  proxy_port

optional arguments:
  -h, --help            show this help message and exit
  --type {HTTP,SOCKS4,SOCKS5}
                        The type of proxy to forward the traffic to
  -p PORT, --port PORT  port to bind the transparent proxy on the local socket
                        (default 10080)
  -n, --nat             set bind address to 0.0.0.0 to make pr0cks work from a
                        netfilter FORWARD rule instead of OUTPUT
  -v, --verbose         print all the connections requested through the proxy
  -c, --no-cache        don't cache dns requests
  --username USERNAME   Username to authenticate with to the server. The
                        default is no authentication.
  --password PASSWORD   Only relevant when a username has been provided
```

# Dependencies
- tested with Python 3.6

# TODO
- support UDP (with socks5)
- support proxy chaining


Don't hesitate to send me your feedback or any issue you may find

I hope it will be useful to someone ! Have fun :)
