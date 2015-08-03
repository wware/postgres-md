#!/bin/bash

py.test

# * DANGER * This next line will kill ALL Docker instances running on your machine.
docker rm -f $(docker ps -a | tail --lines=+2 | cut -c -8)
