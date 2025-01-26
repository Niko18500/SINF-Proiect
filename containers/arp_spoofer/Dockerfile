FROM python:3.8-alpine

WORKDIR /app

COPY arp_spoof.py /app/

RUN pip install scapy getmac

CMD ["python3", "-u", "arp_spoof.py"]
