# tapping
Sample ping utility to practice with asyncio and networking

Pings all hosts in an ipv4 or ipv6 subnet

To create a virtual environment, and run without installing:

```bash
pipenv shell
sudo python pingdiscover/pingdiscover.py 192.168.1.0/25 --concurrency 8 --timeout 2
```

To install globally, use either pip or make:

```bash
sudo pip install .
sudo make install
sudo pingdiscover fe80::b9ac:3e4f:1c56:ad00/120 --concurrency 8 --timeout 2
```

Must be run as root on unix, but not on windows