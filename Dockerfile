FROM python:3.6.10

RUN python -m pip install ruuvitag_sensor paho-mqtt && \
    apt update && \
    apt install -y bluez bluez-hcidump sudo

COPY ruuvi-publisher.py /ruuvi-publisher.py

ENTRYPOINT ["python", "/ruuvi-publisher.py"]
