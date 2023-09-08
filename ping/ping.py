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

import rich
from rich import console
console = console.Console()
import argparse
from rich.live import Live
from rich.table import Table
import time
import re
import threading
from queue import Queue #, Empty
import subprocess
from rich.text import Text
import platform

def get_color(value, minLatency, maxLatency):
    colors = {
        408: "rgb(255,51,51)",
        407: "rgb(255,52,51)",
        406: "rgb(255,53,51)",
        405: "rgb(255,54,51)",
        404: "rgb(255,55,51)",
        403: "rgb(255,56,51)",
        402: "rgb(255,57,51)",
        401: "rgb(255,58,51)",
        400: "rgb(255,59,51)",
        399: "rgb(255,60,51)",
        398: "rgb(255,61,51)",
        397: "rgb(255,62,51)",
        396: "rgb(255,63,51)",
        395: "rgb(255,64,51)",
        394: "rgb(255,65,51)",
        393: "rgb(255,66,51)",
        392: "rgb(255,67,51)",
        391: "rgb(255,68,51)",
        390: "rgb(255,69,51)",
        389: "rgb(255,70,51)",
        388: "rgb(255,71,51)",
        387: "rgb(255,72,51)",
        386: "rgb(255,73,51)",
        385: "rgb(255,74,51)",
        384: "rgb(255,75,51)",
        383: "rgb(255,76,51)",
        382: "rgb(255,77,51)",
        381: "rgb(255,78,51)",
        380: "rgb(255,79,51)",
        379: "rgb(255,80,51)",
        378: "rgb(255,81,51)",
        377: "rgb(255,82,51)",
        376: "rgb(255,83,51)",
        375: "rgb(255,84,51)",
        374: "rgb(255,85,51)",
        373: "rgb(255,86,51)",
        372: "rgb(255,87,51)",
        371: "rgb(255,88,51)",
        370: "rgb(255,89,51)",
        369: "rgb(255,90,51)",
        368: "rgb(255,91,51)",
        367: "rgb(255,92,51)",
        366: "rgb(255,93,51)",
        365: "rgb(255,94,51)",
        364: "rgb(255,95,51)",
        363: "rgb(255,96,51)",
        362: "rgb(255,97,51)",
        361: "rgb(255,98,51)",
        360: "rgb(255,99,51)",
        359: "rgb(255,100,51)",
        358: "rgb(255,101,51)",
        357: "rgb(255,102,51)",
        356: "rgb(255,103,51)",
        355: "rgb(255,104,51)",
        354: "rgb(255,105,51)",
        353: "rgb(255,106,51)",
        352: "rgb(255,107,51)",
        351: "rgb(255,108,51)",
        350: "rgb(255,109,51)",
        349: "rgb(255,110,51)",
        348: "rgb(255,111,51)",
        347: "rgb(255,112,51)",
        346: "rgb(255,113,51)",
        345: "rgb(255,114,51)",
        344: "rgb(255,115,51)",
        343: "rgb(255,116,51)",
        342: "rgb(255,117,51)",
        341: "rgb(255,118,51)",
        340: "rgb(255,119,51)",
        339: "rgb(255,120,51)",
        338: "rgb(255,121,51)",
        337: "rgb(255,122,51)",
        336: "rgb(255,123,51)",
        335: "rgb(255,124,51)",
        334: "rgb(255,125,51)",
        333: "rgb(255,126,51)",
        332: "rgb(255,127,51)",
        331: "rgb(255,128,51)",
        330: "rgb(255,129,51)",
        329: "rgb(255,130,51)",
        328: "rgb(255,131,51)",
        327: "rgb(255,132,51)",
        326: "rgb(255,133,51)",
        325: "rgb(255,134,51)",
        324: "rgb(255,135,51)",
        323: "rgb(255,136,51)",
        322: "rgb(255,137,51)",
        321: "rgb(255,138,51)",
        320: "rgb(255,139,51)",
        319: "rgb(255,140,51)",
        318: "rgb(255,141,51)",
        317: "rgb(255,142,51)",
        316: "rgb(255,143,51)",
        315: "rgb(255,144,51)",
        314: "rgb(255,145,51)",
        313: "rgb(255,146,51)",
        312: "rgb(255,147,51)",
        311: "rgb(255,148,51)",
        310: "rgb(255,149,51)",
        309: "rgb(255,150,51)",
        308: "rgb(255,151,51)",
        307: "rgb(255,152,51)",
        306: "rgb(255,153,51)",
        305: "rgb(255,154,51)",
        304: "rgb(255,155,51)",
        303: "rgb(255,156,51)",
        302: "rgb(255,157,51)",
        301: "rgb(255,158,51)",
        300: "rgb(255,159,51)",
        299: "rgb(255,160,51)",
        298: "rgb(255,161,51)",
        297: "rgb(255,162,51)",
        296: "rgb(255,163,51)",
        295: "rgb(255,164,51)",
        294: "rgb(255,165,51)",
        293: "rgb(255,166,51)",
        292: "rgb(255,167,51)",
        291: "rgb(255,168,51)",
        290: "rgb(255,169,51)",
        289: "rgb(255,170,51)",
        288: "rgb(255,171,51)",
        287: "rgb(255,172,51)",
        286: "rgb(255,173,51)",
        285: "rgb(255,174,51)",
        284: "rgb(255,175,51)",
        283: "rgb(255,176,51)",
        282: "rgb(255,177,51)",
        281: "rgb(255,178,51)",
        280: "rgb(255,179,51)",
        279: "rgb(255,180,51)",
        278: "rgb(255,181,51)",
        277: "rgb(255,182,51)",
        276: "rgb(255,183,51)",
        275: "rgb(255,184,51)",
        274: "rgb(255,185,51)",
        273: "rgb(255,186,51)",
        272: "rgb(255,187,51)",
        271: "rgb(255,188,51)",
        270: "rgb(255,189,51)",
        269: "rgb(255,190,51)",
        268: "rgb(255,191,51)",
        267: "rgb(255,192,51)",
        266: "rgb(255,193,51)",
        265: "rgb(255,194,51)",
        264: "rgb(255,195,51)",
        263: "rgb(255,196,51)",
        262: "rgb(255,197,51)",
        261: "rgb(255,198,51)",
        260: "rgb(255,199,51)",
        259: "rgb(255,200,51)",
        258: "rgb(255,201,51)",
        257: "rgb(255,202,51)",
        256: "rgb(255,203,51)",
        255: "rgb(255,204,51)",
        254: "rgb(255,205,51)",
        253: "rgb(255,206,51)",
        252: "rgb(255,207,51)",
        251: "rgb(255,208,51)",
        250: "rgb(255,209,51)",
        249: "rgb(255,210,51)",
        248: "rgb(255,211,51)",
        247: "rgb(255,212,51)",
        246: "rgb(255,213,51)",
        245: "rgb(255,214,51)",
        244: "rgb(255,215,51)",
        243: "rgb(255,216,51)",
        242: "rgb(255,217,51)",
        241: "rgb(255,218,51)",
        240: "rgb(255,219,51)",
        239: "rgb(255,220,51)",
        238: "rgb(255,221,51)",
        237: "rgb(255,222,51)",
        236: "rgb(255,223,51)",
        235: "rgb(255,224,51)",
        234: "rgb(255,225,51)",
        233: "rgb(255,226,51)",
        232: "rgb(255,227,51)",
        231: "rgb(255,228,51)",
        230: "rgb(255,229,51)",
        229: "rgb(255,230,51)",
        228: "rgb(255,231,51)",
        227: "rgb(255,232,51)",
        226: "rgb(255,233,51)",
        225: "rgb(255,234,51)",
        224: "rgb(255,235,51)",
        223: "rgb(255,236,51)",
        222: "rgb(255,237,51)",
        221: "rgb(255,238,51)",
        220: "rgb(255,239,51)",
        219: "rgb(255,240,51)",
        218: "rgb(255,241,51)",
        217: "rgb(255,242,51)",
        216: "rgb(255,243,51)",
        215: "rgb(255,244,51)",
        214: "rgb(255,245,51)",
        213: "rgb(255,246,51)",
        212: "rgb(255,247,51)",
        211: "rgb(255,248,51)",
        210: "rgb(255,249,51)",
        209: "rgb(255,250,51)",
        208: "rgb(255,251,51)",
        207: "rgb(255,252,51)",
        206: "rgb(255,253,51)",
        205: "rgb(255,254,51)",
        204: "rgb(255,255,51)",
        203: "rgb(254,255,51)",
        202: "rgb(253,255,51)",
        201: "rgb(252,255,51)",
        200: "rgb(251,255,51)",
        199: "rgb(250,255,51)",
        198: "rgb(249,255,51)",
        197: "rgb(248,255,51)",
        196: "rgb(247,255,51)",
        195: "rgb(246,255,51)",
        194: "rgb(245,255,51)",
        193: "rgb(244,255,51)",
        192: "rgb(243,255,51)",
        191: "rgb(242,255,51)",
        190: "rgb(241,255,51)",
        189: "rgb(240,255,51)",
        188: "rgb(239,255,51)",
        187: "rgb(238,255,51)",
        186: "rgb(237,255,51)",
        185: "rgb(236,255,51)",
        184: "rgb(235,255,51)",
        183: "rgb(234,255,51)",
        182: "rgb(233,255,51)",
        181: "rgb(232,255,51)",
        180: "rgb(231,255,51)",
        179: "rgb(230,255,51)",
        178: "rgb(229,255,51)",
        177: "rgb(228,255,51)",
        176: "rgb(227,255,51)",
        175: "rgb(226,255,51)",
        174: "rgb(225,255,51)",
        173: "rgb(224,255,51)",
        172: "rgb(223,255,51)",
        171: "rgb(222,255,51)",
        170: "rgb(221,255,51)",
        169: "rgb(220,255,51)",
        168: "rgb(219,255,51)",
        167: "rgb(218,255,51)",
        166: "rgb(217,255,51)",
        165: "rgb(216,255,51)",
        164: "rgb(215,255,51)",
        163: "rgb(214,255,51)",
        162: "rgb(213,255,51)",
        161: "rgb(212,255,51)",
        160: "rgb(211,255,51)",
        159: "rgb(210,255,51)",
        158: "rgb(209,255,51)",
        157: "rgb(208,255,51)",
        156: "rgb(207,255,51)",
        155: "rgb(206,255,51)",
        154: "rgb(205,255,51)",
        153: "rgb(204,255,51)",
        152: "rgb(203,255,51)",
        151: "rgb(202,255,51)",
        150: "rgb(201,255,51)",
        149: "rgb(200,255,51)",
        148: "rgb(199,255,51)",
        147: "rgb(198,255,51)",
        146: "rgb(197,255,51)",
        145: "rgb(196,255,51)",
        144: "rgb(195,255,51)",
        143: "rgb(194,255,51)",
        142: "rgb(193,255,51)",
        141: "rgb(192,255,51)",
        140: "rgb(191,255,51)",
        139: "rgb(190,255,51)",
        138: "rgb(189,255,51)",
        137: "rgb(188,255,51)",
        136: "rgb(187,255,51)",
        135: "rgb(186,255,51)",
        134: "rgb(185,255,51)",
        133: "rgb(184,255,51)",
        132: "rgb(183,255,51)",
        131: "rgb(182,255,51)",
        130: "rgb(181,255,51)",
        129: "rgb(180,255,51)",
        128: "rgb(179,255,51)",
        127: "rgb(178,255,51)",
        126: "rgb(177,255,51)",
        125: "rgb(176,255,51)",
        124: "rgb(175,255,51)",
        123: "rgb(174,255,51)",
        122: "rgb(173,255,51)",
        121: "rgb(172,255,51)",
        120: "rgb(171,255,51)",
        119: "rgb(170,255,51)",
        118: "rgb(169,255,51)",
        117: "rgb(168,255,51)",
        116: "rgb(167,255,51)",
        115: "rgb(166,255,51)",
        114: "rgb(165,255,51)",
        113: "rgb(164,255,51)",
        112: "rgb(163,255,51)",
        111: "rgb(162,255,51)",
        110: "rgb(161,255,51)",
        109: "rgb(160,255,51)",
        108: "rgb(159,255,51)",
        107: "rgb(158,255,51)",
        106: "rgb(157,255,51)",
        105: "rgb(156,255,51)",
        104: "rgb(155,255,51)",
        103: "rgb(154,255,51)",
        102: "rgb(153,255,51)",
        101: "rgb(152,255,51)",
        100: "rgb(151,255,51)",
        99: "rgb(150,255,51)",
        98: "rgb(149,255,51)",
        97: "rgb(148,255,51)",
        96: "rgb(147,255,51)",
        95: "rgb(146,255,51)",
        94: "rgb(145,255,51)",
        93: "rgb(144,255,51)",
        92: "rgb(143,255,51)",
        91: "rgb(142,255,51)",
        90: "rgb(141,255,51)",
        89: "rgb(140,255,51)",
        88: "rgb(139,255,51)",
        87: "rgb(138,255,51)",
        86: "rgb(137,255,51)",
        85: "rgb(136,255,51)",
        84: "rgb(135,255,51)",
        83: "rgb(134,255,51)",
        82: "rgb(133,255,51)",
        81: "rgb(132,255,51)",
        80: "rgb(131,255,51)",
        79: "rgb(130,255,51)",
        78: "rgb(129,255,51)",
        77: "rgb(128,255,51)",
        76: "rgb(127,255,51)",
        75: "rgb(126,255,51)",
        74: "rgb(125,255,51)",
        73: "rgb(124,255,51)",
        72: "rgb(123,255,51)",
        71: "rgb(122,255,51)",
        70: "rgb(121,255,51)",
        69: "rgb(120,255,51)",
        68: "rgb(119,255,51)",
        67: "rgb(118,255,51)",
        66: "rgb(117,255,51)",
        65: "rgb(116,255,51)",
        64: "rgb(115,255,51)",
        63: "rgb(114,255,51)",
        62: "rgb(113,255,51)",
        61: "rgb(112,255,51)",
        60: "rgb(111,255,51)",
        59: "rgb(110,255,51)",
        58: "rgb(109,255,51)",
        57: "rgb(108,255,51)",
        56: "rgb(107,255,51)",
        55: "rgb(106,255,51)",
        54: "rgb(105,255,51)",
        53: "rgb(104,255,51)",
        52: "rgb(103,255,51)",
        51: "rgb(102,255,51)",
        50: "rgb(101,255,51)",
        49: "rgb(100,255,51)",
        48: "rgb(99,255,51)",
        47: "rgb(98,255,51)",
        46: "rgb(97,255,51)",
        45: "rgb(96,255,51)",
        44: "rgb(95,255,51)",
        43: "rgb(94,255,51)",
        42: "rgb(93,255,51)",
        41: "rgb(92,255,51)",
        40: "rgb(91,255,51)",
        39: "rgb(90,255,51)",
        38: "rgb(89,255,51)",
        37: "rgb(88,255,51)",
        36: "rgb(87,255,51)",
        35: "rgb(86,255,51)",
        34: "rgb(85,255,51)",
        33: "rgb(84,255,51)",
        32: "rgb(83,255,51)",
        31: "rgb(82,255,51)",
        30: "rgb(81,255,51)",
        29: "rgb(80,255,51)",
        28: "rgb(79,255,51)",
        27: "rgb(78,255,51)",
        26: "rgb(77,255,51)",
        25: "rgb(76,255,51)",
        24: "rgb(75,255,51)",
        23: "rgb(74,255,51)",
        22: "rgb(73,255,51)",
        21: "rgb(72,255,51)",
        20: "rgb(71,255,51)",
        19: "rgb(70,255,51)",
        18: "rgb(69,255,51)",
        17: "rgb(68,255,51)",
        16: "rgb(67,255,51)",
        15: "rgb(66,255,51)",
        14: "rgb(65,255,51)",
        13: "rgb(64,255,51)",
        12: "rgb(63,255,51)",
        11: "rgb(62,255,51)",
        10: "rgb(61,255,51)",
        9: "rgb(60,255,51)",
        8: "rgb(59,255,51)",
        7: "rgb(58,255,51)",
        6: "rgb(57,255,51)",
        5: "rgb(56,255,51)",
        4: "rgb(55,255,51)",
        3: "rgb(54,255,51)",
        2: "rgb(53,255,51)",
        1: "rgb(52,255,51)",
        0: "rgb(51,255,51)",
    }
    if value <= minLatency:
        return colors[0]
    elif value >= maxLatency:
        return colors[408]
    else:
        return colors[int(408 * ((value - minLatency) / (maxLatency - minLatency)))]

