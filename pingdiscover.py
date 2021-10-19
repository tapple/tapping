import argparse
import ipaddress
import asyncio
import aioping


async def do_ping(host, timeout):
    try:
        delay = await aioping.ping(host, timeout=timeout) * 1000
        print("Ping response in %s ms" % delay)

    except TimeoutError:
        print("Timed out")


async def main():
    parser = argparse.ArgumentParser(description='Ping all hosts within the given subnet')
    parser.add_argument('network', type=ipaddress.ip_network, help='Subnet + netmask. E.g. "192.168.0.0/24"')
    parser.add_argument('--concurrency', '--jobs', '-c', '-j', type=int, default=1,
                        help="number of concurrent hosts that are pinged at the same time")
    parser.add_argument('--timeout', '-t', type=float, default=5,
                        help="the number of seconds after giving up on pinging a host (default 5s)")
    args = parser.parse_args()

    print(args)

    for host in args.network:
        await do_ping(str(host), args.timeout)


if __name__ == "__main__":
    asyncio.run(main())
