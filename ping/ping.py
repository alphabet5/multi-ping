# multi-ping: a simple script to ping multiple devices and display the status.
# Copyright (C) 2022  John Burt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from rich import console

console = console.Console()
import argparse
from rich.live import Live
from rich.table import Table
import time
import re
import subprocess
from rich.text import Text
import platform
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import socket
import os
import sys
import ipaddress
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from textual.containers import Container
import asyncio


def get_color(value, minLatency, maxLatency):
    """Returns a color string interpolated through green->yellow->red based on the value."""
    if value == "!":
        return "rgb(255,51,51)"

    value = min(max(value, minLatency), maxLatency)
    ratio = (value - minLatency) / (maxLatency - minLatency)

    if ratio < 0.5:  # Green to Yellow
        r = int(51 + (255 - 51) * (ratio * 2))
        g = 255
        b = 51
    else:  # Yellow to Red
        r = 255
        g = int(255 - (255 - 51) * ((ratio - 0.5) * 2))
        b = 51

    return f"rgb({r},{g},{b})"


def ping_device(name, host, maxLatency, interval):
    # threading.Timer(interval=interval, function=ping_device, args=[host, maxLatency, interval]).start()
    error = ""
    try:
        ipaddress.ip_address(host)
    except:
        return name, "!", f"Invalid IP address, {host}"
    if platform.system() != "Windows":
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(maxLatency), host], capture_output=True
        )
        parse = re.compile(r".*time=(\d+\.\d+) ms")
        if result.stdout == b"":
            error = result.stderr.decode("utf-8").strip()
        try:
            latency = float(parse.search(str(result.stdout)).group(1))
        except:
            latency = "!"
    else:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", str(maxLatency), host], capture_output=True
        )
        parse = re.compile(r".*Maximum = (\d*)ms")
        try:
            latency = float(parse.search(str(result.stdout)).group(1))
        except:
            latency = "!"
    return name, latency, error


def generate_table(minLatency, maxLatency) -> Table:
    global hosts
    table = Table()
    table.add_column("Hostname/IP")
    table.add_column("Ping Status", justify="right", width=50, no_wrap=True)
    table.add_column("Error")

    for name, h in hosts.items():
        text = Text()
        for ping in h["pings"]:
            if ping != "!":
                text.append("|", style=get_color(ping, minLatency, maxLatency))
            else:
                text.append("!", style="rgb(255,51,51)")
        table.add_row(name, text, h["error"])
    return table


def check_host(host, domains):
    try:
        addr = socket.gethostbyname(host)
        return addr
    except:
        for domain in domains:
            try:
                addr = socket.gethostbyname(host + "." + domain)
                return addr
            except:
                pass
    return "NXDOMAIN"


hosts = dict()
executor = ThreadPoolExecutor(max_workers=10)


def main():
    global hosts
    parser = argparse.ArgumentParser(
        description="Ping multiple hosts and display the results in a table."
    )
    parser.add_argument(
        "--maxLatency",
        help="The maximum latency for coloring and icmp timeout.",
        default=1000,
        type=int,
    )
    parser.add_argument(
        "--minLatency", help="The minimum latency for coloring.", default=40, type=int
    )
    parser.add_argument(
        "--interval", help="The interval to ping the devices.", default=1, type=int
    )
    parser.add_argument(
        "--domain",
        help="Append domain if the host doesn't resolve. Default=[] or PNG_APPEND_DOMAINS",
        default=[],
        type=str,
        action="append",
    )
    parser.add_argument(
        "hosts", help="Hostnames to ping.", type=str, nargs=argparse.REMAINDER
    )
    args = vars(parser.parse_args())

    if args["domain"] == []:
        domains = os.getenv("PNG_APPEND_DOMAINS", "").split(",")
    else:
        domains = args["domain"]
    for h in args["hosts"]:
        if h not in hosts:
            if h[:1] == "/":
                hosts[h] = {"addr": "/", "pings": list(), "error": "", "last_start": 0}
            else:
                hosts[h] = {
                    "addr": check_host(h, domains),
                    "pings": list(),
                    "error": "",
                    "last_start": 0,
                }
    table = generate_table(args["minLatency"], args["maxLatency"])
    active_futures = list()
    exe = ThreadPoolExecutor(max_workers=50)

    with Live(table, refresh_per_second=4) as live:
        while True:
            for host, h in hosts.items():
                if (
                    time.time() - h["last_start"] > args["interval"]
                    and h["addr"] != "/"
                ):
                    hosts[host]["last_start"] = time.time()
                    active_futures.append(
                        exe.submit(
                            ping_device,
                            host,
                            h["addr"],
                            args["maxLatency"],
                            args["interval"],
                        )
                    )
            for future in active_futures:
                try:
                    if future.done():
                        host, latency, error = future.result()
                        pings = hosts[host]["pings"][-49:]
                        pings.append(latency)
                        hosts[host]["pings"] = pings
                        if error:
                            hosts[host]["error"] = error
                        active_futures.remove(future)
                except:
                    import traceback

                    print(traceback.format_exc())
                    active_futures.remove(future)
            try:
                time.sleep(0.1)
                table = generate_table(args["minLatency"], args["maxLatency"])
                live.update(table)
            except KeyboardInterrupt:
                sys.exit(0)


if __name__ == "__main__":
    main()
