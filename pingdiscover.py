import argparse
import asyncio
import aioping


async def do_ping(host):
    try:
        delay = await aioping.ping(host) * 1000
        print("Ping response in %s ms" % delay)

    except TimeoutError:
        print("Timed out")


def main():
    parser = argparse.ArgumentParser(description='Ping all hosts within the given subnet')
    parser.add_argument('subnet', help='Subnet + netmask. E.g. "192.168.0.0/24"')
    parser.add_argument('--concurrency', '--jobs', '-c', '-j', type=int, default=1,
                        help="number of concurrent hosts that are pinged at the same time")
    parser.add_argument('--timeout', '-t', type=float, default=5,
                        help="the number of seconds after giving up on pinging a host (default 5s)")
    args = parser.parse_args()

    print(args)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_ping("8.8.8.8"))


if __name__ == "__main__":
    main()
