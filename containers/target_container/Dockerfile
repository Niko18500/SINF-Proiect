FROM python:3.8-alpine

WORKDIR /app

COPY target.py /app/

RUN pip install requests getmac

CMD ["python3", "-u", "target.py"]