def ping_device(host, maxLatency, interval, q):
    threading.Timer(interval=interval, function=ping_device, args=[host, maxLatency, interval, q]).start()
    if platform.system() != 'Windows':
        result = subprocess.run(['ping', '-c', '1', '-W', str(maxLatency), host], capture_output=True)
        parse = re.compile(r".*time=(\d+\.\d+) ms")
        if result.stdout == b'':
            print("Error with host " + host + " :" + result.stderr)
        try:
            latency = float(parse.search(str(result.stdout)).group(1))
        except:
            latency = '!'
    else:
        result = subprocess.run(['ping', '-n', '1', '-w', str(maxLatency), host], capture_output=True)
        parse = re.compile(r".*Maximum = (\d*)ms")
        try:
            latency = float(parse.search(str(result.stdout)).group(1))
        except:
            latency = '!'
    q.put((host, latency))


def generate_table(hosts, q, minLatency, maxLatency) -> Table:

    while not q.empty():
        host, latency = q.get()
        if len(hosts[host]) > 50:
            hosts[host].pop(0)
            hosts[host].append(latency)
        else:
            hosts[host].append(latency)
    table = Table()
    table.add_column("Hostname/IP")
    table.add_column("Ping Status", justify="right", min_width=50)

    for host, pings in hosts.items():
        text = Text()
        for ping in pings:
            if ping != '!':
                text.append('|', style=get_color(ping, minLatency, maxLatency))
            else:
                text.append('!', style="rgb(255,51,51)")
        table.add_row(
            host, text
        )
    return hosts, table, q

    # for row in range(random.randint(2, 6)):
    #     value = random.random() * 100
    #     table.add_row(
    #         f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
    #     )
    # return table


def main():
    # Add arguments
    parser = argparse.ArgumentParser(description="Ping multiple hosts and display the results in a table.")
    parser.add_argument('--maxLatency',
                        help='The maximum latency for coloring and icmp timeout.',
                        default=1000,
                        type=int)
    parser.add_argument('--minLatency',
                        help='The minimum latency for coloring.',
                        default=40,
                        type=int)
    parser.add_argument('--interval',
                        help='The interval to ping the devices.',
                        default=1,
                        type=int)
    parser.add_argument('hosts',
                        help='Hostnames to ping.',
                        type=str,
                        nargs=argparse.REMAINDER)
    args = vars(parser.parse_args())

    q = Queue()
    hosts = dict()
    for host in args['hosts']:
        threading.Timer(interval=args["interval"], function=ping_device, args=[host, args['maxLatency'], args['interval'], q]).start()
        hosts[host] = list()    
    hosts, table, q = generate_table(hosts, q, args['minLatency'], args['maxLatency'])
    with Live(table, refresh_per_second=4) as live:
        while True:
            time.sleep(0.1)
            hosts, table, q = generate_table(hosts, q, args['minLatency'], args['maxLatency'])
            live.update(table)

if __name__ == '__main__':
    main()