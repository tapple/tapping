import argparse
import ipaddress
import asyncio
from typing import Sequence, Awaitable
import logging
import time

import aioping  # type: ignore

logger = logging.getLogger(__name__)


async def do_ping(host: ipaddress.IPv4Address, timeout: float) -> None:
    """
    Ping the given host, and print the result
    :param host: address of the host to ping
    :param timeout: Wait this many seconds before giving up
    """
    logger.debug(f"do_ping({host}, {timeout})")
    start_time = time.monotonic()
    try:
        delay = await aioping.ping(str(host), timeout=timeout)
        print(f"{host}: Ping response in {delay * 1000:.0f} ms")
    except TimeoutError:
        print(f"{host}: Timed out")
    exec_time = time.monotonic() - start_time
    logger.debug(f"ping {host} executed in {exec_time}")


async def gather_with_concurrency(coroutines: Sequence[Awaitable], concurrency: int) -> tuple:
    """
    Run coroutines concurrently, but only concurrency at a time
    :param coroutines: list of coroutines to execute concurrently
    :param concurrency: the number of coroutines to run at once
    """
    sem = asyncio.Semaphore(concurrency)

    async def bound_task(coroutine: Awaitable):
        async with sem:
            return await coroutine

    bound_tasks = [bound_task(coroutine) for coroutine in coroutines]
    return await asyncio.gather(*bound_tasks)


async def main() -> None:
    """
    entry point for the program
    :return:
    """
    parser = argparse.ArgumentParser(description='Ping all hosts within the given subnet')
    parser.add_argument('network', type=ipaddress.ip_network, help='Subnet + netmask. E.g. "192.168.0.0/24"')
    parser.add_argument('--concurrency', '--jobs', '-c', '-j', type=int, default=1,
                        help="number of concurrent hosts that are pinged at the same time")
    parser.add_argument('--timeout', '-t', type=float, default=5,
                        help="the number of seconds after giving up on pinging a host (default 5s)")
    args = parser.parse_args()

    tasks = [do_ping(host, args.timeout) for host in args.network]
    await gather_with_concurrency(tasks, args.concurrency)


def run_main() -> None:
    """ Convenience method to start the async main function """
    # logging.basicConfig(level=logging.DEBUG, )
    asyncio.run(main())


if __name__ == "__main__":
    run_main()
