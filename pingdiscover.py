import argparse
import ipaddress
import asyncio
import logging
import time

import aioping


logger = logging.getLogger(__name__)


async def do_ping(host, timeout):
    logger.debug(f"do_ping({host}, {timeout})")
    try:
        start_time = time.monotonic()
        delay = await aioping.ping(str(host), timeout=timeout)
        exec_time = time.monotonic() - start_time
        print(f"{host}: Ping response in {delay*1000:.0f} ms")
        logger.debug(f"{host}: Ping response in {delay} ms (exec time {exec_time})")
    except TimeoutError:
        exec_time = time.monotonic() - start_time
        print(f"{host}: Timed out")
        logger.debug(f"{host}: Timed out (exec time {exec_time})")


async def subscriber(queue, timeout):
    logger.debug("starting worker")
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

    # print(args)
    queue = asyncio.Queue(args.concurrency * 4)
    workers = [asyncio.create_task(subscriber(queue, args.timeout)) for i in range(args.concurrency)]

    for host in args.network:
        logger.debug(f"enqueueing host {host}")
        await queue.put(host)
    await queue.join()

    for task in workers:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG, )
    asyncio.run(main())
