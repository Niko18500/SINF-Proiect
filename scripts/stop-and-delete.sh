#! /bin/bash

docker container stop downstream-container target-container arp-spoofer
docker container rm downstream-container target-container arp-spoofer

docker image rm downstream_container target_container arp_spoofer