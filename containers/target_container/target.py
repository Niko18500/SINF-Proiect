from getmac import get_mac_address as gma
import time
import requests
import socket
import subprocess

def get_ip(container_name):
    """Resolve the IP address of a container by its name."""
    try:
        return socket.gethostbyname(container_name)
    except socket.gaierror as e:
        print(f"[ERROR] Unable to resolve IP for {container_name}: {e}", flush=True)
        return None

def get_mac_from_arp(ip):
    """Fetch the MAC address associated with the IP address from the ARP table."""
    try:
        arp_result = subprocess.check_output(f"arp -n {ip}", shell=True).decode('utf-8')
        
        for line in arp_result.splitlines():
            if ip in line:
                parts = line.split()
                if len(parts) >= 4:
                    return parts[3]
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ARP lookup failed for {ip}: {e}", flush=True)
    return None

if __name__ == "__main__":
    print(f"The target's MAC address: {gma()}", flush=True)

    downstream_container_name = "downstream-container"
    target_ip = get_ip(downstream_container_name)
    downstream_url = f"http://{target_ip}:8080"

    while True:
        try:
            print(f"[INFO] Sending request to {downstream_url}", flush=True)
            response = requests.get(downstream_url)
            print(f"[RESPONSE] {response.status_code}: {response.text[:50]}", flush=True)

            mac_address = get_mac_from_arp(target_ip)
            if mac_address:
                print(f"[INFO] MAC address for {target_ip}: {mac_address}", flush=True)
            else:
                print(f"[INFO] MAC address not found for {target_ip}", flush=True)
        except Exception as e:
            print(f"[ERROR] Unable to reach {downstream_url}: {e}", flush=True)
        
        time.sleep(5)
