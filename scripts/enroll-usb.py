#!/usr/bin/python3
"""Explicitly enroll an attached USB network interface; never stores passwords."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('interface', help='USB tether interface shown by ip -brief address')
args = parser.parse_args()
if os.geteuid() != 0:
    parser.error('Run with sudo')
if not args.interface or not all(c.isalnum() or c in '_-.' for c in args.interface):
    parser.error('Invalid interface name')
path = Path('/sys/class/net') / args.interface
result = subprocess.run(['udevadm', 'info', '-q', 'property', str(path)], capture_output=True, text=True, check=True)
props = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
keys = ('ID_VENDOR_ID', 'ID_MODEL_ID', 'ID_SERIAL_SHORT', 'ID_NET_DRIVER')
if not all(props.get(key) for key in keys) or props['ID_NET_DRIVER'] not in ('rndis_host', 'cdc_ether', 'cdc_ncm'):
    parser.error('Expected a USB tether adapter with vendor, product, serial and supported driver')
base = Path('/etc/hakcdevconsole')
base.mkdir(mode=0o700, exist_ok=True)
p = base / 'usb-device.json'
fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, 'w') as f:
    json.dump({key: props[key] for key in keys}, f)
p.chmod(0o600)
print('USB adapter enrolled. Start the guard service or run its dispatcher to apply.')
