import os
import sys
import json
import logging
import paho.mqtt.client as mqtt
from ruuvitag_sensor.ruuvi import RuuviTagSensor


class RuuviTagMqttPublisher:

    def __init__(self, mqtt_client):
        self._mqtt_client = mqtt_client

    def _handle_data(self, data):
        mac, data = data

        del data["mac"]
        del data["data_format"]

        base_topic = "ruuvitag/%s" % mac.replace(":", "").lower()

        for name, value in data.items():
            topic = "%s/%s" % (base_topic, name)

            logger.info("Publishing topic %s, payload %s", topic, value)
            self._mqtt_client.publish(topic, payload=value, qos=0)

    def run(self):
        RuuviTagSensor.get_datas(self._handle_data)

if __name__ == "__main__":
    address = os.environ.get("MQTT_BROKER_ADDRESS")
    port = int(os.environ.get("MQTT_BROKER_PORT", 1883))
    user = os.environ.get("MQTT_BROKER_USERNAME", "")
    password = os.environ.get("MQTT_BROKER_PASSWORD", "")
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    logger = logging.getLogger("ruuvitag_sensor")
    logger.setLevel(log_level)

    logger = logging.getLogger("mqtt")
    logger.setLevel(log_level)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    logging.basicConfig(level=log_level, format="%(asctime)s - %(message)s")

    mqtt_client = mqtt.Client("")
    mqtt_client.enable_logger(logging.getLogger("mqtt"))

    if user and password:
      mqtt_client.username_pw_set(user, password)
    else:
      logger.info("Username and/or password not given, connecting anonymously")

    if not address or not port:
      logger.error("Address or port not given, exiting...")
      sys.exit(1)

    logger.info("Publishing MQTT topics to %s:%d" % (address, port))

    mqtt_client.connect_async(address, port=port)
    mqtt_client.loop_start()

    logger.info("Listening for RuuviTags...")

    collector = RuuviTagMqttPublisher(mqtt_client)
    collector.run()
