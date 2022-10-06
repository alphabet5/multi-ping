# Python script to ping multiple devices and display the status with history.

This is a simple script to make pinging and viewing the status of pinging multiple devices easy.

## Usage

```
usage: png [-h] [--maxLatency MAXLATENCY] [--minLatency MINLATENCY] [--interval INTERVAL] ...

Ping multiple hosts and display the results in a table.

positional arguments:
  hosts                 Hostnames to ping.

options:
  -h, --help            show this help message and exit
  --maxLatency MAXLATENCY
                        The maximum latency for coloring and icmp timeout.
  --minLatency MINLATENCY
                        The minimum latency for coloring.
  --interval INTERVAL   The interval to ping the devices.
```

## Example

```
% png 1.1.1.1 8.8.8.8 192.0.2.1
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Hostname/IP ┃                                         Ping Status ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1.1.1.1     │ ||||||||||||||||||||||||||||||||||||||||||||||||||| │
│ 8.8.8.8     │ ||||||||||||||||||||||||||||||||||||||||||||||||||| │
│ 192.0.2.1   │ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! │
└─────────────┴─────────────────────────────────────────────────────┘
```

## Building and Installing

```
python3 -m pip uninstall multi-ping -y
python3 setup.py bdist_wheel --universal
python3 -m pip install dist/multi_ping-*-py2.py3-none-any.whl
```


## Changelog

### 0.0.1
- Initial Release