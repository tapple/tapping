import argparse
import ipaddress
import asyncio
import aioping



async def do_ping(host, timeout):
    try:
        delay = await aioping.ping(host, timeout=timeout) * 1000
        print(f"{host}: Ping response in {delay} ms")
    except TimeoutError:
        print(f"{host}: Timed out")


async def publisher(queue, network):
    for host in network:
        await queue.put(host)


async def subscriber(queue, timeout):
    while True:
        host = await queue.get()
        await do_ping(host, timeout)
        queue.task_done()


async def main():
    parser = argparse.ArgumentParser(description='Ping all hosts within the given subnet')
    parser.add_argument('network', type=ipaddress.ip_network, help='Subnet + netmask. E.g. "192.168.0.0/24"')
    parser.add_argument('--concurrency', '--jobs', '-c', '-j', type=int, default=1,
                        help="number of concurrent hosts that are pinged at the same time")
    parser.add_argument('--timeout', '-t', type=float, default=5,
                        help="the number of seconds after giving up on pinging a host (default 5s)")
    args = parser.parse_args()

    print(args)
    queue = asyncio.Queue(args.concurrency * 4)
    pub = asyncio.create_task(publisher(queue, args.network))
    workers = [asyncio.create_task(subscriber(queue, args.timeout)) for i in range(args.concurrency)]

    await pub
    await queue.join()
    for task in workers:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
