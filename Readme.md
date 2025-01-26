# SINF-Proiect

This is an ARP Spoofing Attack PoC.

## Run information

To build the Docker images:
```
./scripts/build-images.sh
```

This will create the Docker network and images.

To run each container:
1. Downstream:
```
./scripts/run-downstream.sh
```

This container represents the server receiving and responding to requests.

2. Target:
```
./scripts/run-target.sh
```

This container represents the target of the attack. It sends requests to the downstream server.

3. ARP spoofer:
```
./scripts/run-arp-spoofer.sh
```

This container represents the ARP spoofer, that will spoof the target's IP address. It will then forward the requests to the original receiver (i.e. the downsream container), performing a Man-In-The-Middle.

To stop the containers and remove the docker images:
```
./scripts/stop-and-delete.sh
```