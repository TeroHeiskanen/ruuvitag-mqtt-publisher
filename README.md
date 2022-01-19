# RuuviTag MQTT publisher
## Description
Collects data from RuuviTags and publishes them as MQTT topics. Uses docker-compose for the convenience of keeping the service alive.

## Howto
- Edit MQTT brokers host, port and optionally username and password to docker-compose file. Certificates are not supported as of now.
- Run `docker-compose up --detach --build` to start the service.
- Check the logs using `docker-compose logs --follow`.
