#! /bin/bash

docker network create sinf-network

docker build -t downstream_container ./containers/downstream_container
docker build -t target_container ./containers/target_container
docker build -t arp_spoofer ./containers/arp_spoofer
